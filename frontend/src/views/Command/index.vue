<template>
  <div class="command-page">
    <div class="command-left">
      <div class="assets-header">
        <span class="assets-title">选择资产</span>
        <el-button size="small" icon="el-icon-refresh" @click="fetchAssets" circle :loading="assetsLoading"></el-button>
      </div>
      <el-table
        v-loading="assetsLoading"
        height="430"
        :data="assets"
        @selection-change="handleSelectionChange"
        style="width: 100%"
        border
        :row-key="row => row.id"
      >
        <el-table-column
          type="selection"
          width="45"
        />
        <el-table-column
          prop="ip"
          label="IP地址"
          min-width="100"
        />
        <el-table-column
          prop="hostName"
          label="主机名"
          min-width="110"
        />
      </el-table>
    </div>
    <div class="command-right">
      <div class="command-input-header">
        <span class="command-input-title">输入命令</span>
        <div class="quick-commands">
          <el-tag
            v-for="(cmd, idx) in quickCommands"
            :key="cmd"
            type="success"
            effect="plain"
            size="small"
            @click="handleQuickCommand(cmd)"
            class="quick-cmd-tag"
          >{{ cmd }}</el-tag>
        </div>
      </div>
      <el-input
        type="textarea"
        v-model="command"
        :rows="6"
        placeholder="请输入要执行的 shell 命令"
        class="command-input"
        :disabled="submitting"
      />
      <el-button
        type="primary"
        class="submit-btn"
        :loading="submitting"
        :disabled="!selectedAssetIds.length || !command.trim()"
        @click="onSubmit"
        size="large"
      >提交命令</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const assets = ref([])
const assetsLoading = ref(false)
const selectedAssetIds = ref([])

const command = ref('')
const submitting = ref(false)

const quickCommands = [
  'ls',
  'df -h',
  'top -bn1',
  'free -h',
  'uptime',
  'whoami',
  'ps aux --sort -pcpu | head',
  'cat /etc/os-release'
]

// 获取资产列表
const fetchAssets = async () => {
  assetsLoading.value = true
  try {
    const resp = await fetch('/api/assets')
    const respJson = await resp.json()
    // 假定 respJson: [{id, ip, hostName, ...}, ...]
    assets.value = Array.isArray(respJson) ? respJson : []
  } catch (e) {
    ElMessage.error('获取资产列表失败')
    assets.value = []
  }
  assetsLoading.value = false
}

const handleSelectionChange = (selection) => {
  selectedAssetIds.value = selection.map(row => row.id)
}

const handleQuickCommand = (cmd) => {
  if (command.value.trim()) {
    command.value += '\n' + cmd
  } else {
    command.value = cmd
  }
}

const router = useRouter()

const onSubmit = async () => {
  if (!selectedAssetIds.value.length || !command.value.trim()) return
  submitting.value = true
  try {
    // 假定接口: POST /api/tasks/executeCommand, body: {assetIds, command}
    const resp = await fetch('/api/tasks/executeCommand', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        assetIds: selectedAssetIds.value,
        command: command.value.trim()
      })
    })
    const respJson = await resp.json()
    if (resp.ok && respJson && respJson.success !== false) {
      ElMessageBox.alert('任务已提交', '成功', {
        confirmButtonText: '确定',
        showCancelButton: true,
        cancelButtonText: '去任务列表',
        showClose: false
      }).then(() => {
        // stay here
      }).catch(() => {
        router.push({ name: 'Tasks' }) // 跳转到任务列表页，需配置路由
      })
      // 清空输入
      command.value = ''
      selectedAssetIds.value = []
    } else {
      ElMessage.error(respJson.message || '任务提交失败')
    }
  } catch (e) {
    ElMessage.error('任务提交失败')
  }
  submitting.value = false
}

onMounted(() => {
  fetchAssets()
})

</script>

<style scoped>
.command-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 570px;
  background: linear-gradient(120deg, #bee8fa 0%, #e9f1fe 100%);
  padding: 48px 0;
  gap: 38px;
}
.command-left, .command-right {
  background: rgba(255,255,255,0.98);
  border-radius: 16px;
  box-shadow: 0 4px 18px 0 rgba(107,179,250,0.11), 0 1.5px 5px #b0c8ee30;
  padding: 32px 24px 24px 24px;
  min-width: 360px;
  max-width: 430px;
  width: 100%;
}
.command-left {
  flex: 0 0 410px;
  min-width: 340px;
}
.command-right {
  flex: 1 1 440px;
  min-width: 370px;
  display: flex;
  flex-direction: column;
}
.assets-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.assets-title {
  font-size: 18px;
  font-weight: 600;
  color: #234;
  letter-spacing: .2px;
}
.command-input-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 8px;
  gap: 12px;
}
.command-input-title {
  font-size: 17px;
  font-weight: 600;
  color: #234;
  margin-bottom: 2px;
}
.quick-commands {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 2px;
}
.quick-cmd-tag {
  cursor: pointer;
  user-select: none;
  transition: background 0.15s;
}
.quick-cmd-tag:hover {
  background: #e0f1ff;
  color: #016ee3;
}
.command-input {
  margin-bottom: 22px;
}
.submit-btn {
  align-self: flex-end;
  min-width: 150px;
  font-size: 16px;
  letter-spacing: 1px;
  margin-top: 8px;
}
@media (max-width: 1200px) {
  .command-page {
    flex-direction: column;
    align-items: center;
    gap: 28px;
    padding: 32px 0;
  }
  .command-left,
  .command-right {
    max-width: 98vw;
    min-width: 290px;
  }
}
</style>