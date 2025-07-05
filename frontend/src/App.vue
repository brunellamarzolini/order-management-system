<script setup>
import Toast from '@/components/common/Toast.vue'
import Card from './components/common/Card.vue'
import OrderList from './views/OrderList.vue'
</script>

<template>
  <div class="app">
    <Toast />

    <div class="container">
      <Card title="Order Management System">
        <OrderList />
      </Card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.filters {
  display: grid;
  grid-template-columns: 120px auto;
  gap: $space-2 $space-3;
  margin-bottom: $space-3;

  .row {
    display: contents;
  }

  .label {
    font-weight: bold;
    text-align: left;
  }

  .value {
    text-align: left;
  }
}
</style>
