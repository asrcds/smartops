<template>
  <div class="task-page">
    <el-table
      :data="taskList"
      style="width: 100%;"
      class="task-table"
      height="540"
      border
    >
      <el-table-column prop="id" label="任务ID" min-width="110" />
      <el-table-column prop="command" label="命令" min-width="140" />
      <el-table-column
        prop="targets"
        label="目标主机"
        min-width="120"
      >
        <template #default="{ row }">
          <span>{{ row.targets && row.targets.length > 0 ? row.targets[0] : '-' }}</span>
          <span v-if="row.targets && row.targets.length > 1" class="more-targets">等{{ row.targets.length }}台</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        min-width="100"
      >
        <template #default="{ row }">
          <el-tag
            :type="statusTagType(row.status)"
            disable-transitions
          >{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" min-width="160" />
      <el-table-column
        label="操作"
        min-width="110"
        align="center"
      >
        <template #default="{ row }">
          <el-button size="small" @click="showResult(row)" :disabled="!canShowResult(row)">
            查看结果
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        @current-change="handlePageChange"
      />
    </div>
    <el-dialog
      v-model="resultDialogVisible"
      title="任务结果"
      width="650px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <template #default>
        <div v-if="loadingResult" style="text-align:center;">
          <el-icon><loading /></el-icon> 加载中...
        </div>
        <div v-else>
          <el-tabs type="border-card">
            <el-tab-pane label="标准输出 stdout">
              <pre class="stdout-content">{{ currentTaskResult.stdout || '(无输出)' }}</pre>
            </el-tab-pane>
            <el-tab-pane label="错误输出 stderr">
              <pre class="stderr-content">{{ currentTaskResult.stderr || '(无错误输出)' }}</pre>
            </el-tab-pane>
          </el-tabs>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 假设 tasks 对象已在全局或 context 提供
// import tasks from '@/api/tasks'

const taskList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const resultDialogVisible = ref(false)
const loadingResult = ref(false)
const currentTaskResult = ref({ stdout: '', stderr: '' })

function statusTagType(status) {
  if (status === 'PENDING') return ''
  if (status === 'RUNNING') return 'info'
  if (status === 'SUCCESS') return 'success'
  if (status === 'FAILED') return 'danger'
  return ''
}
function statusText(status) {
  if (status === 'PENDING') return '等待中'
  if (status === 'RUNNING') return '执行中'
  if (status === 'SUCCESS') return '成功'
  if (status === 'FAILED') return '失败'
  return status
}
function canShowResult(row) {
  // 只有成功/失败才允许查结果
  return row.status === 'SUCCESS' || row.status === 'FAILED'
}

async function fetchTaskList() {
  try {
    // resp = await tasks.getTaskHistory({ page: page.value, page_size: pageSize.value })
    // 假数据结构: { total: 100, items: [ ... ] }
    const resp = await (typeof tasks !== 'undefined'
      ? tasks.getTaskHistory({ page: page.value, page_size: pageSize.value })
      : mockGetTaskHistory({ page: page.value, page_size: pageSize.value }))
    taskList.value = resp.items
    total.value = resp.total
  } catch (e) {
    ElMessage.error('获取任务历史失败')
  }
}

function handlePageChange(val) {
  page.value = val
  fetchTaskList()
}

async function showResult(row) {
  resultDialogVisible.value = true
  loadingResult.value = true
  currentTaskResult.value = { stdout: '', stderr: '' }
  try {
    // const res = await tasks.getTaskResult(row.id)
    const res = await (typeof tasks !== 'undefined'
      ? tasks.getTaskResult(row.id)
      : mockGetTaskResult(row.id))
    currentTaskResult.value = {
      stdout: res.stdout || '',
      stderr: res.stderr || ''
    }
  } catch (e) {
    ElMessage.error('获取结果失败')
    currentTaskResult.value = { stdout: '', stderr: '' }
  }
  loadingResult.value = false
}

onMounted(() => {
  fetchTaskList()
})

/* ----------------
  MOCK 数据
-----------------*/
const MOCK_STATUS = ['PENDING', 'RUNNING', 'SUCCESS', 'FAILED']
function mockGetTaskHistory({ page, page_size }) {
  const total = 34
  const items = []
  for (let i = 0; i < page_size; i++) {
    const idx = (page - 1) * page_size + i
    if (idx >= total) break
    items.push({
      id: `task-${1000 + idx}`,
      command: ['ls -al', 'df -h', 'cat /etc/passwd', 'echo Hello'][idx % 4],
      targets: [`host-${(idx % 5) + 1}`, `host-${((idx+2)%5)+1}`],
      status: MOCK_STATUS[idx % 4],
      created_at: `2024-06-0${(idx % 9) + 1} 10:1${idx % 6}:3${8 + idx}`
    })
  }
  return Promise.resolve({ total, items })
}
function mockGetTaskResult(id) {
  return Promise.resolve({
    stdout: `[stdout for ${id}]\nCommand executed successfully!\n...`,
    stderr: id.includes('3')
      ? `Error: permission denied for ${id}\n...`
      : ''
  })
}
</script>

<style scoped>
.task-page {
  padding: 18px 24px;
}
.task-table {
  background: rgba(255,255,255,0.98);
  border-radius: 10px;
  box-shadow: 0 2px 10px #b0c8ee22;
  padding: 10px 0 0 0;
}
.more-targets {
  color: #888;
  font-size: 12px;
  margin-left: 8px;
}
.table-pagination {
  display: flex;
  justify-content: flex-end;
  margin: 14px 4px 0 0;
}
.el-tag.success {
  background-color: #e5fced;
  border-color: #e5fced;
  color: #21b66f;
  font-weight: 600;
}
.el-tag.danger {
  background-color: #fde2e1;
  border-color: #fde2e1;
  color: #e55454;
  font-weight: 600;
}
.el-tag.info {
  background-color: #ecf6fe;
  border-color: #ecf6fe;
  color: #238ae6;
  font-weight: 600;
}
.stdout-content,
.stderr-content {
  background: #f7f8fa;
  padding: 12px;
  border-radius: 7px;
  font-family: Fira Mono, Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-all;
}
.stderr-content {
  background: #fff4f3;
  color: #ab3333;
}
</style>