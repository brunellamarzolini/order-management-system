<script setup lang="ts">
import BaseToast from '@/components/common/BaseToast.vue'
import { useAuth } from '@/composables/useAuth'
import BaseButton from './components/common/BaseButton.vue'

const { isAuthenticated, logout } = useAuth()
</script>

<template>
  <div class="app">
    <BaseToast />
    <header v-if="isAuthenticated">
      <nav style="display: flex; justify-content: flex-end; padding: 1rem">
        <BaseButton @click="logout" class="btn-primary">Logout</BaseButton>
      </nav>
    </header>
    <router-view />
  </div>
</template>
