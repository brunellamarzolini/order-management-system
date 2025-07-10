<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseTextArea from '@/components/common/BaseTextArea.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseForm from '@/components/common/BaseForm.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFormRow from '@/components/common/BaseFormRow.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useOrders } from '@/composables/useOrders'
import { useProducts } from '@/composables/useProducts'
import { debounce } from '@/utils/debounce.ts'
import Multiselect from 'vue-multiselect'
import { useToast } from '@/composables/useToast'
import { useDiff } from '@/composables/useDiff'
import type { Order, Product } from '@/ts/types'
import BaseDropdown from '@/components/common/BaseDropdown.vue'

const showAddProductModal = ref(false)
const showRemoveAllProductsModal = ref(false)
const addProductSelected = ref<Product[]>([])
const addProductSearch = ref('')
const {
  products: searchProducts,
  loading: searchProductsLoading,
  error: searchProductsError,
  fetchProducts,
} = useProducts()

const route = useRoute()
const router = useRouter()
const orderId = route.params.id as string

const { order, loading, error, fetchOrder, updateOrder, deleteOrder } = useOrders()
const { hasDiff } = useDiff()
const { showToast } = useToast()

const productHeaders = [
  { key: 'select', label: '', sortable: false },
  { key: 'id', label: 'ID', sortable: false },
  { key: 'name', label: 'Name', sortable: false },
  { key: 'price', label: 'Price', sortable: false },
]

const productSearch = ref('')
const selectedProductIds = ref<string[]>([])
const selectAll = ref(false)
const bulkAction = ref('')
const showBulkDeleteModal = ref(false)

const filteredProducts = computed(() => {
  if (!editableOrder.value?.product_details) return []
  const q = productSearch.value.trim().toLowerCase()
  if (!q) return editableOrder.value.product_details
  return editableOrder.value.product_details.filter((p) => {
    return (
      (p.name && p.name.toLowerCase().includes(q)) ||
      (p.id && String(p.id).toLowerCase().includes(q))
    )
  })
})

function toggleSelectAll() {
  if (!editableOrder.value) return
  if (selectAll.value) {
    selectedProductIds.value = editableOrder.value.product_details?.map((p) => p.id) || []
  } else {
    selectedProductIds.value = []
  }
}

function toggleProductSelection(id: string) {
  if (selectedProductIds.value.includes(id)) {
    selectedProductIds.value = selectedProductIds.value.filter((pid) => pid !== id)
  } else {
    selectedProductIds.value.push(id)
  }
}

watch(
  selectedProductIds,
  (val) => {
    if (!editableOrder.value) return
    selectAll.value =
      !!editableOrder.value.product_details &&
      val.length === (editableOrder.value.product_details?.length || 0)
  },
  { deep: true },
)

function handleBulkActionConfirm() {
  if (bulkAction.value === 'delete' && selectedProductIds.value.length) {
    showBulkDeleteModal.value = true
  }
}

function confirmBulkDelete() {
  if (!editableOrder.value) return
  editableOrder.value.product_details =
    editableOrder.value.product_details?.filter((p) => !selectedProductIds.value.includes(p.id)) ||
    []
  selectedProductIds.value = []
  showBulkDeleteModal.value = false
}

const editableOrder = ref<Order | null>(null)
function isOrderChanged() {
  return hasDiff(editableOrder.value, order.value)
}

onMounted(async () => {
  await fetchOrder(orderId)
  if (order.value) {
    editableOrder.value = JSON.parse(JSON.stringify(order.value))
  }
})

watch(order, (val) => {
  if (val) {
    editableOrder.value = JSON.parse(JSON.stringify(val))
  }
})

async function handleUpdate() {
  if (!order.value || !editableOrder.value) return
  // Check if all products are being removed
  const originalProducts = order.value.product_details || []
  const newProducts = editableOrder.value.product_details || []
  if (originalProducts.length > 0 && newProducts.length === 0) {
    showRemoveAllProductsModal.value = true
    return
  }
  await doUpdateOrder()
}

async function doUpdateOrder() {
  if (!order.value || !editableOrder.value) return
  try {
    await updateOrder(order.value.id, {
      name: editableOrder.value.name,
      description: editableOrder.value.description,
      products: editableOrder.value.product_details?.map((p) => p.id) || [],
    })
    await fetchOrder(orderId)
    if (order.value) {
      editableOrder.value = JSON.parse(JSON.stringify(order.value))
    }
    showToast('Order updated successfully', 'success')
  } catch {
    showToast(error.value || 'Failed to update order', 'error')
  }
  showRemoveAllProductsModal.value = false
}

