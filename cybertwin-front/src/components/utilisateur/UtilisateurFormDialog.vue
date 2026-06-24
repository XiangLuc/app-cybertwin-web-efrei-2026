<script setup>
import { ref, watch } from 'vue'

const props = defineProps({ visible: { type: Boolean, default: false } })
const emit = defineEmits(['update:visible', 'submit'])

const ROLES_ADMIN = [
  { label: 'Administrateur', value: 'ADMIN' },
  { label: 'Analyste', value: 'ANALYSTE' },
  { label: 'Lecteur', value: 'LECTEUR' },
]

const form = ref(vide())
const erreurs = ref({})

function vide() {
  return { email: '', mot_de_passe: '', nom: '', prenom: '', role: 'LECTEUR' }
}

watch(() => props.visible, (o) => { if (o) { form.value = vide(); erreurs.value = {} } })

function valider() {
  const e = {}
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.value.email)) e.email = 'Email invalide'
  if (!form.value.mot_de_passe) e.mot_de_passe = 'Mot de passe requis'
  erreurs.value = e
  return Object.keys(e).length === 0
}

function soumettre() {
  if (!valider()) return
  emit('submit', { payload: { ...form.value } })
}
</script>

<template>
  <Dialog :visible="visible" header="Nouvel utilisateur" modal :style="{ width: '30rem' }"
          @update:visible="emit('update:visible', $event)">
    <div class="field">
      <label>Email *</label>
      <InputText v-model="form.email" class="full" :invalid="!!erreurs.email" />
      <small v-if="erreurs.email" class="p-error">{{ erreurs.email }}</small>
    </div>
    <div class="row">
      <div class="field" style="flex:1"><label>Prenom</label><InputText v-model="form.prenom" class="full" /></div>
      <div class="field" style="flex:1"><label>Nom</label><InputText v-model="form.nom" class="full" /></div>
    </div>
    <div class="field">
      <label>Role</label>
      <Select v-model="form.role" :options="ROLES_ADMIN" optionLabel="label" optionValue="value" class="full" />
    </div>
    <div class="field">
      <label>Mot de passe *</label>
      <Password v-model="form.mot_de_passe" toggleMask :feedback="true" class="full" inputClass="full" :invalid="!!erreurs.mot_de_passe" />
      <small class="muted">Min. 12 caracteres, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractere special (CNIL).</small>
      <small v-if="erreurs.mot_de_passe" class="p-error">{{ erreurs.mot_de_passe }}</small>
    </div>

    <template #footer>
      <Button label="Annuler" text severity="secondary" @click="emit('update:visible', false)" />
      <Button label="Creer" icon="pi pi-check" @click="soumettre" />
    </template>
  </Dialog>
</template>
