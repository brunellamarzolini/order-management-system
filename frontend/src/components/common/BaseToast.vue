<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const { visible, message, type } = useToast()
</script>

<template>
  <div v-if="visible" class="toast" :class="type">
    {{ message }}
  </div>
</template>

<style lang="scss" scoped>
.toast {
  position: fixed;
  bottom: $space-3;
  right: $space-3;
  padding: $space-2 $space-3;
  border-radius: $border-radius-sm;
  color: #fff;
  font-weight: bold;
  z-index: 1000;
}
.toast.error {
  background-color: $color-error;
}
.toast.success {
  background-color: $color-success;
}
</style>
