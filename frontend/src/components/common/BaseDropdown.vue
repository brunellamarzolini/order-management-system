<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  label: {
    type: String,
  },
  options: {
    type: Array as () => string[],
    default: () => [],
  },
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Select an option',
  },
  id: {
    type: String,
  },
  name: {
    type: String,
  },
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selectedOption = ref(props.modelValue)
const dropdownRef = ref<HTMLElement | null>(null)

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function selectOption(option: string) {
  if (selectedOption.value === option) {
    // Deselect if clicking the selected option
    selectedOption.value = ''
    emit('update:modelValue', '')
    isOpen.value = false
    return
  }
  selectedOption.value = option
  emit('update:modelValue', option)
  isOpen.value = false
}

function handleClickOutside(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
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
  <div class="base-dropdown" ref="dropdownRef" :id="props.id" :name="props.name">
    <label v-if="props.label" class="base-label">
      {{ label }}
    </label>
    <div class="dropdown-wrapper base-form-field" @click="toggleDropdown">
      <div class="dropdown-selected">
        {{ selectedOption || placeholder }}
      </div>
      <ul v-if="isOpen" class="dropdown-options">
        <li class="dropdown-placeholder" style="color: #888; cursor: default" @click.stop>
          {{ placeholder }}
        </li>
        <li
          v-for="opt in options"
          :key="String(opt)"
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
.base-dropdown {
  position: relative;
  min-width: 200px;

  .dropdown-wrapper {
    position: relative;
    background: white;
    cursor: pointer;

    .dropdown-placeholder {
      padding: $space-1 $space-2;
      font-style: italic;
      pointer-events: none;
      background: none;
    }

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
