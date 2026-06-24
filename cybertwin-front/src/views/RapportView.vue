<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { analyseService } from '@/services/analyse-service'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'
import { labelTypeActif, labelCriticite } from '@/constants/enums'

const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const rapport = ref(null)
const chargement = ref(false)
const generationPdf = ref(false)
const entrepriseId = computed(() => entrepriseStore.selectionId)

onMounted(charger)
watch(entrepriseId, charger)
async function charger() {
  if (!entrepriseId.value) { rapport.value = null; return }
  chargement.value = true
  try { rapport.value = await analyseService.rapport(entrepriseId.value) }
  catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}

async function telechargerPdf() {
  if (!rapport.value) return
  generationPdf.value = true
  // Petit delai pour afficher l'etat de generation (UX).
  await new Promise((r) => setTimeout(r, 5000))
  try {
    const { genererRapportPdf } = await import('@/services/pdf-service')
    genererRapportPdf(rapport.value)
    toast.add({ severity: 'success', summary: 'PDF genere', detail: 'Le rapport a ete telecharge.', life: 3000 })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erreur', detail: 'Echec de la generation PDF.', life: 4000 })
  } finally { generationPdf.value = false }
}

const severiteRisque = (n) => ({ FAIBLE: 'success', MOYEN: 'warn', ELEVE: 'danger' }[n] || 'secondary')
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Rapport de securite</h1>
        <p class="page-subtitle">Synthese complete pour l'entreprise selectionnee.</p>
      </div>
      <Button v-if="rapport" :label="generationPdf ? 'Generation...' : 'Telecharger le PDF'"
              :icon="generationPdf ? 'pi pi-spin pi-spinner' : 'pi pi-file-pdf'"
              :disabled="generationPdf" @click="telechargerPdf" />
    </div>

    <Message v-if="!entrepriseId" severity="warn" :closable="false">Selectionnez une entreprise.</Message>
    <div v-else-if="chargement" class="spinner-wrap"><ProgressSpinner /><span class="muted">Chargement du rapport...</span></div>

    <template v-else-if="rapport">
      <div class="panel fade-up">
        <h2 style="margin-top:0">1. Presentation de l'entreprise</h2>
        <div class="stat-grid">
          <div><span class="muted">Nom</span><div>{{ rapport.entreprise.nom }}</div></div>
          <div><span class="muted">Secteur</span><div>{{ rapport.entreprise.secteur_activite }}</div></div>
          <div><span class="muted">Employes</span><div>{{ rapport.entreprise.nombre_employes }}</div></div>
          <div><span class="muted">Serveurs</span><div>{{ rapport.entreprise.nombre_serveurs }}</div></div>
          <div><span class="muted">Postes clients</span><div>{{ rapport.entreprise.nombre_postes_clients }}</div></div>
        </div>
        <div style="margin-top:0.75rem">
          <span class="muted">Services exposes : </span>
          <Tag v-for="s in rapport.entreprise.services_exposes" :key="s" :value="s" severity="info" style="margin:2px" />
          <span v-if="!rapport.entreprise.services_exposes?.length" class="muted">aucun</span>
        </div>
      </div>

      <div class="panel fade-up" style="margin-top:1.25rem">
        <h2 style="margin-top:0">2. Inventaire des actifs ({{ rapport.inventaire_actifs.length }})</h2>
        <DataTable :value="rapport.inventaire_actifs" stripedRows responsiveLayout="scroll">
          <template #empty><div class="empty">Aucun actif.</div></template>
          <Column field="nom" header="Nom" />
          <Column header="Type"><template #body="{ data }">{{ labelTypeActif(data.type_actif) }}</template></Column>
          <Column field="description" header="Description" />
        </DataTable>
      </div>

      <div class="panel fade-up" style="margin-top:1.25rem">
        <h2 style="margin-top:0">3. Vulnerabilites detectees ({{ rapport.vulnerabilites_detectees.length }})</h2>
        <DataTable :value="rapport.vulnerabilites_detectees" stripedRows responsiveLayout="scroll">
          <template #empty><div class="empty">Aucune vulnerabilite.</div></template>
          <Column field="libelle" header="Libelle" />
          <Column header="Criticite"><template #body="{ data }">{{ labelCriticite(data.criticite) }}</template></Column>
          <Column field="description" header="Description" />
        </DataTable>
      </div>

      <div class="panel fade-up" style="margin-top:1.25rem">
        <h2 style="margin-top:0">4. Niveau de risque</h2>
        <div class="row" style="align-items:center; gap:1.5rem">
          <div><span class="muted">Score global</span><div class="stat-value">{{ rapport.analyse_risque.score }}</div></div>
          <div>
            <span class="muted">Niveau</span>
            <div style="margin-top:0.4rem"><Tag :value="rapport.analyse_risque.niveau_risque" :severity="severiteRisque(rapport.analyse_risque.niveau_risque)" style="font-size:1rem; padding:0.4rem 0.8rem" /></div>
          </div>
        </div>
      </div>

      <div class="panel fade-up" style="margin-top:1.25rem">
        <h2 style="margin-top:0">5. Recommandations de securite</h2>
        <ul style="line-height:1.9; padding-left:1.2rem">
          <li v-for="(r, i) in rapport.recommandations" :key="i">{{ r }}</li>
        </ul>
      </div>
    </template>

    <!-- Overlay de generation PDF -->
    <Dialog :visible="generationPdf" modal :closable="false" :showHeader="false" :style="{ width: '320px' }">
      <div style="text-align:center; padding:1.5rem 0.5rem">
        <ProgressSpinner style="width:48px; height:48px" />
        <h3 style="margin:1rem 0 0.25rem">Generation du PDF</h3>
        <p class="muted" style="margin:0">Mise en forme du rapport en cours...</p>
      </div>
    </Dialog>
  </div>
</template>
