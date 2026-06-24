<script setup>
import { ref, watch } from 'vue'
import { SERVICES_EXPOSES } from '@/constants/enums'

const props = defineProps({
  visible: { type: Boolean, default: false },
  entreprise: { type: Object, default: null }, // null = creation
})
const emit = defineEmits(['update:visible', 'submit'])

const form = ref(vide())
const erreurs = ref({})

function vide() {
  return {
    nom: '', secteur_activite: '', nombre_employes: 0,
    nombre_serveurs: 0, nombre_postes_clients: 0, services_exposes: [],
  }
}

watch(
  () => props.visible,
  (ouvert) => {
    if (ouvert) {
      erreurs.value = {}
      form.value = props.entreprise
        ? { ...props.entreprise, services_exposes: [...(props.entreprise.services_exposes || [])] }
        : vide()
    }
  },
)

function valider() {
  const e = {}
  if (!form.value.nom?.trim()) e.nom = 'Nom requis'
  if (!form.value.secteur_activite?.trim()) e.secteur_activite = "Secteur requis"
  erreurs.value = e
  return Object.keys(e).length === 0
}

function soumettre() {
  if (!valider()) return
  emit('submit', {
    payload: {
      nom: form.value.nom.trim(),
      secteur_activite: form.value.secteur_activite.trim(),
      nombre_employes: form.value.nombre_employes || 0,
      nombre_serveurs: form.value.nombre_serveurs || 0,
      nombre_postes_clients: form.value.nombre_postes_clients || 0,
      services_exposes: form.value.services_exposes || [],
    },
    edition: !!props.entreprise,
    id: props.entreprise?.id,
  })
}
</script>

<template>
  <Dialog
    :visible="visible" :header="entreprise ? 'Modifier l\'entreprise' : 'Nouvelle entreprise'"
    modal :style="{ width: '32rem' }" @update:visible="emit('update:visible', $event)"
  >
    <div class="field">
      <label>Nom de l'entreprise *</label>
      <InputText v-model="form.nom" class="full" :invalid="!!erreurs.nom" />
      <small v-if="erreurs.nom" class="p-error">{{ erreurs.nom }}</small>
    </div>
    <div class="field">
      <label>Secteur d'activite *</label>
      <InputText v-model="form.secteur_activite" class="full" :invalid="!!erreurs.secteur_activite" />
      <small v-if="erreurs.secteur_activite" class="p-error">{{ erreurs.secteur_activite }}</small>
    </div>
    <div class="row">
      <div class="field" style="flex:1">
        <label>Employes</label>
        <InputNumber v-model="form.nombre_employes" :min="0" class="full" />
      </div>
      <div class="field" style="flex:1">
        <label>Serveurs</label>
        <InputNumber v-model="form.nombre_serveurs" :min="0" class="full" />
      </div>
      <div class="field" style="flex:1">
        <label>Postes clients</label>
        <InputNumber v-model="form.nombre_postes_clients" :min="0" class="full" />
      </div>
    </div>
    <div class="field">
      <label>Services exposes sur Internet</label>
      <MultiSelect
        v-model="form.services_exposes" :options="SERVICES_EXPOSES"
        display="chip" filter placeholder="Selectionner..." class="full"
      />
    </div>

    <template #footer>
      <Button label="Annuler" text severity="secondary" @click="emit('update:visible', false)" />
      <Button :label="entreprise ? 'Enregistrer' : 'Creer'" icon="pi pi-check" @click="soumettre" />
    </template>
  </Dialog>
</template>
