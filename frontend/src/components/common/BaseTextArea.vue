<script setup lang="ts">
const props = defineProps({
  modelValue: String,
  placeholder: String,
  label: String,
  id: String,
  name: String,
  rows: Number,
  cols: Number,
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="base-textarea-wrapper">
    <label v-if="props.label" :for="props.id" class="base-label">{{ props.label }}</label>
    <textarea
      :value="props.modelValue"
      @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
      :placeholder="props.placeholder"
      :rows="props.rows"
      :id="props.id"
      :name="props.name"
      class="base-form-field base-textarea"
      :aria-invalid="!!props.error"
      :aria-describedby="props.error ? `${props.id}-error` : undefined"
    />
    <div v-if="props.error" :id="`${props.id}-error`" class="field-msg-error">
      {{ props.error }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.base-textarea-wrapper {
  width: 100%;
}
</style>
