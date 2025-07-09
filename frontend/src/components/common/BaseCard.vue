<script setup lang="ts">
defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="card">
    <div class="card-title" v-if="title">{{ title }}</div>
    <div class="card-content">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.card {
  width: 100%;
  background-color: white;
  border-radius: $border-radius-sm;
  box-shadow: $shadow-sm;
  padding: $space-3;

  .card-title {
    //margin: 0 0 $space-3 0;
    font-size: $font-size-md;
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
