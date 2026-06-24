<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { httpEvents } from '@/services/http-client'

const toast = useToast()

function surReseau(e) { toast.add({ severity: 'error', summary: 'Connexion perdue', detail: e.detail.message, life: 5000 }) }
function surServeur(e) { toast.add({ severity: 'error', summary: 'Erreur serveur', detail: e.detail.message, life: 5000 }) }
function surSession(e) { toast.add({ severity: 'warn', summary: 'Session', detail: e.detail.message, life: 4000 }) }

onMounted(() => {
  httpEvents.addEventListener('reseau', surReseau)
  httpEvents.addEventListener('serveur', surServeur)
  httpEvents.addEventListener('session', surSession)
})
onUnmounted(() => {
  httpEvents.removeEventListener('reseau', surReseau)
  httpEvents.removeEventListener('serveur', surServeur)
  httpEvents.removeEventListener('session', surSession)
})
</script>

<template>
  <router-view />
  <Toast position="top-right" />
  <ConfirmDialog />
</template>
