<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useNotificationStore } from '@/stores/notification.store'
import { httpEvents } from '@/services/http-client'

const notif = useNotificationStore()
const op = ref()

function onMutation() { notif.rafraichirCompteur() }
onMounted(() => {
  notif.demarrerPolling()
  httpEvents.addEventListener('mutation', onMutation)
})
onUnmounted(() => {
  notif.arreterPolling()
  httpEvents.removeEventListener('mutation', onMutation)
})

function ouvrir(e) {
  // Ouvrir le Popover SYNCHRONIQUEMENT avec l'evenement frais (sinon
  // event.currentTarget devient null apres un await et le positionnement casse).
  op.value.toggle(e)
  notif.charger()
}

const icone = (type) => ({ ALERTE: 'pi-exclamation-triangle', SUCCES: 'pi-check-circle', INFO: 'pi-info-circle' }[type] || 'pi-bell')
const couleur = (type) => ({ ALERTE: '#ef4444', SUCCES: '#22c55e', INFO: 'var(--ct-primary)' }[type] || 'var(--ct-muted)')

function tempsRelatif(iso) {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000
  if (diff < 60) return "a l'instant"
  if (diff < 3600) return `il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `il y a ${Math.floor(diff / 3600)} h`
  return `il y a ${Math.floor(diff / 86400)} j`
}
</script>

<template>
  <button class="icon-btn bell" @click="ouvrir" v-tooltip.bottom="'Notifications'">
    <i class="pi pi-bell" />
    <span v-if="notif.count" class="bell-badge">{{ notif.count > 9 ? '9+' : notif.count }}</span>
  </button>

  <Popover ref="op">
    <div class="notif-panel">
      <div class="notif-head">
        <strong>Notifications</strong>
        <button v-if="notif.items.some((n) => !n.lu)" class="lien-action" @click="notif.marquerToutesLues()">
          Tout marquer comme lu
        </button>
      </div>

      <div v-if="notif.chargement" class="notif-empty">Chargement...</div>
      <div v-else-if="!notif.items.length" class="notif-empty">
        <i class="pi pi-inbox" style="font-size:1.6rem; display:block; margin-bottom:0.5rem" />
        Aucune notification
      </div>

      <div v-else class="notif-list">
        <div v-for="n in notif.items" :key="n.id" class="notif-item" :class="{ nonlu: !n.lu }">
          <i class="pi" :class="icone(n.type)" :style="{ color: couleur(n.type) }" />
          <div class="notif-body" @click="notif.marquerLue(n.id)">
            <div class="notif-titre">{{ n.titre }}</div>
            <div class="notif-message">{{ n.message }}</div>
            <div class="notif-temps">{{ tempsRelatif(n.created_at) }}</div>
          </div>
          <button class="icon-btn small" @click="notif.supprimer(n.id)" v-tooltip.left="'Supprimer'">
            <i class="pi pi-times" />
          </button>
        </div>
      </div>
    </div>
  </Popover>
</template>

<style scoped>
.bell { position: relative; }
.bell-badge { position: absolute; top: 2px; right: 2px; min-width: 17px; height: 17px; padding: 0 4px;
  border-radius: 9px; background: #ef4444; color: #fff; font-size: 0.65rem; font-weight: 700;
  display: grid; place-items: center; line-height: 1; }
.notif-panel { width: 340px; max-width: 86vw; }
.notif-head { display: flex; align-items: center; justify-content: space-between; padding-bottom: 0.6rem; margin-bottom: 0.4rem; border-bottom: 1px solid var(--ct-border); }
.lien-action { background: none; border: none; color: var(--ct-primary); cursor: pointer; font-size: 0.78rem; }
.notif-empty { text-align: center; color: var(--ct-muted); padding: 1.5rem 0; }
.notif-list { max-height: 360px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.2rem; }
.notif-item { display: flex; gap: 0.6rem; align-items: flex-start; padding: 0.6rem 0.4rem; border-radius: 0.6rem; transition: background 0.15s; }
.notif-item:hover { background: var(--ct-surface-2); }
.notif-item.nonlu { background: var(--ct-primary-soft); }
.notif-body { flex: 1; cursor: pointer; min-width: 0; }
.notif-titre { font-weight: 600; font-size: 0.88rem; }
.notif-message { font-size: 0.8rem; color: var(--ct-muted); }
.notif-temps { font-size: 0.7rem; color: var(--ct-muted); margin-top: 0.15rem; }
.icon-btn.small { width: 28px; height: 28px; }
</style>
