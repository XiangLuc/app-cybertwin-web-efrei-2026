<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const LIBELLES = {
  '/': 'Accueil',
  '/tableau-de-bord': 'Tableau de bord',
  '/entreprises': 'Entreprises',
  '/actifs': 'Actifs',
  '/vulnerabilites': 'Vulnerabilites',
  '/comparaison': 'Comparaison',
  '/rapport': 'Rapport',
  '/historique': 'Historique',
  '/profil': 'Profil',
  '/utilisateurs': 'Utilisateurs',
  '/a-propos': 'Qui sommes-nous',
}

function prettify(segment) {
  const s = (segment || '').replace(/-/g, ' ')
  return s.charAt(0).toUpperCase() + s.slice(1)
}

function libelle(r) {
  return r.meta?.titre || LIBELLES[r.path] || prettify(r.path.split('/').pop())
}

const fil = computed(() => {
  const items = [{ label: 'Accueil', to: '/' }]
  route.matched.forEach((r) => {
    if (r.path && r.path !== '/') {
      items.push({ label: libelle(r), to: r.path })
    }
  })
  return items
})

const visible = computed(() => fil.value.length > 1)
</script>

<template>
  <nav v-if="visible" class="fil-ariane" aria-label="Fil d'Ariane">
    <template v-for="(item, i) in fil" :key="item.to">
      <router-link v-if="i < fil.length - 1" :to="item.to" class="fil-lien">
        {{ item.label }}
      </router-link>
      <span v-else class="fil-actuel">{{ item.label }}</span>
      <i v-if="i < fil.length - 1" class="pi pi-angle-right fil-sep" />
    </template>
  </nav>
</template>

<style scoped>
.fil-ariane { display: flex; align-items: center; flex-wrap: wrap; gap: 0.4rem; font-size: 0.85rem; margin-bottom: 1rem; }
.fil-lien { color: var(--ct-muted); text-decoration: none; transition: color 0.15s; }
.fil-lien:hover { color: var(--ct-primary); }
.fil-actuel { color: var(--ct-text); font-weight: 600; }
.fil-sep { font-size: 0.7rem; color: var(--ct-muted); }
</style>