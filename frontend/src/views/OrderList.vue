<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseDropdown from '@/components/common/BaseDropdown.vue'
import BasePagination from '@/components/common/BasePagination.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import { useOrders } from '@/composables/useOrders'
import { useToast } from '@/composables/useToast'
import { debounce } from '@/utils/debounce.ts'

const headers = [
  { key: 'id', label: 'ID', sortable: false },
  { key: 'name', label: 'Name', sortable: false },
  { key: 'description', label: 'Description', sortable: false },
  { key: 'total_amount', label: 'Total Amount', sortable: true },
  { key: 'created_at', label: 'Date', sortable: true },
]

const { orders, loading, error, total, totalPages, fetchOrders } = useOrders()
const { showToast } = useToast()

const page = ref(1)
const perPage = ref('10')
const q = ref('')
const sort = ref('')
const dateFrom = ref('')
const dateTo = ref('')

async function loadOrders() {
  const params: Record<string, unknown> = {
    page: page.value,
    page_size: Number(perPage.value),
  }
  if (q.value) params.search = q.value
  if (dateFrom.value) params.created_at_after = dateFrom.value
  if (dateTo.value) params.created_at_before = dateTo.value
  if (sort.value) {
    const [key, dir] = sort.value.split(':')
    params.ordering = dir === 'desc' ? `-${key}` : key
  }
  try {
    await fetchOrders(params)
  } catch {
    showToast(error.value || 'Failed to fetch orders', 'error')
  }
}

function handleSort({ dir, key }: { dir: string; key: string }) {
  if (key === 'total_amount') {
    key = 'total_amount_db'
  }
  sort.value = `${key}:${dir}`
}

function clearAllFilters() {
  q.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  loadOrders()
}

watch([page, perPage, sort, dateFrom, dateTo], () => {
  loadOrders()
})

// Debounced search
const debouncedLoadOrders = debounce(loadOrders, 400)
watch(q, () => {
  debouncedLoadOrders()
})
onMounted(loadOrders)
</script>

<template>
  <div class="container">
    <BaseCard title="Order List">
      <BaseTable
        v-if="orders"
        :headers="headers"
        :rows="orders"
        :loading="loading"
        @update:sort="handleSort($event)"
        @clear-filters="clearAllFilters"
        showClearFilters
      >
        <template #filters>
          <div class="order-filters-row">
            <div class="order-filters-search">
              <BaseInput
                v-model="q"
                placeholder="Search by id, name or description"
                id="order-search"
                name="order-search"
              />
            </div>
            <div class="order-filters-date">
              <BaseInput
                label="from"
                type="date"
                v-model="dateFrom"
                id="order-date-from"
                name="order-date-from"
              />
            </div>
            <div class="order-filters-date">
              <BaseInput
                label="to"
                type="date"
                v-model="dateTo"
                id="order-date-to"
                name="order-date-to"
              />
            </div>
          </div>
        </template>

        <!-- Row Slot -->
        <template #id="{ row }">
          <router-link :to="{ name: 'order-detail', params: { id: String(row.id) } }">
            {{ row.id }}
          </router-link>
        </template>

        <template #total_amount="{ row }">
          {{ typeof row.total_amount === 'number' ? row.total_amount.toFixed(2) : '0.00' }} €
        </template>

        <template #created_at="{ row }">
          {{
            typeof row.created_at === 'string' ||
            typeof row.created_at === 'number' ||
            row.created_at instanceof Date
              ? new Date(row.created_at).toLocaleString('en-US', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                })
              : ''
          }}
        </template>

        <!-- Footer Slot -->
        <template #footer>
          <div>
            <span v-if="total > 0"> {{ total }} items </span>
            <span v-else> No items found </span>
          </div>
          <BasePagination
            :current-page="page"
            :total-pages="totalPages"
            @update:currentPage="(val) => (page = val)"
          />
          <!-- Per-page -->
          <BaseDropdown
            :options="['10', '20', '50']"
            v-model="perPage"
            :style="{ 'min-width': 'auto' }"
            id="order-per-page"
            name="order-per-page"
          />
        </template>
      </BaseTable>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
.order-filters-row {
  display: flex;
  gap: $space-3;
  align-items: flex-end;
  width: 100%;
  overflow: hidden;

  @media (max-width: $breakpoint-lg) {
    display: grid;
  }
}
.order-filters-search {
  flex: 1 1 0;
  min-width: 0;
}
.order-filters-date {
  flex: 0 1 15%;
}
</style>
