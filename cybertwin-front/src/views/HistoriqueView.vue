<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { analyseService } from '@/services/analyse-service'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'

const entrepriseStore = useEntrepriseStore()
const toast = useToast()
const entrees = ref([])
const chargement = ref(false)
const entrepriseId = computed(() => entrepriseStore.selectionId)

onMounted(charger)
watch(entrepriseId, charger)
async function charger() {
  if (!entrepriseId.value) { entrees.value = []; return }
  chargement.value = true
  try { entrees.value = await analyseService.history(entrepriseId.value) }
  catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}

async function relancer() {
  try {
    await analyseService.calculerRisque(entrepriseId.value)
    toast.add({ severity: 'success', summary: 'Analyse lancee', detail: 'Historique mis a jour.', life: 2500 })
    await charger()
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
}

const severiteRisque = (n) => ({ FAIBLE: 'success', MOYEN: 'warn', ELEVE: 'danger' }[n] || 'secondary')
const dateFr = (iso) => new Date(iso).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' })

// Graphe d'evolution du score (du plus ancien au plus recent)
const chartData = computed(() => {
  const ordre = [...entrees.value].reverse()
  return {
    labels: ordre.map((e) => dateFr(e.created_at)),
    datasets: [{
      label: 'Score de risque', data: ordre.map((e) => e.score),
      borderColor: '#0ea5e9', backgroundColor: 'rgba(14,165,233,0.15)', fill: true, tension: 0.3, pointRadius: 4,
    }],
  }
})
const chartOptions = {
  plugins: { legend: { labels: { color: '#94a3b8' } } },
  scales: {
    x: { ticks: { color: '#94a3b8', maxRotation: 0 }, grid: { display: false } },
    y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, beginAtZero: true },
  },
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Historique des analyses</h1>
        <p class="page-subtitle">
          Tracabilite des calculs de risque
          <span v-if="entrepriseStore.selection">de <strong>{{ entrepriseStore.selection.nom }}</strong></span>.
        </p>
      </div>
      <Button v-if="entrepriseId" label="Lancer une analyse" icon="pi pi-bolt" @click="relancer" />
    </div>

    <Message v-if="!entrepriseId" severity="warn" :closable="false">Selectionnez une entreprise.</Message>
    <div v-else-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>
    <Message v-else-if="!entrees.length" severity="info" :closable="false">
      Aucune analyse enregistree. Lancez-en une depuis le tableau de bord ou ci-dessus.
    </Message>

    <template v-else>
      <div class="panel" v-if="entrees.length > 1">
        <h3 style="margin-top:0">Evolution du score</h3>
        <Chart type="line" :data="chartData" :options="chartOptions" style="height:280px" />
      </div>
      <div class="panel" :style="entrees.length > 1 ? 'margin-top:1.25rem' : ''">
        <DataTable :value="entrees" paginator :rows="10" stripedRows responsiveLayout="scroll">
          <Column header="Date"><template #body="{ data }">{{ dateFr(data.created_at) }}</template></Column>
          <Column field="utilisateur_email" header="Auteur">
            <template #body="{ data }"><span :class="{ muted: !data.utilisateur_email }">{{ data.utilisateur_email || '—' }}</span></template>
          </Column>
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
