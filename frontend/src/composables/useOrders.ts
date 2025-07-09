import { ref } from 'vue'
import { ordersApi } from '@/ts/api'
import type { Order } from '@/ts/types'

export function useOrders() {
  const orders = ref<Order[]>([])
  const order = ref<Order | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const total = ref(0)
  const totalPages = ref(1)

  async function fetchOrders(params: Record<string, unknown> = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await ordersApi.list(params)
      orders.value = data.results
      total.value = data.count
      const pageSize =
        typeof params.page_size === 'number' ? params.page_size : Number(params.page_size) || 10
      totalPages.value = Math.ceil(data.count / pageSize)
      return data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch orders.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchOrder(id: string) {
    loading.value = true
    error.value = null
    try {
      order.value = await ordersApi.retrieve(id)
      return order.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch order.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateOrder(id: string, data: Partial<Order>) {
    loading.value = true
    error.value = null
    try {
      const updated = await ordersApi.update(id, data)
      order.value = { ...order.value, ...updated } as Order
      return updated
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update order.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteOrder(id: string) {
    loading.value = true
    error.value = null
    try {
      await ordersApi.delete(id)
      order.value = null
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete order.'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    orders,
    order,
    loading,
    error,
    total,
    totalPages,
    fetchOrders,
    fetchOrder,
    updateOrder,
    deleteOrder,
  }
}
