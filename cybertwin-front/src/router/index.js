import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { ROLES } from '@/constants/enums'

import MainLayout from '@/layout/MainLayout.vue'
import AuthLayout from '@/layout/AuthLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', name: 'home', component: () => import('@/views/HomeView.vue') },
      { path: 'a-propos', name: 'a-propos', component: () => import('@/views/AboutView.vue') },
      { path: 'entreprises', name: 'entreprises', component: () => import('@/views/EntreprisesView.vue') },
      { path: 'actifs', name: 'actifs', component: () => import('@/views/ActifsView.vue') },
      { path: 'vulnerabilites', name: 'vulnerabilites', component: () => import('@/views/VulnerabilitesView.vue') },
      { path: 'tableau-de-bord', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'comparaison', name: 'comparaison', component: () => import('@/views/ComparaisonView.vue') },
      { path: 'rapport', name: 'rapport', component: () => import('@/views/RapportView.vue') },
      { path: 'historique', name: 'historique', component: () => import('@/views/HistoriqueView.vue') },
      { path: 'profil', name: 'profil', component: () => import('@/views/ProfileView.vue') },
      {
        path: 'utilisateurs',
        name: 'utilisateurs',
        component: () => import('@/views/UsersView.vue'),
        meta: { roles: [ROLES.ADMIN] },
      },
    ],
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      { path: 'login', name: 'login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
      { path: 'register', name: 'register', component: () => import('@/views/RegisterView.vue'), meta: { public: true } },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue'), meta: { public: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.public) {
    if (auth.estConnecte && (to.name === 'login' || to.name === 'register')) {
      return { name: 'home' }
    }
    return true
  }

  if (!auth.estConnecte) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.role)) {
    return { name: 'home' }
  }

  return true
})

export default router
