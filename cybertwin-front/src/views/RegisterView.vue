<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth.store'
import { messageErreur } from '@/services/http-client'
import { ROLES_OPTIONS } from '@/constants/enums'
import AppLogo from '@/components/shared/AppLogo.vue'
import { SOCIETE } from '@/constants/societe'

const auth = useAuthStore()
const router = useRouter()
const toast = useToast()
const form = ref({ email: '', mot_de_passe: '', nom: '', prenom: '', role: 'ANALYSTE' })
const chargement = ref(false)

async function inscription() {
  chargement.value = true
  try {
    await auth.register({ ...form.value })
    await auth.login(form.value.email, form.value.mot_de_passe)
    toast.add({ severity: 'success', summary: 'Compte cree', detail: 'Bienvenue sur CyberTwin', life: 3000 })
    router.push('/')
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Echec', detail: messageErreur(e), life: 5000 })
  } finally { chargement.value = false }
}
</script>

<template>
  <div class="auth-card">
    <div class="text-center" style="margin-bottom:1rem">
      <AppLogo :size="56" />
      <h1 class="auth-title" style="margin-top:0.5rem">Inscription</h1>
      <p class="auth-sub">Creez votre compte CyberTwin</p>
    </div>
    <Message severity="info" :closable="false" style="margin-bottom:1rem">
      {{ SOCIETE.produit }} par {{ SOCIETE.nom }} aide les PME a evaluer leur risque cyber.
      Le tout premier compte cree devient automatiquement administrateur.
    </Message>
    <div class="row">
      <div class="field" style="flex:1"><label>Prenom</label><InputText v-model="form.prenom" class="full" /></div>
      <div class="field" style="flex:1"><label>Nom</label><InputText v-model="form.nom" class="full" /></div>
    </div>
    <div class="field">
      <label>Email</label>
      <IconField><InputIcon class="pi pi-envelope" /><InputText v-model="form.email" class="full" placeholder="vous@exemple.fr" /></IconField>
    </div>
    <div class="field">
      <label>Role souhaite</label>
      <Select v-model="form.role" :options="ROLES_OPTIONS" optionLabel="label" optionValue="value" class="full" />
    </div>
    <div class="field">
      <label>Mot de passe</label>
      <Password v-model="form.mot_de_passe" toggleMask class="full" inputClass="full" />
      <small class="muted">Min. 12 caracteres, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractere special (CNIL).</small>
    </div>
    <Button label="Creer mon compte" icon="pi pi-user-plus" class="full mt-1" :loading="chargement" @click="inscription" />
    <p class="text-center muted mt-1">
      Deja inscrit ? <router-link to="/login" style="color:var(--ct-primary); font-weight:600">Connexion</router-link>
    </p>
  </div>
</template>
