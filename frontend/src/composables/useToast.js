import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('error') // available status: ['error', 'success']

export function useToast() {
  function showToast(msg, toastType = 'error', duration = 3000) {
    message.value = msg
    type.value = toastType
    visible.value = true

    setTimeout(() => {
      visible.value = false
    }, duration)
  }

  return {
    visible,
    message,
    type,
    showToast,
  }
}
