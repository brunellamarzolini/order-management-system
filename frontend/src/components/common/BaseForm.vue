<script setup lang="ts">
import { useSlots } from 'vue'
const emit = defineEmits(['submit'])
defineProps({
  loading: Boolean,
})
function onSubmit() {
  emit('submit')
}

const slots = useSlots()
</script>

<template>
  <form @submit.prevent="onSubmit" class="base-form">
    <div v-if="slots.actions" class="form-actions">
      <slot name="actions" />
    </div>
    <div v-if="loading">Loading...</div>
    <div class="form-fields">
      <slot />
    </div>
  </form>
</template>

<style scoped lang="scss">
.base-form {
  display: flex;
  flex-direction: column;
  gap: $space-4;
}
.form-fields {
  display: flex;
  flex-direction: column;
  gap: $space-3;
}
.form-actions {
  display: flex;
  gap: $space-3;
  align-self: self-end;
}
</style>
