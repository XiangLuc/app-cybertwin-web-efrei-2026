<script setup>
import { ref, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { analyseService } from '@/services/analyse-service'
import { messageErreur } from '@/services/http-client'

/**
 * Comparaison multi-entreprises : selectionnez plusieurs entreprises pour
 * comparer leurs scores et niveaux de risque (exploite /risk/calculate).
 */
const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const selection = ref([])
const resultats = ref([])
const chargement = ref(false)

watch(selection, comparer)

async function comparer() {
  if (!selection.value.length) { resultats.value = []; return }
  chargement.value = true
  try {
    const reponses = await Promise.all(selection.value.map((id) => analyseService.calculerRisque(id)))
    resultats.value = reponses.map((r) => ({
      ...r,
      nom: entrepriseStore.entreprises.find((e) => e.id === r.entreprise_id)?.nom || `#${r.entreprise_id}`,
    }))
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 })
  } finally { chargement.value = false }
}

const severiteRisque = (n) => ({ FAIBLE: 'success', MOYEN: 'warn', ELEVE: 'danger' }[n] || 'secondary')
const couleurNiveau = { FAIBLE: '#22c55e', MOYEN: '#eab308', ELEVE: '#ef4444' }

const chartData = () => ({
  labels: resultats.value.map((r) => r.nom),
  datasets: [{
    label: 'Score de risque',
    data: resultats.value.map((r) => r.score),
    backgroundColor: resultats.value.map((r) => couleurNiveau[r.niveau_risque] || '#0ea5e9'),
    borderRadius: 6,
  }],
})
const chartOptions = {
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
    y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, beginAtZero: true },
  },
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Comparaison multi-entreprises</h1>
        <p class="page-subtitle">Comparez le niveau de risque de plusieurs entreprises.</p>
      </div>
      <MultiSelect
        v-model="selection" :options="entrepriseStore.entreprises" optionLabel="nom" optionValue="id"
        display="chip" filter placeholder="Choisir des entreprises..." style="min-width:280px; max-width:420px"
      />
    </div>

    <Message v-if="!selection.length" severity="info" :closable="false">
      Selectionnez au moins deux entreprises pour les comparer.
    </Message>
    <div v-else-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>

    <template v-else-if="resultats.length">
      <div class="panel">
        <h3 style="margin-top:0">Scores de risque compares</h3>
        <Chart type="bar" :data="chartData()" :options="chartOptions" style="height:320px" />
      </div>
      <div class="panel" style="margin-top:1.25rem">
        <DataTable :value="resultats" stripedRows responsiveLayout="scroll">
          <Column field="nom" header="Entreprise" sortable />
          <Column field="nombre_actifs" header="Actifs" sortable />
          <Column field="nombre_vulnerabilites" header="Vulnerabilites" sortable />
          <Column field="score" header="Score" sortable />
          <Column header="Niveau" field="niveau_risque" sortable>
            <template #body="{ data }"><Tag :value="data.niveau_risque" :severity="severiteRisque(data.niveau_risque)" /></template>
          </Column>
        </DataTable>
      </div>
    </template>
  </div>
</template>
