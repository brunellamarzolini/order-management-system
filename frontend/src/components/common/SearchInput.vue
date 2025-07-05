<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Search...',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="search-input-wrapper">
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      type="text"
      :placeholder="placeholder"
      class="search-input"
    />
  </div>
</template>

<style scoped lang="scss">
.search-input-wrapper {
  width: 100%;
}

.search-input {
  width: 100%;
  height: 50px;
  padding: $space-2;
  border: 1px solid $color-border;
  border-radius: $border-radius-sm;
  font-size: $font-size-normal;

  &:focus {
    outline: none;
    //border-color: $color-primary;
  }
}
</style>
