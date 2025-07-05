<script setup>
import { ref, watch, onMounted } from 'vue'
import Dropdown from '@/components/common/Dropdown.vue'
import Pagination from '@/components/common/Pagination.vue'
import SearchInput from '@/components/common/SearchInput.vue'
import Table from '@/components/common/Table.vue'
import { ordersApi } from '@/ts/api.ts'

const headers = [
  { key: 'id', label: 'ID', sortable: false },
  { key: 'name', label: 'Name', sortable: false },
  { key: 'description', label: 'Description', sortable: false },
  { key: 'total_amount', label: 'Total Amount', sortable: true },
  { key: 'date', label: 'Date', sortable: true },
]

const orders = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const perPage = ref(10)
const totalPages = ref(1)
const q = ref('')
const sort = ref('')

async function fetchOrders() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: perPage.value,
    }
    if (q.value) params.search = q.value
    if (sort.value) {
      const [key, dir] = sort.value.split(':')
      params.ordering = dir === 'desc' ? `-${key}` : key
    }
    const data = await ordersApi.list(params)
    orders.value = data.results
    total.value = data.count
    totalPages.value = Math.ceil(data.count / perPage.value)
  } finally {
    loading.value = false
  }
}

function handleSort({ dir, key }) {
  console.log(key)
  if (key === 'total_amount') {
    key = 'total_amount_db' // Use the annotated field for total amount
  }
  sort.value = `${key}:${dir}`
}

watch([page, perPage, q, sort], fetchOrders)
onMounted(fetchOrders)
</script>

<template>
  <Table
    v-if="orders"
    :headers="headers"
    :rows="orders"
    :loading="loading"
    @update:sort="handleSort($event)"
  >
    <template #filters>
      <!-- Name search -->
      <SearchInput v-model="q" placeholder="Search by id, name or description" />
    </template>

    <!-- Row Slot -->

    <template #total_amount="{ row }">
      {{ row.total_amount ? row.total_amount.toFixed(2) : '0.00' }} €
    </template>

    <template #date="{ row }">
      {{
        new Date(row.date).toLocaleString('it-IT', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
        })
      }}
    </template>

    <!-- Footer Slot -->
    <template #footer>
      <div>
        <span v-if="total > 0"> {{ total }} items </span>
        <span v-else> No items found </span>
      </div>
      <Pagination
        :current-page="page"
        :total-pages="totalPages"
        @update:currentPage="(val) => (page = val)"
      />
      <!-- Per-page -->
      <Dropdown :options="['10', '20', '50']" v-model="perPage" :style="{ 'min-width': 'auto' }" />
    </template>
  </Table>
</template>

<style scoped lang="scss"></style>
