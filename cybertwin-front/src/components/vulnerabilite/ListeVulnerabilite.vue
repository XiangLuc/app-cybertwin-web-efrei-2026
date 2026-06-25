<script setup>
import { labelCriticite } from '@/constants/enums'
defineProps({
  vulnerabilites: { type: Array, default: () => [] },
  actifs: { type: Array, default: () => [] },
  peutEcrire: { type: Boolean, default: false },
})
const emit = defineEmits(['edit', 'delete'])
const nomActif = (id, actifs) => actifs.find((a) => a.id === id)?.nom || `#${id}`
const severiteCriticite = (c) => ({ FAIBLE: 'success', MOYENNE: 'warn', ELEVEE: 'danger', CRITIQUE: 'danger' }[c] || 'secondary')
</script>

<template>
  <DataTable :value="vulnerabilites" paginator :rows="10" stripedRows removableSort responsiveLayout="scroll">
    <template #empty><div class="empty">Aucune vulnerabilite enregistree.</div></template>
    <Column field="libelle" header="Libelle" sortable />
    <Column header="Actif"><template #body="{ data }">{{ nomActif(data.actif_id, actifs) }}</template></Column>
    <Column header="Criticite" field="criticite" sortable>
      <template #body="{ data }"><Tag :value="labelCriticite(data.criticite)" :severity="severiteCriticite(data.criticite)" /></template>
    </Column>
    <Column field="description" header="Description">
      <template #body="{ data }"><span :class="{ muted: !data.description }">{{ data.description || '—' }}</span></template>
    </Column>
    <Column v-if="peutEcrire" header="Actions" style="width:8rem">
      <template #body="{ data }">
        <Button icon="pi pi-pencil" text rounded @click="emit('edit', data)" v-tooltip.top="'Modifier'" />
        <Button icon="pi pi-trash" text rounded severity="danger" @click="emit('delete', data)" v-tooltip.top="'Supprimer'" />
      </template>
    </Column>
  </DataTable>
</template>
