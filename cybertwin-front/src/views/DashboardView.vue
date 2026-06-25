<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { analyseService } from '@/services/analyse-service'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { messageErreur } from '@/services/http-client'
import { labelTypeActif, labelCriticite, COULEUR_CRITICITE, COULEUR_RISQUE } from '@/constants/enums'

const entrepriseStore = useEntrepriseStore()
const toast = useToast()

const data = ref(null)
const risque = ref(null)
const chargement = ref(false)
const entrepriseId = computed(() => entrepriseStore.selectionId)

onMounted(charger)
watch(entrepriseId, charger)

async function charger() {
  if (!entrepriseId.value) { data.value = null; return }
  chargement.value = true
  try {
    [data.value, risque.value] = await Promise.all([
      analyseService.dashboard(entrepriseId.value),
      analyseService.calculerRisque(entrepriseId.value),
    ])
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 })
  } finally { chargement.value = false }
}

const severiteRisque = (n) => ({ FAIBLE: 'success', MOYEN: 'warn', ELEVE: 'danger' }[n] || 'secondary')

const optionsCommunes = {
  plugins: { legend: { labels: { color: '#94a3b8' } } },
  scales: {
    x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(148,163,184,0.15)' } },
    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(148,163,184,0.15)' }, beginAtZero: true },
  },
}

const chartActifs = computed(() => {
  const r = data.value?.repartition_actifs || {}
  return {
    labels: Object.keys(r).map(labelTypeActif),
    datasets: [{ label: 'Actifs', data: Object.values(r), backgroundColor: '#0ea5e9', borderRadius: 6 }],
  }
})
const chartCriticites = computed(() => {
  const r = data.value?.repartition_criticites || {}
  const labels = Object.keys(r)
  return {
    labels: labels.map(labelCriticite),
    datasets: [{ data: Object.values(r), backgroundColor: labels.map((c) => COULEUR_CRITICITE[c] || '#64748b'), borderWidth: 0 }],
  }
})
const optionsDoughnut = { plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }, cutout: '62%' }
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Tableau de bord</h1>
        <p class="page-subtitle">
          Synthese du risque
          <span v-if="entrepriseStore.selection">de <strong>{{ entrepriseStore.selection.nom }}</strong></span>.
        </p>
      </div>
    </div>

    <Message v-if="!entrepriseId" severity="warn" :closable="false">Selectionnez une entreprise.</Message>
    <div v-else-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>

    <template v-else-if="data">
      <div class="stat-grid">
        <div class="stat-card">
          <i class="pi pi-server stat-ic" />
          <div class="stat-label">Actifs</div>
          <div class="stat-value">{{ data.nombre_total_actifs }}</div>
        </div>
        <div class="stat-card">
          <i class="pi pi-shield stat-ic" />
          <div class="stat-label">Vulnerabilites</div>
          <div class="stat-value">{{ data.nombre_total_vulnerabilites }}</div>
        </div>
        <div class="stat-card">
          <i class="pi pi-gauge stat-ic" />
          <div class="stat-label">Score de risque</div>
          <div class="stat-value">{{ data.score_risque_global }}</div>
        </div>
        <div class="stat-card" :style="{ borderColor: COULEUR_RISQUE[data.niveau_risque] }">
          <i class="pi pi-exclamation-circle stat-ic" :style="{ color: COULEUR_RISQUE[data.niveau_risque] }" />
          <div class="stat-label">Niveau de risque</div>
          <div style="margin-top:0.6rem"><Tag :value="data.niveau_risque" :severity="severiteRisque(data.niveau_risque)" style="font-size:1rem; padding:0.4rem 0.8rem" /></div>
        </div>
      </div>

      <div class="row" style="margin-top:1.5rem; align-items:stretch">
        <div class="panel" style="flex:2; min-width:320px">
          <h3 style="margin-top:0">Repartition des actifs</h3>
          <Chart type="bar" :data="chartActifs" :options="optionsCommunes" style="height:300px" />
        </div>
        <div class="panel" style="flex:1; min-width:280px">
          <h3 style="margin-top:0">Criticite des vulnerabilites</h3>
          <Chart v-if="Object.keys(data.repartition_criticites || {}).length" type="doughnut" :data="chartCriticites" :options="optionsDoughnut" style="height:300px" />
          <div v-else class="empty">Aucune vulnerabilite.</div>
        </div>
      </div>

      <div v-if="risque" class="panel" style="margin-top:1.5rem">
        <h3 style="margin-top:0"><i class="pi pi-lightbulb" style="color:var(--ct-primary)" /> Recommandations de securite</h3>
        <ul class="reco-list">
          <li v-for="(r, i) in risque.recommandations" :key="i">{{ r }}</li>
        </ul>
      </div>
    </template>
  </div>
</template>

<style scoped>
.stat-ic { font-size: 1.4rem; color: var(--ct-primary); }
.stat-card { display: flex; flex-direction: column; gap: 0.15rem; }
.reco-list { line-height: 1.9; padding-left: 1.2rem; margin: 0.5rem 0 0; }
.reco-list li { margin-bottom: 0.3rem; }
</style>
