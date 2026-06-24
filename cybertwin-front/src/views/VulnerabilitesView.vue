<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { vulnerabiliteService } from '@/services/vulnerabilite-service'
import { actifService } from '@/services/actif-service'
import { useAuthStore } from '@/stores/auth.store'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'
import ListeVulnerabilite from '@/components/vulnerabilite/ListeVulnerabilite.vue'
import VulnerabiliteFormDialog from '@/components/vulnerabilite/VulnerabiliteFormDialog.vue'

const auth = useAuthStore()
const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const confirm = useConfirm()

const vulnerabilites = ref([])
const actifs = ref([])
const chargement = ref(false)
const dialogVisible = ref(false)
const selection = ref(null)
const entrepriseId = computed(() => entrepriseStore.selectionId)

onMounted(charger)
watch(entrepriseId, charger)
async function charger() {
  if (!entrepriseId.value) { vulnerabilites.value = []; actifs.value = []; return }
  chargement.value = true
  try {
    [vulnerabilites.value, actifs.value] = await Promise.all([
      vulnerabiliteService.list({ entrepriseId: entrepriseId.value }),
      actifService.list(entrepriseId.value),
    ])
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}

function ouvrirCreation() { selection.value = null; dialogVisible.value = true }
function ouvrirEdition(v) { selection.value = v; dialogVisible.value = true }
function onSubmit({ payload, edition, id }) {
  if (edition) {
    confirm.require({
      header: 'Confirmer la modification', message: `Enregistrer les modifications de "${payload.libelle}" ?`,
      icon: 'pi pi-pencil', acceptLabel: 'Enregistrer', rejectLabel: 'Annuler',
      accept: () => executer(vulnerabiliteService.update(id, payload), 'Vulnerabilite modifiee.'),
    })
  } else executer(vulnerabiliteService.create(payload), 'Vulnerabilite creee.')
}
function supprimer(v) {
  confirm.require({
    header: 'Confirmer la suppression', message: `Supprimer la vulnerabilite "${v.libelle}" ?`,
    icon: 'pi pi-exclamation-triangle', acceptLabel: 'Supprimer', rejectLabel: 'Annuler', acceptClass: 'p-button-danger',
    accept: () => executer(vulnerabiliteService.remove(v.id), 'Vulnerabilite supprimee.'),
  })
}
async function executer(promesse, succes) {
  try { await promesse; dialogVisible.value = false
    toast.add({ severity: 'success', summary: 'Succes', detail: succes, life: 2500 }); await charger()
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Vulnerabilites</h1>
        <p class="page-subtitle">
          Failles associees aux actifs
          <span v-if="entrepriseStore.selection">de <strong>{{ entrepriseStore.selection.nom }}</strong></span>.
        </p>
      </div>
      <Button v-if="auth.peutEcrire && actifs.length" label="Nouvelle vulnerabilite" icon="pi pi-plus" @click="ouvrirCreation" />
    </div>

    <Message v-if="!entrepriseId" severity="warn" :closable="false">Selectionnez une entreprise dans la barre du haut.</Message>
    <Message v-else-if="!chargement && !actifs.length" severity="info" :closable="false">
      Cette entreprise n'a aucun actif. Ajoutez d'abord des actifs pour leur associer des vulnerabilites.
    </Message>

    <div v-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>
    <div v-else-if="entrepriseId" class="panel">
      <ListeVulnerabilite :vulnerabilites="vulnerabilites" :actifs="actifs" :peutEcrire="auth.peutEcrire" @edit="ouvrirEdition" @delete="supprimer" />
    </div>

    <VulnerabiliteFormDialog v-model:visible="dialogVisible" :vulnerabilite="selection" :actifs="actifs" @submit="onSubmit" />
  </div>
</template>
