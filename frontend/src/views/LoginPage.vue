<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseForm from '@/components/common/BaseForm.vue'
import BaseFormRow from '@/components/common/BaseFormRow.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import api from '@/ts/api'

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)
const { login } = useAuth()

const onSubmit = async () => {
  error.value = null
  if (!username.value || !password.value) {
    error.value = 'Username and password are required.'
    return
  }
  loading.value = true
  try {
    const res = await api.post('/auth/login/', {
      username: username.value,
      password: password.value,
    })
    const access_token = res.data?.access
    const refresh_token = res.data?.refresh

    if (access_token && refresh_token) {
      login(access_token, refresh_token)
    } else {
      error.value = 'Invalid response from server.'
    }
  } catch {
    error.value = 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <BaseForm @submit="onSubmit" class="login-form">
    <h2>Login</h2>

    <BaseFormRow>
      <BaseInput
        v-model="username"
        id="username"
        name="username"
        label="Username"
        :error="error && !username ? 'Username is required' : ''"
        required
      />
    </BaseFormRow>
    <BaseFormRow>
      <BaseInput
        v-model="password"
        id="password"
        name="password"
        label="Password"
        type="password"
        :error="error && !password ? 'Password is required' : ''"
        required
      />
    </BaseFormRow>
    <div class="form-actions">
      <BaseButton type="submit" :loading="loading" class="btn btn-primary">Login</BaseButton>
      <span v-if="error" class="error">{{ error }}</span>
    </div>
  </BaseForm>
</template>

<style scoped lang="scss">
.login-form {
  max-width: 400px;
  margin: $space-5 auto;
  padding: $space-5;
  border: 1px solid #eee;
  border-radius: $border-radius-md;
  background: #fff;
}
.form-actions {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: $space-1;
}
.error {
  color: $color-error;
  font-size: $font-size-sm;
}
</style>
