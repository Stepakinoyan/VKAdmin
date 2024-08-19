import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import DashBoard from '../views/DashBoard.vue';
import VueCookies from 'vue-cookies';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      beforeEnter: (to, from, next) => {
        const token = VueCookies.get('token');
        if (token) {
          next('/dashboard');
        } else {
          next();
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
});

// Охранник маршрутов для проверки авторизации
router.beforeEach((to, from, next) => {
  const token = VueCookies.get('token');
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
