<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useUiStore } from '@/stores/ui.store'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import NotificationBell from '@/components/shared/NotificationBell.vue'

const auth = useAuthStore()
const ui = useUiStore()
const entrepriseStore = useEntrepriseStore()
const router = useRouter()
const menu = ref()

const severiteRole = computed(() => ({ ADMIN: 'danger', ANALYSTE: 'info', LECTEUR: 'secondary' }[auth.role] || 'secondary'))
const items = [
  { label: auth.nomAffiche, disabled: true },
  { separator: true },
  { label: 'Mon profil', icon: 'pi pi-user', command: () => router.push('/profil') },
  { label: 'Accueil', icon: 'pi pi-home', command: () => router.push('/') },
  { label: 'Deconnexion', icon: 'pi pi-sign-out', command: () => { auth.logout(); router.push('/login') } },
]
</script>

<template>
  <header class="app-topbar">
    <div style="display:flex; align-items:center; gap:0.6rem;">
      <button class="icon-btn mobile-only" @click="ui.basculerSidebarMobile()"><i class="pi pi-bars" /></button>
      <button class="icon-btn desktop-only" @click="ui.basculerSidebar()" v-tooltip.bottom="'Reduire le menu'"><i class="pi pi-bars" /></button>
      <i class="pi pi-building muted desktop-only" />
      <Select
        :modelValue="entrepriseStore.selectionId" :options="entrepriseStore.entreprises"
        optionLabel="nom" optionValue="id" placeholder="Aucune entreprise" filter
        style="min-width: 200px" @change="entrepriseStore.selectionner($event.value)"
      />
    </div>

    <div style="display:flex; align-items:center; gap:0.6rem;">
      <NotificationBell />
      <button class="icon-btn" @click="ui.basculerTheme()" v-tooltip.bottom="ui.estSombre ? 'Mode clair' : 'Mode sombre'">
        <i :class="ui.estSombre ? 'pi pi-sun' : 'pi pi-moon'" />
      </button>
      <Tag :value="auth.role" :severity="severiteRole" class="desktop-only" />
      <button class="user-btn" @click="menu.toggle($event)">
        <Avatar :label="auth.nomAffiche?.charAt(0)?.toUpperCase() || '?'" shape="circle" style="background:var(--ct-primary); color:#fff" />
        <i class="pi pi-angle-down muted desktop-only" />
      </button>
      <Menu ref="menu" :model="items" :popup="true" />
    </div>
  </header>
</template>

<style scoped>
.user-btn { display:flex; align-items:center; gap:0.4rem; background:transparent; border:none; cursor:pointer; color:var(--ct-text); }
</style>
