<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { entrepriseService } from '@/services/entreprise-service'
import { useAuthStore } from '@/stores/auth.store'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'
import ListeEntreprise from '@/components/entreprise/ListeEntreprise.vue'
import EntrepriseFormDialog from '@/components/entreprise/EntrepriseFormDialog.vue'

const auth = useAuthStore()
const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const confirm = useConfirm()

const entreprises = ref([])
const chargement = ref(true)
const dialogVisible = ref(false)
const selection = ref(null)

onMounted(charger)
async function charger() {
  chargement.value = true
  try { entreprises.value = await entrepriseService.list() }
  catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}

function ouvrirCreation() { selection.value = null; dialogVisible.value = true }
function ouvrirEdition(e) { selection.value = e; dialogVisible.value = true }
function activer(e) { entrepriseStore.selectionner(e.id); toast.add({ severity: 'info', summary: 'Entreprise active', detail: e.nom, life: 2000 }) }

function onSubmit({ payload, edition, id }) {
  if (edition) {
    confirm.require({
      header: 'Confirmer la modification', message: `Enregistrer les modifications de "${payload.nom}" ?`,
      icon: 'pi pi-pencil', acceptLabel: 'Enregistrer', rejectLabel: 'Annuler',
      accept: () => executer(entrepriseService.update(id, payload), 'Entreprise modifiee.'),
    })
  } else executer(entrepriseService.create(payload), 'Entreprise creee.')
}

function supprimer(e) {
  confirm.require({
    header: 'Confirmer la suppression',
    message: `Supprimer "${e.nom}" ?\n\nRepercussions : tous ses actifs et leurs vulnerabilites seront definitivement supprimes (cascade).`,
    icon: 'pi pi-exclamation-triangle', acceptLabel: 'Supprimer', rejectLabel: 'Annuler', acceptClass: 'p-button-danger',
    accept: () => executer(entrepriseService.remove(e.id), 'Entreprise supprimee.'),
  })
}

async function executer(promesse, succes) {
  try {
    await promesse
    dialogVisible.value = false
    toast.add({ severity: 'success', summary: 'Succes', detail: succes, life: 2500 })
    await charger(); await entrepriseStore.charger()
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Entreprises</h1>
        <p class="page-subtitle">Gestion des entreprises et de leur profil.</p>
      </div>
      <Button v-if="auth.peutEcrire" label="Nouvelle entreprise" icon="pi pi-plus" @click="ouvrirCreation" />
    </div>

    <div v-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>
    <div v-else class="panel">
      <ListeEntreprise
        :entreprises="entreprises" :peutEcrire="auth.peutEcrire" :selectionId="entrepriseStore.selectionId"
        @edit="ouvrirEdition" @delete="supprimer" @select="activer"
      />
    </div>

    <EntrepriseFormDialog v-model:visible="dialogVisible" :entreprise="selection" @submit="onSubmit" />
  </div>
</template>
