<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth.store'
import { messageErreur } from '@/services/http-client'
import AppLogo from '@/components/shared/AppLogo.vue'
import { SOCIETE } from '@/constants/societe'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const toast = useToast()
const email = ref('')
const motDePasse = ref('')
const chargement = ref(false)

async function connexion() {
  if (!email.value || !motDePasse.value) {
    toast.add({ severity: 'warn', summary: 'Champs requis', detail: 'Email et mot de passe.', life: 3000 }); return
  }
  chargement.value = true
  try {
    await auth.login(email.value, motDePasse.value)
    toast.add({ severity: 'success', summary: 'Connecte', detail: `Bienvenue ${auth.nomAffiche}`, life: 2500 })
    router.push(route.query.redirect || '/')
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Echec', detail: messageErreur(e, 'Identifiants incorrects.'), life: 4000 })
  } finally { chargement.value = false }
}
</script>

<template>
  <div class="auth-card">
    <div class="text-center" style="margin-bottom:1.25rem">
      <AppLogo :size="56" />
      <h1 class="auth-title" style="margin-top:0.5rem">CyberTwin</h1>
      <p class="auth-sub">Connexion a votre espace securite</p>
    </div>
    <Message severity="info" :closable="false" style="margin-bottom:1.25rem">
      {{ SOCIETE.produit }} par {{ SOCIETE.nom }} : {{ SOCIETE.slogan }} Cartographiez vos actifs,
      identifiez vos vulnerabilites et evaluez votre risque cyber.
    </Message>
    <div>
    </div>
    <div class="field">
      <label>Email</label>
      <IconField>
        <InputIcon class="pi pi-envelope" />
        <InputText v-model="email" class="full" placeholder="vous@exemple.fr" @keyup.enter="connexion" />
      </IconField>
    </div>
    <div class="field">
      <label>Mot de passe</label>
      <Password v-model="motDePasse" :feedback="false" toggleMask class="full" inputClass="full" @keyup.enter="connexion" />
    </div>
    <Button label="Se connecter" icon="pi pi-sign-in" class="full mt-1" :loading="chargement" @click="connexion" />
    <p class="text-center muted mt-1">
      Pas de compte ? <router-link to="/register" style="color:var(--ct-primary); font-weight:600">Inscription</router-link>
    </p>
  </div>
</template>
