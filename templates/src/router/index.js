import { createRouter, createWebHistory } from 'vue-router';
import Form from '../components/Form.vue';
import DashBoard from '../views/DashBoard.vue';
import Help from '../views/Help.vue';
import VueCookies from 'vue-cookies';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Form,
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
      component: Form
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashBoard,
      meta: { requiresAuth: true }
    },
    {
      path: '/help',
      name: 'help',
      component: Help,
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
