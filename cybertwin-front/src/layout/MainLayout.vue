<script setup>
import { onMounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'
import ChatbotWidget from '@/components/shared/ChatbotWidget.vue'
import AppFilAriane from '@/components/shared/AppFilAriane.vue'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { useUiStore } from '@/stores/ui.store'

const entrepriseStore = useEntrepriseStore()
const ui = useUiStore()
onMounted(() => entrepriseStore.charger())
</script>

<template>
  <div class="app-shell">
    <AppSidebar />
    <div class="sidebar-backdrop" :class="{ actif: ui.sidebarMobileOuverte }" @click="ui.fermerSidebarMobile()" />
    <div class="app-main" :class="{ reduite: ui.sidebarReduite }">
      <AppTopbar />
      <main class="app-content">
        <AppFilAriane /> 
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
    <ChatbotWidget />
  </div>
</template>
