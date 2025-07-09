<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array as () => Array<{ label: string; route?: string }>,
    required: true,
  },
})

const crumbs = computed(() => props.items)
</script>

<template>
  <nav class="base-breadcrumbs" aria-label="Breadcrumb">
    <ol>
      <li v-for="(crumb, idx) in crumbs" :key="idx">
        <template v-if="crumb.route && idx < crumbs.length - 1">
          <router-link :to="crumb.route">{{ crumb.label }}</router-link>
        </template>
        <template v-else>
          <span class="active">{{ crumb.label }}</span>
        </template>
      </li>
    </ol>
  </nav>
</template>

<style scoped lang="scss">
.base-breadcrumbs ol {
  display: flex;
  list-style: none;
  padding: 0;
  gap: $space-1;
}
.base-breadcrumbs li {
  display: flex;
  align-items: center;
}
.base-breadcrumbs li:not(:last-child)::after {
  content: '/';
  margin: 0 $space-1;
  color: #888;
}
.base-breadcrumbs .active {
  color: #888;
  font-weight: bold;
}
</style>
