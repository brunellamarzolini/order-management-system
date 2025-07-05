<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: false,
  },
  options: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    default: 'all',
  },
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selectedOption = ref(props.modelValue)
const dropdownRef = ref(null)

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function selectOption(option) {
  selectedOption.value = option
  emit('update:modelValue', option)
  isOpen.value = false
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="dropdown" ref="dropdownRef">
    <label>
      {{ label }}
    </label>
    <div class="dropdown-wrapper" @click="toggleDropdown">
      <div class="dropdown-selected">
        {{ selectedOption }}
      </div>
      <ul v-if="isOpen" class="dropdown-options">
        <li
          v-for="opt in options"
          :key="opt"
          :class="{ active: opt === modelValue }"
          @click="selectOption(opt)"
        >
          {{ opt }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
.dropdown {
  position: relative;
  min-width: 200px;
  height: 50px;

  label {
    position: absolute;
    top: -18%;
    background: white;
    font-size: $font-size-sm;
    z-index: 9;
    left: $space-1;
  }

  .dropdown-wrapper {
    position: relative;
    cursor: pointer;
    border: 1px solid $color-border;
    border-radius: $border-radius-sm;
    padding: $space-2;
    background: white;

    .dropdown-selected {
      text-transform: capitalize;
    }

    .dropdown-options {
      position: absolute;
      top: 100%;
      left: 0;
      width: 100%;
      margin: 0;
      padding: 0;
      list-style: none;
      border: 1px solid $color-border;
      border-radius: $border-radius-sm;
      background: white;
      z-index: 10;
      max-height: 300px;
      overflow-y: auto;

      li {
        padding: $space-1 $space-2;
        text-transform: capitalize;
        cursor: pointer;

        &:hover {
          background-color: $color-bg;
        }

        &.active {
          background-color: $color-secondary;
          color: white;
        }
      }
    }
  }
}
</style>
