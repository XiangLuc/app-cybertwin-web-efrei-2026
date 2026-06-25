<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { authService } from '@/services/auth-service'
import { useAuthStore } from '@/stores/auth.store'
import { messageErreur } from '@/services/http-client'
import ListeUtilisateur from '@/components/utilisateur/ListeUtilisateur.vue'
import UtilisateurFormDialog from '@/components/utilisateur/UtilisateurFormDialog.vue'

const auth = useAuthStore()
const toast = useToast()
const confirm = useConfirm()
const users = ref([])
const chargement = ref(true)
const dialogVisible = ref(false)

onMounted(charger)
async function charger() {
  chargement.value = true
  try { users.value = await authService.listUsers() }
  catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }) }
  finally { chargement.value = false }
}
function onSubmit({ payload }) { executer(authService.createUser(payload), 'Utilisateur cree.') }

function changerRole({ utilisateur, role }) {
  if (role === utilisateur.role) return
  confirm.require({
    header: 'Confirmer le changement de role',
    message: `Attribuer le role ${role} a "${utilisateur.email}" ?`,
    icon: 'pi pi-user-edit', acceptLabel: 'Confirmer', rejectLabel: 'Annuler',
    accept: () => executer(authService.changeRole(utilisateur.id, role), 'Role mis a jour.'),
    reject: charger, // restaure l'affichage si annule
  })
}

function supprimer(u) {
  confirm.require({
    header: 'Confirmer la suppression', message: `Supprimer l'utilisateur "${u.email}" ?`,
    icon: 'pi pi-exclamation-triangle', acceptLabel: 'Supprimer', rejectLabel: 'Annuler', acceptClass: 'p-button-danger',
    accept: () => executer(authService.deleteUser(u.id), 'Utilisateur supprime.'),
  })
}
async function executer(promesse, succes) {
  try { await promesse; dialogVisible.value = false
    toast.add({ severity: 'success', summary: 'Succes', detail: succes, life: 2500 }); await charger()
  } catch (e) { toast.add({ severity: 'error', summary: 'Erreur', detail: messageErreur(e), life: 4000 }); await charger() }
}
</script>

<template>
  <div class="fade-up">
    <div class="page-header">
      <div>
        <h1 class="page-title">Utilisateurs</h1>
        <p class="page-subtitle">Gestion des comptes et des roles (administrateurs uniquement).</p>
      </div>
      <Button label="Nouvel utilisateur" icon="pi pi-user-plus" @click="dialogVisible = true" />
    </div>

    <div v-if="chargement" class="spinner-wrap"><ProgressSpinner /></div>
    <div v-else class="panel">
      <ListeUtilisateur :utilisateurs="users" :moiId="auth.user?.id" @delete="supprimer" @change-role="changerRole" />
    </div>

    <UtilisateurFormDialog v-model:visible="dialogVisible" @submit="onSubmit" />
  </div>
</template>
