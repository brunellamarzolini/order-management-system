<script setup>
const props = defineProps({
  totalPages: {
    type: Number,
    required: true,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
  currentPage: {
    type: Number,
    default: 1,
  },
})

const emit = defineEmits(['update:currentPage'])

function go(page) {
  if (page >= 1 && page <= props.totalPages) {
    emit('update:currentPage', page)
  }
}
</script>

<template>
  <nav class="pagination">
    <button @click="go(currentPage - 1)" :disabled="currentPage <= 1">Prev</button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button @click="go(currentPage + 1)" :disabled="currentPage >= totalPages">Next</button>
  </nav>
</template>

<style scoped lang="scss">
.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: $space-2;

  button {
    padding: $space-1 $space-2;
    border: none;
    background: $color-primary;
    color: white;
    border-radius: $border-radius-sm;
    cursor: pointer;

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}
</style>
