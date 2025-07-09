import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('error') // available status: ['error', 'success']

export function useToast() {
  type ToastType = 'error' | 'success'

  function showToast(msg: string, toastType: ToastType = 'error', duration: number = 3000): void {
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
