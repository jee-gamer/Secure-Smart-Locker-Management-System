import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import LockersView from '../views/LockersView.vue'
import AdminLogsView from '../views/AdminLogsView.vue'

const routes = [
  { path: '/', redirect: '/lockers' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  {
    path: '/lockers',
    component: LockersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/logs',
    component: AdminLogsView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
