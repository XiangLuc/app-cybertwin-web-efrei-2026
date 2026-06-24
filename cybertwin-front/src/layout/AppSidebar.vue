<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useUiStore } from '@/stores/ui.store'
import AppLogo from '@/components/shared/AppLogo.vue'

const auth = useAuthStore()
const ui = useUiStore()
const route = useRoute()

const liens = computed(() => {
  const base = [
    { to: '/', icon: 'pi pi-home', label: 'Accueil', exact: true },
    { to: '/a-propos', icon: 'pi pi-info-circle', label: 'Qui sommes-nous' },
    { to: '/entreprises', icon: 'pi pi-building', label: 'Entreprises' },
    { to: '/actifs', icon: 'pi pi-server', label: 'Actifs' },
    { to: '/vulnerabilites', icon: 'pi pi-shield', label: 'Vulnerabilites' },
    { to: '/tableau-de-bord', icon: 'pi pi-chart-bar', label: 'Tableau de bord' },
    { to: '/comparaison', icon: 'pi pi-sliders-h', label: 'Comparaison' },
    { to: '/rapport', icon: 'pi pi-file', label: 'Rapport' },
    { to: '/historique', icon: 'pi pi-history', label: 'Historique' },
    { to: '/profil', icon: 'pi pi-user', label: 'Mon profil' },
  ]
  if (auth.estAdmin) base.push({ to: '/utilisateurs', icon: 'pi pi-users', label: 'Utilisateurs' })
  return base
})
const estActif = (lien) => (lien.exact ? route.path === '/' : route.path.startsWith(lien.to))
</script>

<template>
  <aside class="app-sidebar" :class="{ reduite: ui.sidebarReduite, 'mobile-ouverte': ui.sidebarMobileOuverte }">
    <div class="brand">
      <AppLogo :size="34" />
      <div class="brand-text">
        <div class="brand-name">CyberTwin</div>
        <div class="brand-sub">Risque cyber PME</div>
      </div>
    </div>

    <nav class="nav">
      <div class="nav-section">Navigation</div>
      <router-link
        v-for="lien in liens" :key="lien.to" :to="lien.to" class="nav-link"
        :class="{ 'router-link-active': estActif(lien) }"
        @click="ui.fermerSidebarMobile()" v-tooltip.right="ui.sidebarReduite ? lien.label : ''"
      >
        <i :class="lien.icon" />
        <span>{{ lien.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>
