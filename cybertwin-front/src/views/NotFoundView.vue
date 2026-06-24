<script setup>
import { useRouter } from 'vue-router'
import AppLogo from '@/components/shared/AppLogo.vue'
const router = useRouter()
</script>

<template>
  <div class="auth-shell">
    <div class="auth-bg"><div class="auth-grid" /><div class="auth-blob b1" /><div class="auth-blob b2" /></div>
    <div class="text-center" style="position:relative; z-index:1">
      <AppLogo :size="64" />
      <h1 style="font-size:2.5rem; margin:0.5rem 0">404</h1>
      <p class="muted">Cette page n'existe pas.</p>
      <Button label="Retour a l'accueil" icon="pi pi-home" class="mt-1" @click="router.push('/')" />
    </div>
  </div>
</template>
