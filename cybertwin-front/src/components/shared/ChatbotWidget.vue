<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useEntrepriseStore } from '@/stores/entreprise.store'
import { analyseService } from '@/services/analyse-service'

/**
 * Chatbot a arbre de decision (sans IA).
 * - Reconnaissance par mots-cles, insensible a la casse et accents.
 * - fais de la navigation sur mot clé ("ouvre le rapport", "va au tableau de bord") :
 * - redirige directement, mais refuse si aucune entreprise n'est selectionnee.
 * - Sinon : indique qu'il ne sait pas.
 */
const router = useRouter()
const entrepriseStore = useEntrepriseStore()

const ouvert = ref(false)
const corps = ref(null)
const saisie = ref('')
const messages = ref([
  { de: 'bot', texte: "Bonjour ! Je suis l'assistant securite de CyberTwin. Posez une question simple ou utilisez les suggestions." },
])

const suggestions = [
  'Donne-moi des recommandations de securite',
  "Affiche les vulnerabilites de l'entreprise",
  'Quel est mon niveau de risque ?',
  'Comment proteger mes mots de passe ?',
  'Ouvre le rapport',
]

function normaliser(texte) {
  return (texte || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
}

function naviguer(route) {
  router.push(route)
  ouvert.value = false
}

const verbesNavigation = ['ouvre', 'ouvrir', 'accede', 'acceder', 'va ', 'aller', 'rendre sur', 'redirige', 'emmene', 'conduis', 'amene']
const ciblesNavigation = [
  { cles: ['rapport', 'pdf'], route: '/rapport', label: 'le rapport' },
  { cles: ['tableau de bord', 'dashboard'], route: '/tableau-de-bord', label: 'le tableau de bord' },
  { cles: ['vulnerabilit'], route: '/vulnerabilites', label: 'les vulnerabilites' },
]
const veutNaviguer = (q) => verbesNavigation.some((v) => q.includes(v))

const intentions = [
  {
    cles: ['recommand', 'conseil', 'bonne pratique'],
    rep: "Bonnes pratiques : 1) Mettre a jour les logiciels. 2) Sauvegardes automatiques (regle 3-2-1). 3) Authentification a deux facteurs. 4) Limiter les services exposes.",
    action: { label: 'Voir le tableau de bord', route: '/tableau-de-bord' },
  },
  {
    cles: ['mot de passe', 'mots de passe', 'password', 'mdp', 'passe'],
    rep: "Mots de passe : au moins 12 caracteres avec majuscule, minuscule, chiffre et caractere special. Un par service, et un gestionnaire de mots de passe.",
  },
  {
    cles: ['rancongiciel', 'ransomware', 'rancon'],
    rep: "Contre les rancongiciels : sauvegardes hors-ligne testees, mises a jour, sensibilisation au phishing et segmentation reseau.",
  },
  {
    cles: ['exposition', 'internet', 'expose', 'port'],
    rep: "Reduisez l'exposition : fermez les ports inutiles, pare-feu, VPN pour les acces distants, et ne publiez que le strict necessaire.",
  },
  {
    cles: ['phishing', 'hameconnage', 'mail frauduleux'],
    rep: "Phishing : verifiez l'expediteur, ne cliquez pas sur les liens douteux, ne donnez jamais vos identifiants par email.",
  },
  {
    cles: ['sauvegarde', 'backup'],
    rep: "Sauvegardes : appliquez la regle 3-2-1 (3 copies, 2 supports, 1 hors-site) et testez regulierement la restauration.",
  },
  {
    cles: ['qui es-tu', 'qui es tu', 'ton nom', 'tu es qui', 'age', 'bonjour', 'salut'],
    rep: "Je suis l'assistant securite de CyberTwin. Je traite uniquement des questions simples de cybersecurite.",
  },
  {
    cles: ['rapport', 'pdf'],
    rep: "Le rapport reprend l'entreprise, ses actifs, ses vulnerabilites, le niveau de risque et les recommandations. Vous pouvez le telecharger en PDF.",
    action: { label: 'Ouvrir le rapport', route: '/rapport' },
  },
]

const messageSansEntreprise = (quoi) =>
  `Je ne peux pas ${quoi} : aucune entreprise n'est selectionnee. Choisissez-en une dans la barre du haut, puis reessayez.`

async function donneesEntreprise(type) {
  const id = entrepriseStore.selectionId
  if (!id) {
    return { texte: messageSansEntreprise(type === 'vulnerabilites' ? 'afficher les vulnerabilites' : 'evaluer le risque') }
  }
  try {
    const d = await analyseService.dashboard(id)
    const nom = entrepriseStore.selection?.nom || 'cette entreprise'
    if (type === 'vulnerabilites') {
      return {
        texte: `${nom} compte ${d.nombre_total_vulnerabilites} vulnerabilite(s) sur ${d.nombre_total_actifs} actif(s).`,
        action: { label: 'Voir les vulnerabilites', route: '/vulnerabilites' },
      }
    }
    return {
      texte: `Niveau de risque de ${nom} : ${d.niveau_risque} (score ${d.score_risque_global}).`,
      action: { label: 'Voir le tableau de bord', route: '/tableau-de-bord' },
    }
  } catch {
    return { texte: 'Impossible de recuperer les donnees pour le moment.' }
  }
}

async function repondre(question) {
  const q = normaliser(question)

  if (veutNaviguer(q)) {
    const cible = ciblesNavigation.find((c) => c.cles.some((k) => q.includes(k)))
    if (cible) {
      if (!entrepriseStore.selectionId) {
        return { texte: messageSansEntreprise(`ouvrir ${cible.label}`) }
      }
      naviguer(cible.route)
      return { texte: `J'ouvre ${cible.label}.` }
    }
  }

  if (
    q.includes('vulnerabilit') &&
    (q.includes('affiche') || q.includes('montre') || q.includes('liste') ||
      q.includes('combien') || q.includes('entreprise'))
  ) {
    return await donneesEntreprise('vulnerabilites')
  }
  if (q.includes('risque') || q.includes('score')) {
    return await donneesEntreprise('risque')
  }

  const trouve = intentions.find((i) => i.cles.some((c) => q.includes(normaliser(c))))
  if (trouve) return { texte: trouve.rep, action: trouve.action }

  return {
    texte: "Desole, je ne sais pas repondre a cela. Je traite uniquement des questions simples de cybersecurite. Essayez une suggestion.",
  }
}

async function envoyer(texte) {
  const message = (texte ?? saisie.value).trim()
  if (!message) return

  messages.value.push({ de: 'user', texte: message })
  saisie.value = ''
  await defiler()

  const reponse = await repondre(message)
  setTimeout(async () => {
    messages.value.push({ de: 'bot', ...reponse })
    await defiler()
  }, 300)
}

async function defiler() {
  await nextTick()
  if (corps.value) corps.value.scrollTop = corps.value.scrollHeight
}
</script>

<template>
  <div class="chatbot">
    <transition name="page">
      <div v-if="ouvert" class="chat-panel">
        <div class="chat-head">
          <div style="display:flex; align-items:center; gap:0.5rem"><i class="pi pi-comments" /> <strong>Assistant securite</strong></div>
          <button class="icon-btn" @click="ouvert = false"><i class="pi pi-times" /></button>
        </div>
        <div ref="corps" class="chat-body">
          <div v-for="(m, i) in messages" :key="i" class="chat-row" :class="m.de">
            <div class="chat-msg" :class="m.de">{{ m.texte }}</div>
            <button v-if="m.action" class="chat-action" @click="naviguer(m.action.route)">
              <i class="pi pi-arrow-right" /> {{ m.action.label }}
            </button>
          </div>
        </div>
        <div class="chat-suggestions">
          <button v-for="s in suggestions" :key="s" class="chip" @click="envoyer(s)">{{ s }}</button>
        </div>
        <div class="chat-input">
          <InputText v-model="saisie" class="full" placeholder="Votre question..." @keyup.enter="envoyer()" />
          <Button icon="pi pi-send" @click="envoyer()" />
        </div>
      </div>
    </transition>
    <button class="chat-fab" @click="ouvert = !ouvert" v-tooltip.left="'Assistant securite'">
      <i :class="ouvert ? 'pi pi-times' : 'pi pi-comments'" />
    </button>
  </div>
</template>

<style scoped>
.chatbot { position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 60; }
.chat-fab { width: 56px; height: 56px; border-radius: 50%; border: none; cursor: pointer; background: var(--ct-primary); color: #fff; font-size: 1.3rem; box-shadow: 0 10px 24px -8px var(--ct-primary); transition: transform 0.15s; }
.chat-fab:hover { transform: scale(1.06); }
.chat-panel { position: absolute; bottom: 70px; right: 0; width: 350px; max-width: 86vw; height: 480px; background: var(--ct-surface); border: 1px solid var(--ct-border); border-radius: 1rem; box-shadow: var(--ct-shadow); display: flex; flex-direction: column; overflow: hidden; }
.chat-head { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; border-bottom: 1px solid var(--ct-border); background: var(--ct-surface-2); }
.chat-body { flex: 1; overflow-y: auto; padding: 0.9rem; display: flex; flex-direction: column; gap: 0.6rem; }
.chat-row { display: flex; flex-direction: column; gap: 0.3rem; }
.chat-row.user { align-items: flex-end; }
.chat-row.bot { align-items: flex-start; }
.chat-msg { padding: 0.6rem 0.8rem; border-radius: 0.8rem; font-size: 0.88rem; line-height: 1.4; max-width: 85%; }
.chat-msg.bot { background: var(--ct-surface-2); border-bottom-left-radius: 0.2rem; }
.chat-msg.user { background: var(--ct-primary); color: #fff; border-bottom-right-radius: 0.2rem; }
.chat-action { align-self: flex-start; display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; padding: 0.35rem 0.7rem; border-radius: 0.6rem; border: 1px solid var(--ct-primary); background: var(--ct-primary-soft); color: var(--ct-primary); cursor: pointer; }
.chat-action:hover { background: var(--ct-primary); color: #fff; }
.chat-suggestions { display: flex; flex-wrap: wrap; gap: 0.35rem; padding: 0 0.75rem 0.5rem; }
.chip { font-size: 0.72rem; padding: 0.3rem 0.55rem; border-radius: 1rem; border: 1px solid var(--ct-border); background: transparent; color: var(--ct-muted); cursor: pointer; }
.chip:hover { border-color: var(--ct-primary); color: var(--ct-text); }
.chat-input { display: flex; gap: 0.4rem; padding: 0.6rem; border-top: 1px solid var(--ct-border); }
</style>