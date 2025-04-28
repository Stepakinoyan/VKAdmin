import { createRouter, createWebHistory } from "vue-router";
import FormView from "../views/FormView.vue";
import DashBoard from "../views/DashBoardView.vue";
import HelpView from "../views/HelpView.vue";

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
    },
    {
      path: "/help",
      name: "help",
      component: HelpView,
    },
  ],
});

export default router;
