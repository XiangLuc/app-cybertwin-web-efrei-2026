<script setup>
import { ref, watch } from 'vue'
import { NIVEAUX_CRITICITE } from '@/constants/enums'

const LIBELLES_COURANTS = [
  'Logiciel obsolete',
  'Mot de passe faible',
  'Absence de sauvegarde',
  'Certificat SSL expire',
  'Port expose',
  'Injection SQL potentielle',
  'Faille XSS',
  'Acces RDP non restreint',
  'Pare-feu mal configure',
  'Absence de double authentification',
  'Firmware obsolete',
  'Reseau non segmente',
  'Journalisation absente',
]

const suggestions = ref([...LIBELLES_COURANTS])

const props = defineProps({
  visible: { type: Boolean, default: false },
  vulnerabilite: { type: Object, default: null },
  actifs: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:visible', 'submit'])

const form = ref(vide())
const erreurs = ref({})

function vide() {
  return { actif_id: null, libelle: '', criticite: null, description: '' }
}

function filtrer(event) {
  const q = (event.query || '').toLowerCase()
  suggestions.value = LIBELLES_COURANTS.filter((l) => l.toLowerCase().includes(q))
}

watch(
  () => props.visible,
  (ouvert) => {
    if (ouvert) {
      erreurs.value = {}
      form.value = props.vulnerabilite ? { ...props.vulnerabilite } : vide()
    }
  },
)

function valider() {
  const e = {}
  if (!form.value.actif_id) e.actif_id = 'Actif requis'
  if (!form.value.libelle?.trim()) e.libelle = 'Libelle requis'
  if (!form.value.criticite) e.criticite = 'Criticite requise'
  erreurs.value = e
  return Object.keys(e).length === 0
}

function soumettre() {
  if (!valider()) return
  emit('submit', {
    payload: {
      actif_id: form.value.actif_id,
      libelle: form.value.libelle.trim(),
      criticite: form.value.criticite,
      description: form.value.description?.trim() || null,
    },
    edition: !!props.vulnerabilite,
    id: props.vulnerabilite?.id,
  })
}
</script>

<template>
  <Dialog
    :visible="visible" :header="vulnerabilite ? 'Modifier la vulnerabilite' : 'Nouvelle vulnerabilite'"
    modal :style="{ width: '30rem' }" @update:visible="emit('update:visible', $event)"
  >
    <div class="field">
      <label>Actif concerne *</label>
      <Select v-model="form.actif_id" :options="actifs" optionLabel="nom" optionValue="id"
              placeholder="Choisir un actif" class="full" filter :invalid="!!erreurs.actif_id" />
      <small v-if="erreurs.actif_id" class="p-error">{{ erreurs.actif_id }}</small>
    </div>
    <div class="field">
     <div class="champ">
        <label>Libelle *</label>
          <AutoComplete
            v-model="form.libelle"
            :suggestions="suggestions"
            @complete="filtrer"
            dropdown
            completeOnFocus
            forceSelection="false"
            placeholder="Ex : Logiciel obsolete (ou saisissez le votre)"
            class="full"
          />
        </div>
    </div>
    <div class="field">
      <label>Criticite *</label>
      <Select v-model="form.criticite" :options="NIVEAUX_CRITICITE" optionLabel="label" optionValue="value"
              placeholder="Niveau de criticite" class="full" :invalid="!!erreurs.criticite" />
      <small v-if="erreurs.criticite" class="p-error">{{ erreurs.criticite }}</small>
    </div>
    <div class="field">
      <label>Description</label>
      <Textarea v-model="form.description" rows="3" class="full" autoResize />
    </div>

    <template #footer>
      <Button label="Annuler" text severity="secondary" @click="emit('update:visible', false)" />
      <Button :label="vulnerabilite ? 'Enregistrer' : 'Creer'" icon="pi pi-check" @click="soumettre" />
    </template>
  </Dialog>
</template>
