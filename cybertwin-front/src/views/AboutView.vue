<script setup>
import { SOCIETE } from '@/constants/societe'
const valeurs = [
  { icon: 'pi pi-lock', titre: 'Securite par defaut', desc: 'Chiffrement, JWT, mots de passe conformes CNIL et moindre privilege.' },
  { icon: 'pi pi-chart-line', titre: 'Analyse de risque', desc: 'Un moteur transparent qui evalue actifs, vulnerabilites et exposition.' },
  { icon: 'pi pi-users', titre: 'Pense pour les PME', desc: 'Un outil simple et accessible, sans expertise cyber prealable.' },
]
const equipe = [
  { nom: 'PREUVOT Jessy', role: 'Responsable Frontend (Vue.js)' },
  { nom: 'XIANG Luc', role: 'Responsable Backend (Flask)' },
]
</script>

<template>
  <div class="fade-up">
    <div class="panel hero-about">
      <div>
        <Tag value="Entreprise fictive" severity="info" />
        <h1 class="page-title" style="font-size:2rem; margin-top:0.75rem">{{ SOCIETE.nom }}</h1>
        <p class="page-subtitle" style="max-width:640px">
          {{ SOCIETE.nom }} est une jeune entreprise fictive specialisee dans la modelisation
          et l'evaluation du risque cyber pour les PME. Elle edite <strong>{{ SOCIETE.produit }}</strong>.
          {{ SOCIETE.pitch }}
        </p>
      </div>
      <i class="pi pi-shield hero-icon" />
    </div>

    <div class="stat-grid" style="margin-top:1.5rem">
      <div v-for="v in valeurs" :key="v.titre" class="stat-card">
        <i :class="v.icon" style="font-size:1.6rem; color:var(--ct-primary)" />
        <div class="stat-value" style="font-size:1.1rem; margin-top:0.7rem">{{ v.titre }}</div>
        <div class="muted" style="font-size:0.9rem; margin-top:0.25rem">{{ v.desc }}</div>
      </div>
    </div>

    <div class="panel" style="margin-top:1.5rem">
      <h2 style="margin-top:0">Notre equipe</h2>
      <div class="row">
        <div v-for="m in equipe" :key="m.nom" class="membre">
          <Avatar :label="m.nom.charAt(0)" shape="circle" size="large" style="background:var(--ct-primary); color:#fff" />
          <div><div style="font-weight:600">{{ m.nom }}</div><div class="muted" style="font-size:0.85rem">{{ m.role }}</div></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-about { display:flex; align-items:center; justify-content:space-between; gap:1rem; overflow:hidden; background: linear-gradient(120deg, var(--ct-surface), var(--ct-primary-soft)); }
.hero-icon { font-size:7rem; color:var(--ct-primary); opacity:0.18; }
.membre { display:flex; align-items:center; gap:0.75rem; padding:0.75rem 1rem; border:1px solid var(--ct-border); border-radius:0.8rem; }
@media (max-width:700px){ .hero-icon{ display:none; } }
</style>
