import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashBoard from '../views/DashBoard.vue'
import VueCookies from 'vue-cookies'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      beforeEnter: (to, from, next) => {
        const token = VueCookies.get('token');
        if (token) {
          next('/dashboard');
        } else {
          next('/login');
        }
      }
    },
    {
      path: '/login',
      name: 'login',
      component: HomeView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashBoard,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = VueCookies.get('token');
    if (token) {
      next();
    } else {
      next('/login');
    }
  } else {
    next();
  }
})

export default router