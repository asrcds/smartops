<template>
  <div class="node-asset-list">
    <el-card>
      <div class="toolbar">
        <el-input
          v-model="search"
          placeholder="搜索IP或主机名"
          clearable
          style="width: 300px; margin-right: 20px"
          @keyup.enter.native="handleSearch"
          @clear="handleSearch"
        />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      <el-table
        :data="filteredAssets"
        border
        style="width: 100%; margin-top: 20px;"
        v-loading="loading"
      >
        <el-table-column prop="id" label="资产编号" width="120" />
        <el-table-column prop="ip" label="IP" width="180" />
        <el-table-column prop="hostname" label="主机名" width="200" />
        <el-table-column prop="os" label="操作系统" width="160" />
        <el-table-column prop="status" label="状态" width="140">
          <template #default="scope">
            <el-select
              v-model="assetStatusMap[scope.row.id]"
              placeholder="请选择状态"
              size="small"
              @change="val => handleStatusChange(scope.row, val)"
              style="width: 100px"
            >
              <el-option
                v-for="item in statusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="saveStatus(scope.row)"
              :loading="updatingIds.includes(scope.row.id)"
            >
              编辑状态
            </el-button>
            <el-button
              type="danger"
              size="small"
              v-if="isAdmin"
              @click="removeAsset(scope.row.id)"
              :loading="deletingIds.includes(scope.row.id)"
              style="margin-left: 5px;"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as assets from '@/api/assets'
import { useStore } from '@/store'

const search = ref('')
const loading = ref(false)
const updatingIds = ref([])
const deletingIds = ref([])

const statusOptions = [
  { value: '闲置', label: '闲置' },
  { value: '在用', label: '在用' },
  { value: '报废', label: '报废' },
]

// 资产数据
const assetList = ref([])

// ID:status 的映射，方便下拉选择绑定
const assetStatusMap = ref({})

const store = useStore()
const isAdmin = computed(() => store.isAdmin)

// 获取资产数据
async function fetchAssets() {
  loading.value = true
  try {
    const res = await assets.getAssets()
    assetList.value = Array.isArray(res) ? res : []
    // 初始化 assetStatusMap
    assetStatusMap.value = {}
    assetList.value.forEach(item => {
      assetStatusMap.value[item.id] = item.status
    })
  } catch (e) {
    ElMessage.error('获取资产列表失败')
  }
  loading.value = false
}

onMounted(fetchAssets)

// 搜索过滤
const filteredAssets = computed(() => {
  if (!search.value.trim()) return assetList.value
  const keyword = search.value.trim().toLowerCase()
  return assetList.value.filter(item =>
    (item.ip && item.ip.toLowerCase().includes(keyword)) ||
    (item.hostname && item.hostname.toLowerCase().includes(keyword))
  )
})

function handleSearch() {
  // 前端过滤, 不需要额外处理
}

// 编辑状态
function handleStatusChange(row, val) {
  assetStatusMap.value[row.id] = val
}

async function saveStatus(row) {
  if (assetStatusMap.value[row.id] === row.status) {
    ElMessage.info('状态未修改')
    return
  }
  updatingIds.value.push(row.id)
  try {
    await assets.updateAssetStatus(row.id, assetStatusMap.value[row.id])
    ElMessage.success('状态更新成功')
    await fetchAssets()
  } catch (e) {
    ElMessage.error('状态更新失败')
    assetStatusMap.value[row.id] = row.status // 恢复为原值
  }
  updatingIds.value = updatingIds.value.filter(id => id !== row.id)
}

// 删除资产
function removeAsset(id) {
  ElMessageBox.confirm('确定要删除该资产吗？', '提示', {
    confirmButtonText: '删除',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      deletingIds.value.push(id)
      try {
        await assets.deleteAsset(id)
        ElMessage.success('资产已删除')
        await fetchAssets()
      } catch (e) {
        ElMessage.error('删除失败')
      }
      deletingIds.value = deletingIds.value.filter(x => x !== id)
    })
    .catch(() => {})
}
</script>

<style scoped>
.node-asset-list {
  padding: 24px;
}
.toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
</style>