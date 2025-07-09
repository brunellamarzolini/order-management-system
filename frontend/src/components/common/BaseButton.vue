<script setup lang="ts">
defineProps<{
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  customClass?: string
}>()
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="['btn', customClass, { loading }]"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner" />
    <slot />
  </button>
</template>

<style scoped lang="scss">
.spinner {
  width: 1em;
  height: 1em;
  border: 2px solid #fff;
  border-top: 2px solid #888;
  border-radius: 50%;
  margin-right: 0.5em;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
