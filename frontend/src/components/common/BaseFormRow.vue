<script setup lang="ts">
const props = defineProps({
  align: {
    type: String,
    default: 'vertical',
  },
  inline: Boolean,
  width: String,
})
const rowStyle = props.width ? { width: props.width } : undefined
</script>

<template>
  <div class="base-form-row" :class="[align, { 'is-inline': inline }]" :style="rowStyle">
    <div class="base-form-slot">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.base-form-row {
  display: flex;
  flex-direction: column;
  gap: $space-1;

  &.is-inline {
    flex-direction: row;
    align-items: center;
  }

  .base-form-slot {
    display: flex;
    gap: $space-3;
  }
}
</style>
