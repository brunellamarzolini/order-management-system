import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isAuthenticated = ref(!!localStorage.getItem('access_token'))

export function useAuth() {
  const router = useRouter()

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    isAuthenticated.value = false
    router.push({ name: 'login' })
  }

  function login(access_token: string, refresh_token: string) {
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    isAuthenticated.value = true
    router.push({ name: 'orders' })
  }

  return {
    isAuthenticated,
    login,
    logout,
  }
}
