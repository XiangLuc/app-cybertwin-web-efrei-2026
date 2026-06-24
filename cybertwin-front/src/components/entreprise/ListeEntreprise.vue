<script setup>
defineProps({
  entreprises: { type: Array, default: () => [] },
  peutEcrire: { type: Boolean, default: false },
  selectionId: { type: Number, default: null },
})
const emit = defineEmits(['edit', 'delete', 'select'])
</script>

<template>
  <DataTable :value="entreprises" paginator :rows="10" stripedRows removableSort responsiveLayout="scroll">
    <template #empty><div class="empty">Aucune entreprise. Creez-en une pour commencer.</div></template>
    <Column field="nom" header="Nom" sortable>
      <template #body="{ data }">
        <span style="font-weight:600">{{ data.nom }}</span>
        <Tag v-if="data.id === selectionId" value="active" severity="success" style="margin-left:0.5rem" />
      </template>
    </Column>
    <Column field="secteur_activite" header="Secteur" sortable />
    <Column field="nombre_employes" header="Employes" sortable />
    <Column field="nombre_serveurs" header="Serveurs" sortable />
    <Column field="nombre_postes_clients" header="Postes" sortable />
    <Column header="Services exposes">
      <template #body="{ data }">
        <Tag v-for="s in data.services_exposes" :key="s" :value="s" severity="info" style="margin:2px" />
        <span v-if="!data.services_exposes?.length" class="muted">—</span>
      </template>
    </Column>
    <Column header="Actions" style="width:11rem">
      <template #body="{ data }">
        <Button icon="pi pi-eye" text rounded @click="emit('select', data)" v-tooltip.top="'Activer'" />
        <Button v-if="peutEcrire" icon="pi pi-pencil" text rounded @click="emit('edit', data)" v-tooltip.top="'Modifier'" />
        <Button v-if="peutEcrire" icon="pi pi-trash" text rounded severity="danger" @click="emit('delete', data)" v-tooltip.top="'Supprimer'" />
      </template>
    </Column>
  </DataTable>
</template>
