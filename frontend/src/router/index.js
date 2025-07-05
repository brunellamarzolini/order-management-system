import { createRouter, createWebHistory } from 'vue-router'
import OrderList from '@/views/OrderList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: OrderList,
    },
  ],
})

export default router
