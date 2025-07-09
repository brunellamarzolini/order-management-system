import { ref } from 'vue'
import { productsApi } from '@/ts/api'
import type { Product } from '@/ts/types'

export function useProducts() {
  const products = ref<Product[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProducts(params: Record<string, unknown> = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await productsApi.list(params)
      products.value = data.results
      return data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch products.'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    loading,
    error,
    fetchProducts,
  }
}
