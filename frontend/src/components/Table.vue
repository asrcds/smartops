<template>
  <div class="common-table">
    <el-table
      :data="data"
      v-loading="loading"
      border
      :header-cell-style="{ background: 'var(--surface-color)', color: 'var(--text-color)' }"
      :cell-style="{ color: 'var(--text-color)' }"
      :style="{ width: '100%' }"
      :row-key="rowKey"
    >
      <template v-for="col in columns" :key="col.prop">
        <el-table-column
          v-bind="getColumnProps(col)"
        >
          <template #default="scope" v-if="hasSlotCol(col)">
            <slot :name="col.prop" v-bind="scope"/>
          </template>
        </el-table-column>
      </template>
    </el-table>
    <div v-if="pagination" class="table-pagination">
      <el-pagination
        :total="pagination.total"
        :current-page="pagination.page"
        :page-size="pagination.size"
        :layout="pagination.layout || 'total, prev, pager, next, sizes'"
        @current-change="onCurrentChange"
        @size-change="onSizeChange"
        background
      />
    </div>
  </div>
</template>

<script setup>
import { computed, useSlots } from 'vue'

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  columns: {
    type: Array,
    default: () => []
  },
  loading: Boolean,
  pagination: {
    type: Object,
    default: null
  },
  rowKey: {
    // 可传递 row-key
    type: [String, Function],
    default: row => row.id || row.key || row._id || JSON.stringify(row)
  }
})

const emit = defineEmits(['update:pagination', 'page-change', 'size-change'])

const slots = useSlots()

// Column helper - separate props for el-table-column
function getColumnProps(col) {
  const base = { 
    prop: col.prop,
    label: col.label,
    minWidth: col.minWidth,
    width: col.width,
    align: col.align,
    fixed: col.fixed,
    sortable: col.sortable,
    showOverflowTooltip: col.showOverflowTooltip ?? true
  }
  if (!hasSlotCol(col) && col.formatter) {
    base.formatter = col.formatter
  }
  if (col.resizable !== undefined) base.resizable = col.resizable
  return base
}

// Check if the column has a custom slot
function hasSlotCol(col) {
  // prefer to match camelCase and kebab-case
  return !!slots[col.prop] || !!slots[col.prop && kebabCase(col.prop)]
}

function kebabCase(str) {
  return str?.replace(/[A-Z]/g, m => '-' + m.toLowerCase())
}

// Pagination
function onCurrentChange(page) {
  emit('update:pagination', { ...props.pagination, page })
  emit('page-change', page)
}
function onSizeChange(size) {
  emit('update:pagination', { ...props.pagination, size, page: 1 })
  emit('size-change', size)
}
</script>

<style scoped>
.common-table {
  width: 100%;
}
.table-pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>