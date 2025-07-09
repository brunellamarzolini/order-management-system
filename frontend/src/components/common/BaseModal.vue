<script setup lang="ts">
import BaseButton from './BaseButton.vue'

defineProps<{
  modelValue: boolean
  title?: string
  customClass?: string
}>()
const emit = defineEmits(['update:modelValue', 'confirm'])
function close() {
  emit('update:modelValue', false)
}
</script>

<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div :class="['modal-content', customClass]" role="dialog" aria-modal="true">
      <header v-if="title" class="modal-header">
        <h3>{{ title }}</h3>
      </header>
      <div class="modal-body">
        <slot />
      </div>
      <footer class="modal-footer">
        <slot name="footer">
          <BaseButton class="btn-secondary" @click="close">Cancel</BaseButton>
          <BaseButton class="btn-primary" @click="$emit('confirm')">Confirm</BaseButton>
        </slot>
      </footer>
    </div>
  </div>
</template>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #fff;
  border-radius: $border-radius-sm;
  min-width: 320px;
  max-width: 90vw;
  padding: $space-3;
  box-shadow: $shadow-sm;

  &.modal-lg {
    width: 680px;

    @media (max-width: $breakpoint-lg) {
      width: 100%;
    }
  }
}
.modal-header {
  margin-bottom: $space-3;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: $space-3;
  margin-top: $space-3;
}
</style>
