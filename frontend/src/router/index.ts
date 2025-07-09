import { createRouter, createWebHistory } from 'vue-router'

import OrderList from '@/views/OrderList.vue'
import OrderDetail from '@/views/OrderDetail.vue'
import LoginPage from '@/views/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/',
      redirect: '/orders',
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrderList,
      meta: { requiresAuth: true },
    },
    {
      path: '/orders/:id',
      name: 'order-detail',
      component: OrderDetail,
      props: true,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const access_token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !access_token) {
    next({ name: 'login' })
  } else if (to.name === 'login' && access_token) {
    next({ name: 'orders' })
  } else {
    next()
  }
})

export default router