const showDeleteModal = ref(false)
function openDeleteModal() {
  showDeleteModal.value = true
}
async function confirmDelete() {
  if (!order.value) return
  try {
    await deleteOrder(order.value.id)
    showToast('Order deleted successfully', 'success')
    router.push('/orders')
  } catch {
    showToast(error.value || 'Failed to delete order', 'error')
  } finally {
    showDeleteModal.value = false
  }
}

const missingRequiredFields = ref(false)
watch(
  editableOrder,
  (val) => {
    missingRequiredFields.value = !val || !val.name
  },
  { deep: true },
)

const debouncedFetchProducts = debounce((...args: unknown[]) => {
  const q = args[0] as string
  fetchProducts({ search: q })
}, 400)

function onProductSearchChange(q: string) {
  addProductSearch.value = q
  debouncedFetchProducts(q)
}

function openAddProductModal() {
  showAddProductModal.value = true
  addProductSearch.value = ''
  fetchProducts()
}

function addSelectedProductsToOrder() {
  if (!editableOrder.value) return
  editableOrder.value.product_details = [
    ...(editableOrder.value.product_details || []),
    ...addProductSelected.value,
  ]
  addProductSelected.value = []
  showAddProductModal.value = false
}

const newTotalAmount = ref('0.00')
watch(
  () => editableOrder.value?.product_details,
  (productDetails) => {
    if (!productDetails) {
      newTotalAmount.value = '0.00'
      return
    }
    const sum = productDetails.reduce((acc, p) => acc + (Number(p.price) || 0), 0)
    newTotalAmount.value = sum.toFixed(2)
  },
  { deep: true, immediate: true },
)

const isProductsChanged = computed(() => {
  if (!editableOrder.value || !order.value) return false
  const a = (editableOrder.value.product_details || []).map((p) => p.id).sort()
  const b = (order.value.product_details || []).map((p) => p.id).sort()
  if (a.length !== b.length) return true
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return true
  }
  return false
})
</script>

