<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { actifService } from '@/services/actif-service'
import { useAuthStore } from '@/stores/auth.store'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'
import ListeActif from '@/components/actif/ListeActif.vue'
import ActifFormDialog from '@/components/actif/ActifFormDialog.vue'

const auth = useAuthStore()
const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const confirm = useConfirm()

const actifs = ref([])
const chargement = ref(false)
const dialogVisible = ref(false)
const selection = ref(null)
const entrepriseId = computed(() => entrepriseStore.selectionId)

onMounted(charger)
watch(entrepriseId, charger)
async function charger() {
  if (!entrepriseId.value) { actifs.value = []; return }
  chargement.value = true
  try { actifs.value = await actifService.list(entrepriseId.value) }
  catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}

function ouvrirCreation() { selection.value = null; dialogVisible.value = true }
function ouvrirEdition(a) { selection.value = a; dialogVisible.value = true }

function onSubmit({ payload, edition, id }) {
  if (edition) {
    confirm.require({
      header: 'Confirmer la modification', message: `Enregistrer les modifications de "${payload.nom}" ?`,
      icon: 'pi pi-pencil', acceptLabel: 'Enregistrer', rejectLabel: 'Annuler',
      accept: () => executer(actifService.update(id, payload), 'Actif modifie.'),
    })
  } else executer(actifService.create(payload), 'Actif cree.')
}
function supprimer(a) {
  confirm.require({
    header: 'Confirmer la suppression',
    message: `Supprimer l'actif "${a.nom}" ?\n\nRepercussions : ses vulnerabilites associees seront aussi supprimees.`,
    icon: 'pi pi-exclamation-triangle', acceptLabel: 'Supprimer', rejectLabel: 'Annuler', acceptClass: 'p-button-danger',
    accept: () => executer(actifService.remove(a.id), 'Actif supprime.'),
  })
}
async function executer(promesse, succes) {
  try {
    await promesse; dialogVisible.value = false
    toast.add({ severity: 'success', summary: 'Succes', detail: succes, life: 2500 })
    await charger()
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Actifs</h1>
        <p class="page-subtitle">
          Inventaire du parc informatique
          <span v-if="entrepriseStore.selection">de <strong>{{ entrepriseStore.selection.nom }}</strong></span>.
        </p>
      </div>
      <Button v-if="auth.peutEcrire && entrepriseId" label="Nouvel actif" icon="pi pi-plus" @click="ouvrirCreation" />
    </div>

    <Message v-if="!entrepriseId" severity="warn" :closable="false">
      Selectionnez une entreprise dans la barre du haut pour gerer ses actifs.
    </Message>
    <div v-else-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>
    <div v-else class="panel">
      <ListeActif :actifs="actifs" :peutEcrire="auth.peutEcrire" @edit="ouvrirEdition" @delete="supprimer" />
    </div>

    <ActifFormDialog v-model:visible="dialogVisible" :actif="selection" :entrepriseId="entrepriseId" @submit="onSubmit" />
  </div>
</template>
