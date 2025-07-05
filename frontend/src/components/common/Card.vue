<script setup>
const props = defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="card">
    <h3 class="card-title" v-if="title">{{ title }}</h3>
    <div class="card-content">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.card {
  background-color: white;
  border-radius: $border-radius-sm;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  padding: $space-3;
  margin-bottom: $space-4;

  .card-title {
    margin: 0 0 $space-3 0;
    font-size: 1.25rem;
    font-weight: bold;
    color: $color-primary;
  }

  .card-content {
    display: flex;
    flex-direction: column;
    gap: $space-3;
  }
}
</style>
