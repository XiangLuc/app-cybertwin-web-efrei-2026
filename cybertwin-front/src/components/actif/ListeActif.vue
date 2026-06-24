<script setup>
import { labelTypeActif } from '@/constants/enums'
defineProps({ actifs: { type: Array, default: () => [] }, peutEcrire: { type: Boolean, default: false } })
const emit = defineEmits(['edit', 'delete'])
const severiteType = (t) => ({ SERVEUR_WEB: 'info', BASE_DE_DONNEES: 'warn', POSTE_UTILISATEUR: 'secondary', ROUTEUR: 'contrast', PARE_FEU: 'success', APPLICATION_METIER: 'info' }[t] || 'secondary')
</script>

<template>
  <DataTable :value="actifs" paginator :rows="10" stripedRows removableSort responsiveLayout="scroll">
    <template #empty><div class="empty">Aucun actif pour cette entreprise.</div></template>
    <Column field="nom" header="Nom" sortable />
    <Column header="Type" field="type_actif" sortable>
      <template #body="{ data }"><Tag :value="labelTypeActif(data.type_actif)" :severity="severiteType(data.type_actif)" /></template>
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
