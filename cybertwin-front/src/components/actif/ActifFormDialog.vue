<script setup>
import { ref, watch } from 'vue'
import { TYPES_ACTIF } from '@/constants/enums'

const props = defineProps({
  visible: { type: Boolean, default: false },
  actif: { type: Object, default: null },
  entrepriseId: { type: Number, default: null },
})
const emit = defineEmits(['update:visible', 'submit'])

const form = ref(vide())
const erreurs = ref({})

function vide() {
  return { nom: '', type_actif: null, description: '' }
}

watch(
  () => props.visible,
  (ouvert) => {
    if (ouvert) {
      erreurs.value = {}
      form.value = props.actif ? { ...props.actif } : vide()
    }
  },
)

function valider() {
  const e = {}
  if (!form.value.nom?.trim()) e.nom = 'Nom requis'
  if (!form.value.type_actif) e.type_actif = 'Type requis'
  erreurs.value = e
  return Object.keys(e).length === 0
}

function soumettre() {
  if (!valider()) return
  emit('submit', {
    payload: {
      entreprise_id: props.actif?.entreprise_id ?? props.entrepriseId,
      nom: form.value.nom.trim(),
      type_actif: form.value.type_actif,
      description: form.value.description?.trim() || null,
    },
    edition: !!props.actif,
    id: props.actif?.id,
  })
}
</script>

<template>
  <Dialog
    :visible="visible" :header="actif ? 'Modifier l\'actif' : 'Nouvel actif'"
    modal :style="{ width: '30rem' }" @update:visible="emit('update:visible', $event)"
  >
    <div class="field">
      <label>Nom de l'actif *</label>
      <InputText v-model="form.nom" class="full" :invalid="!!erreurs.nom" />
      <small v-if="erreurs.nom" class="p-error">{{ erreurs.nom }}</small>
    </div>
    <div class="field">
      <label>Type d'actif *</label>
      <Select v-model="form.type_actif" :options="TYPES_ACTIF" optionLabel="label" optionValue="value"
              placeholder="Choisir un type" class="full" :invalid="!!erreurs.type_actif" />
      <small v-if="erreurs.type_actif" class="p-error">{{ erreurs.type_actif }}</small>
    </div>
    <div class="field">
      <label>Description</label>
      <Textarea v-model="form.description" rows="3" class="full" autoResize />
    </div>

    <template #footer>
      <Button label="Annuler" text severity="secondary" @click="emit('update:visible', false)" />
      <Button :label="actif ? 'Enregistrer' : 'Creer'" icon="pi pi-check" @click="soumettre" />
    </template>
  </Dialog>
</template>
