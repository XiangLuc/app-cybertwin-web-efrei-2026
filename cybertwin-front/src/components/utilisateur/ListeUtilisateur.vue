<script setup>
import { ROLES_OPTIONS_ADMIN } from '@/constants/enums'
defineProps({ utilisateurs: { type: Array, default: () => [] }, moiId: { type: Number, default: null } })
const emit = defineEmits(['delete', 'change-role'])
const severiteRole = (r) => ({ ADMIN: 'danger', ANALYSTE: 'info', LECTEUR: 'secondary' }[r] || 'secondary')
</script>

<template>
  <DataTable :value="utilisateurs" paginator :rows="10" stripedRows responsiveLayout="scroll">
    <template #empty><div class="empty">Aucun utilisateur.</div></template>
    <Column field="email" header="Email" sortable />
    <Column header="Nom"><template #body="{ data }">{{ [data.prenom, data.nom].filter(Boolean).join(' ') || '—' }}</template></Column>
    <Column header="Role" field="role" sortable style="width:13rem">
      <template #body="{ data }">
        <Select
          v-if="data.id !== moiId"
          :modelValue="data.role" :options="ROLES_OPTIONS_ADMIN" optionLabel="label" optionValue="value"
          @change="emit('change-role', { utilisateur: data, role: $event.value })" style="width:11rem"
        />
        <Tag v-else :value="data.role" :severity="severiteRole(data.role)" v-tooltip.top="'Vous'" />
      </template>
    </Column>
    <Column header="Actions" style="width:6rem">
      <template #body="{ data }">
        <Button icon="pi pi-trash" text rounded severity="danger" :disabled="data.id === moiId"
                @click="emit('delete', data)" v-tooltip.top="'Supprimer'" />
      </template>
    </Column>
  </DataTable>
</template>
