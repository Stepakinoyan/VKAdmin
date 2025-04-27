import { createRouter, createWebHistory } from "vue-router";
import FormView from "../views/FormView.vue";
import DashBoard from "../views/DashBoard.vue";
import Help from "../views/Help.vue";
import VueCookies from "vue-cookies";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: FormView,
    },
    {
      path: "/login",
      name: "login",
      component: FormView,
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashBoard,
      meta: { requiresAuth: true },
    },
    {
      path: "/help",
      name: "help",
      component: Help,
      meta: { requiresAuth: true },
    },
  ],
});

export default router;
