<script setup>
import { ref } from 'vue'

const props = defineProps({
  headers: {
    type: Array,
    required: true,
  },
  rows: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const sortKey = ref(null)
const sortOrder = ref('asc')

const emit = defineEmits(['update:sort'])

function sort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }

  emit('update:sort', { key: sortKey.value, dir: sortOrder.value })
}

function getSortClass(key) {
  if (sortKey.value === key) {
    return sortOrder.value === 'asc' ? 'icon-sort-asc' : 'icon-sort-desc'
  }
  return 'icon-sort'
}
</script>

<template>
  <div class="table">
    <div class="table-filters">
      <slot name="filters" />
    </div>

    <div class="table-wrapper">
      <div v-if="loading" class="overlay">
        <div class="spinner">Loading…</div>
      </div>

      <table>
        <thead>
          <tr>
            <th
              v-for="header in headers"
              :key="header.key"
              @click="header.sortable && sort(header.key)"
            >
              {{ header.label }}
              <span v-if="header.sortable" :class="getSortClass(header.key)"></span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td v-for="header in headers" :key="header.key">
              <slot :name="header.key" :row="row">{{ row[header.key] }}</slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.table {
  .table-filters {
    display: flex;
    align-items: center;
    gap: $space-3;
    margin-bottom: $space-3;

    @media (max-width: $breakpoint-lg) {
      display: grid;
    }
  }

  .table-wrapper {
    position: relative;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;

    table {
      width: 100%;
      border-collapse: collapse;
      th,
      td {
        padding: $space-2;
        border: 1px solid $color-border;
      }
      th {
        text-align: left;
        background: $color-secondary;
        color: white;
      }
    }

    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(255, 255, 255, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
    }

    .spinner {
      padding: $space-3 $space-4;
      background: white;
      border: 1px solid $color-primary;
      border-radius: $border-radius-sm;
      font-weight: bold;
    }

    .no-results {
      text-align: center;
      padding: $space-3;
      color: $color-text;
    }
  }

  .table-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: $space-3;
  }

  .icon-sort::after {
    content: '⇅';
  }

  .icon-sort-asc::after {
    content: '↑';
  }

  .icon-sort-desc::after {
    content: '↓';
  }
}
</style>
