<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth.store'
import { authService } from '@/services/auth-service'
import { messageErreur } from '@/services/http-client'

const auth = useAuthStore()
const toast = useToast()
const form = ref({ ancien: '', nouveau: '', confirmation: '' })
const chargement = ref(false)

const severiteRole = (r) => ({ ADMIN: 'danger', ANALYSTE: 'info', LECTEUR: 'secondary' }[r] || 'secondary')

async function changer() {
  if (!form.value.ancien || !form.value.nouveau) {
    toast.add({ severity: 'warn', summary: 'Champs requis', detail: 'Renseignez les mots de passe.', life: 3000 }); return
  }
  if (form.value.nouveau !== form.value.confirmation) {
    toast.add({ severity: 'warn', summary: 'Confirmation', detail: 'Les mots de passe ne correspondent pas.', life: 3000 }); return
  }
  chargement.value = true
  try {
    await authService.changePassword(form.value.ancien, form.value.nouveau)
    toast.add({ severity: 'success', summary: 'Mot de passe modifie', detail: 'Changement effectue.', life: 3000 })
    form.value = { ancien: '', nouveau: '', confirmation: '' }
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Echec', detail: messageErreur(e), life: 5000 })
  } finally { chargement.value = false }
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Mon profil</h1>
        <p class="page-subtitle">Informations du compte et securite.</p>
      </div>
    </div>

    <div class="row" style="align-items:flex-start">
      <div class="panel" style="flex:1; min-width:280px">
        <h3 style="margin-top:0">Informations</h3>
        <div class="profil-ligne"><span class="muted">Nom</span><span>{{ auth.nomAffiche }}</span></div>
        <div class="profil-ligne"><span class="muted">Email</span><span>{{ auth.user?.email }}</span></div>
        <div class="profil-ligne"><span class="muted">Role</span><Tag :value="auth.role" :severity="severiteRole(auth.role)" /></div>
      </div>

      <div class="panel" style="flex:1.4; min-width:320px">
        <h3 style="margin-top:0">Changer mon mot de passe</h3>
        <div class="field">
          <label>Mot de passe actuel</label>
          <Password v-model="form.ancien" :feedback="false" toggleMask class="full" inputClass="full" />
        </div>
        <div class="field">
          <label>Nouveau mot de passe</label>
          <Password v-model="form.nouveau" toggleMask class="full" inputClass="full" />
          <small class="muted">Min. 12 caracteres, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractere special (CNIL).</small>
        </div>
        <div class="field">
          <label>Confirmer le nouveau mot de passe</label>
          <Password v-model="form.confirmation" :feedback="false" toggleMask class="full" inputClass="full" />
        </div>
        <Button label="Mettre a jour" icon="pi pi-check" :loading="chargement" @click="changer" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.profil-ligne { display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid var(--ct-border); }
.profil-ligne:last-child { border-bottom:none; }
</style>