<template>
  <div class="container">
    <BaseCard title="Order Detail">
      <BaseBreadcrumbs :items="[{ label: 'Orders', route: '/orders' }, { label: orderId }]" />
      <div v-if="loading">Loading...</div>
      <div v-else-if="editableOrder">
        <BaseForm :loading="loading" @submit="handleUpdate">
          <template #actions>
            <BaseButton
              type="submit"
              class="btn-primary"
              :disabled="!isOrderChanged() || missingRequiredFields"
            >
              Update
            </BaseButton>
          </template>
          <BaseFormRow>
            <BaseInput
              v-model="editableOrder.name"
              label="Name *"
              id="order-name"
              name="order-name"
              :error="!editableOrder.name ? 'Name is required' : ''"
            />
          </BaseFormRow>
          <BaseFormRow>
            <BaseTextArea
              v-model="editableOrder.description"
              label="Description"
              id="order-description"
              name="order-description"
            />
          </BaseFormRow>
        </BaseForm>

        <div class="text-normal font-weight-bold mt-5 mb-3">Products List</div>
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem">
          <BaseButton type="button" class="btn-primary" @click="openAddProductModal">
            Add Product
          </BaseButton>
        </div>

        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem">
          <BaseInput
            v-model="productSearch"
            placeholder="Search products by name or id"
            id="product-search"
            name="product-search"
            style="max-width: 300px"
          />
          <BaseDropdown
            id="bulk-action"
            v-model="bulkAction"
            placeholder="Select Action"
            :options="['delete']"
          />
          <BaseButton
            v-if="bulkAction === 'delete' && selectedProductIds.length"
            type="button"
            class="btn-danger"
            @click="handleBulkActionConfirm"
          >
            Confirm
          </BaseButton>
        </div>
        <BaseTable :headers="productHeaders" :rows="filteredProducts">
          <template #select-header>
            <input
              type="checkbox"
              :checked="selectAll"
              @change="
                () => {
                  selectAll = !selectAll
                  toggleSelectAll()
                }
              "
              aria-label="Select all products"
            />
          </template>
          <template #select="{ row }">
            <input
              type="checkbox"
              :checked="selectedProductIds.includes(String(row.id))"
              @change="() => toggleProductSelection(String(row.id))"
            />
          </template>
          <template #price="{ row }">{{ row.price }} €</template>
        </BaseTable>

        <BaseModal
          v-model="showBulkDeleteModal"
          title="Confirm Bulk Deletion"
          @confirm="confirmBulkDelete"
        >
          <template #default>
            Are you sure you want to remove {{ selectedProductIds.length }} product(s) from this
            order?
          </template>
        </BaseModal>
      </div>
      <div v-else>No order found.</div>
    </BaseCard>

    <BaseCard>
      <div>
        <p>
          <strong>Created at:</strong>
          <span class="ml-2">{{
            order?.created_at ? new Date(order.created_at).toLocaleString() : 'N/A'
          }}</span>
        </p>
        <p>
          <strong>Updated at:</strong>
          <span class="ml-2">{{
            order?.updated_at ? new Date(order.updated_at).toLocaleString() : 'N/A'
          }}</span>
        </p>
        <p>
          <strong>Total Amount:</strong>
          <span v-if="isProductsChanged && order?.total_amount" class="ml-2">
            <s>{{ order.total_amount }} €</s>
            <span class="text-success font-weight-bold ml-2"> {{ newTotalAmount }} € </span>
          </span>
          <span v-else class="ml-2">
            {{ order?.total_amount ? `${order.total_amount} €` : '0.00 €' }}
          </span>
        </p>
        <BaseButton
          custom-class="btn-danger"
          :style="{ width: '100%' }"
          type="button"
          @click="openDeleteModal"
          >Delete</BaseButton
        >
        <BaseModal
          v-model="showRemoveAllProductsModal"
          title="Remove All Products?"
          @confirm="doUpdateOrder"
          @close="showRemoveAllProductsModal = false"
        >
          <template #default>
            Are you sure you want to remove all the products from the order?
          </template>
        </BaseModal>

        <BaseModal v-model="showDeleteModal" title="Confirm Deletion" @confirm="confirmDelete">
          <template #default>
            Are you sure you want to delete order <strong>{{ order?.id }}</strong
            >?
          </template>
        </BaseModal>

        <BaseModal
          v-model="showAddProductModal"
          title="Add Product"
          @close="showAddProductModal = false"
          @confirm="addSelectedProductsToOrder"
          :custom-class="'modal-lg'"
        >
          <template #default>
            <div>
              <Multiselect
                v-model="addProductSelected"
                class="custom-multiselect"
                :options="searchProducts"
                :multiple="true"
                :searchable="true"
                :loading="searchProductsLoading"
                :internal-search="false"
                :clear-on-select="true"
                :close-on-select="false"
                :allow-empty="true"
                :show-labels="false"
                label="name"
                track-by="id"
                placeholder="Search and select a product"
                @search-change="onProductSearchChange"
              >
                <template #option="props">
                  <div
                    :class="[
                      'option__desc',
                      {
                        disabled:
                          editableOrder &&
                          editableOrder.product_details &&
                          editableOrder.product_details.map((p) => p.id).includes(props.option.id),
                      },
                    ]"
                  >
                    <span class="option__title"
                      >{{ props.option.name }} - {{ props.option.id }}</span
                    >
                  </div>
                </template>
              </Multiselect>
              <div v-if="searchProductsError" class="mt-2 text-sm" style="color: red">
                {{ searchProductsError }}
              </div>
              <div v-if="!searchProductsLoading && !searchProducts.length" class="mt-2 text-sm">
                No products found.
              </div>
            </div>
          </template>
        </BaseModal>
      </div>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
.container {
  display: flex;
  justify-content: space-between;
  gap: $space-3;

  @media (max-width: $breakpoint-lg) {
    display: grid;
    justify-content: stretch;
  }

  .card:first-child {
    min-height: 90vh;
  }

  .card:nth-child(2) {
    position: sticky;
    top: $space-3;
    width: 40%;
    height: fit-content;

    @media (max-width: $breakpoint-lg) {
      width: 100%;
    }
  }

  .input-date {
    width: 25%;
    @media (max-width: $breakpoint-lg) {
      width: 100%;
    }
  }
}
</style>
