<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useEntrepriseStore } from '@/stores/entreprise.store'

const auth = useAuthStore()
const entrepriseStore = useEntrepriseStore()
const router = useRouter()
const cartes = [
  { to: '/entreprises', icon: 'pi pi-building', titre: 'Entreprises', desc: 'Gerer les entreprises et leur profil.' },
  { to: '/actifs', icon: 'pi pi-server', titre: 'Actifs', desc: 'Inventorier le parc informatique.' },
  { to: '/vulnerabilites', icon: 'pi pi-shield', titre: 'Vulnerabilites', desc: 'Associer les failles aux actifs.' },
  { to: '/tableau-de-bord', icon: 'pi pi-chart-bar', titre: 'Tableau de bord', desc: 'Visualiser le risque et les statistiques.' },
  { to: '/rapport', icon: 'pi pi-file', titre: 'Rapport', desc: 'Generer le rapport de securite en PDF.' },
]
const selection = computed(() => entrepriseStore.selection)
</script>

<template>
  <div class="fade-up">
    <div class="hero panel">
      <div>
        <h1 class="page-title" style="font-size:1.9rem">Bonjour {{ auth.nomAffiche }}</h1>
        <p class="page-subtitle" style="max-width:540px">
          Bienvenue sur CyberTwin, le simulateur de risque cyber pour PME.
          <span v-if="selection">Entreprise active : <strong>{{ selection.nom }}</strong>.</span>
          <span v-else>Commencez par creer ou activer une entreprise.</span>
        </p>
        <div style="display:flex; gap:0.6rem; margin-top:1rem; flex-wrap:wrap">
          <Button label="Voir le tableau de bord" icon="pi pi-chart-bar" @click="router.push('/tableau-de-bord')" />
          <Button label="Gerer les entreprises" icon="pi pi-building" outlined @click="router.push('/entreprises')" />
        </div>
      </div>
      <i class="pi pi-shield hero-icon" />
    </div>

    <div class="stat-grid" style="margin-top:1.5rem">
      <div v-for="c in cartes" :key="c.to" class="stat-card" style="cursor:pointer" @click="router.push(c.to)">
        <i :class="c.icon" style="font-size:1.6rem; color:var(--ct-primary)" />
        <div class="stat-value" style="font-size:1.1rem; margin-top:0.7rem">{{ c.titre }}</div>
        <div class="muted" style="font-size:0.88rem; margin-top:0.25rem">{{ c.desc }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero { display:flex; align-items:center; justify-content:space-between; gap:1rem; overflow:hidden; position:relative;
  background: linear-gradient(120deg, var(--ct-surface), var(--ct-primary-soft)); }
.hero-icon { font-size:7rem; color:var(--ct-primary); opacity:0.18; animation: float 6s ease-in-out infinite; }
@media (max-width:700px){ .hero-icon{ display:none; } }
</style>
