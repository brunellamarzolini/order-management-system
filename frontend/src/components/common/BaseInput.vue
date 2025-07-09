<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: String,
  },
  placeholder: {
    type: String,
  },
  type: {
    type: String,
    default: 'text',
  },
  label: {
    type: String,
  },
  id: {
    type: String,
  },
  name: {
    type: String,
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="base-input-wrapper">
    <label v-if="props.label" :for="props.id" class="base-label">{{ props.label }}</label>
    <input
      :type="props.type"
      :value="props.modelValue"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :placeholder="props.placeholder"
      :id="props.id"
      :name="props.name"
      class="base-form-field base-input"
      :aria-invalid="!!props.error"
      :aria-describedby="props.error ? `${props.id}-error` : undefined"
    />
    <div v-if="props.error" :id="`${props.id}-error`" class="field-msg-error">
      {{ props.error }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.base-input-wrapper {
  width: 100%;
}

.base-input-label {
  display: block;
  margin-bottom: $space-1;
  font-size: $font-size-sm;
  color: $color-text;
}
</style>
