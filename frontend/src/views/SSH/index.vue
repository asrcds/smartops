<template>
  <div class="ssh-page">
    <el-card class="ssh-card">
      <div class="form-title">添加 SSH 信息</div>
      <el-form
        ref="sshForm"
        :model="form"
        :rules="rules"
        class="ssh-form"
        label-width="96px"
      >
        <el-form-item label="资产" prop="asset_id">
          <el-select v-model="form.asset_id" placeholder="请选择资产" filterable>
            <el-option
              v-for="item in assetOptions"
              :key="item.id"
              :label="item.host_name || item.ip_address"
              :value="item.id"
            >
              <span>{{ item.host_name || '-' }} ({{ item.ip_address }})</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="SSH 用户名" prop="ssh_user">
          <el-input v-model="form.ssh_user" placeholder="请输入 SSH 用户名" />
        </el-form-item>
        <el-form-item label="SSH 密码" prop="ssh_password">
          <el-input v-model="form.ssh_password" placeholder="请输入 SSH 密码" show-password />
        </el-form-item>
        <el-form-item label="SSH 端口" prop="ssh_port">
          <el-input v-model="form.ssh_port" placeholder="默认 22" type="number" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
// assets API 需在项目中已有，可参考其它页面引入
import * as assets from '@/api/assets'

const form = reactive({
  asset_id: '',
  ssh_user: '',
  ssh_password: '',
  ssh_port: ''
})

const sshForm = ref(null)
const assetOptions = ref([])

const rules = {
  asset_id: [
    { required: true, message: '请选择资产', trigger: 'change' }
  ],
  ssh_user: [
    { required: true, message: '请输入 SSH 用户名', trigger: 'blur' }
  ],
  ssh_password: [
    { required: true, message: '请输入 SSH 密码', trigger: 'blur' }
  ],
  ssh_port: [
    { required: true, message: '请输入 SSH 端口', trigger: 'blur' }
  ]
}

// 获取资产列表
const fetchAssets = async () => {
  try {
    const res = await assets.fetchAssetList()
    assetOptions.value = res?.list || []
  } catch (e) {
    ElMessage.error('资产列表获取失败')
  }
}

const handleSubmit = () => {
  sshForm.value.validate(async (valid) => {
    if (!valid) return

    // 下面应调用更新资产全部字段的接口，资产表需支持 SSH 信息字段
    // 当前 assets.updateAssetStatus 仅支持状态更新，不能更新 SSH 信息
    // 当前仅做演示，实际开发需后端实现 PUT /assets/{id} 的完整字段更新
    ElMessage.info('功能开发中')
    // 伪代码（需后端接口支持）：
    // await assets.updateAsset(form.asset_id, {
    //   ssh_user: form.ssh_user,
    //   ssh_password: form.ssh_password,
    //   ssh_port: form.ssh_port,
    //   ...其它资产字段
    // })
  })
}

const handleReset = () => {
  form.asset_id = ''
  form.ssh_user = ''
  form.ssh_password = ''
  form.ssh_port = ''
  sshForm.value && sshForm.value.clearValidate()
}

onMounted(() => {
  fetchAssets()
})
</script>

<style scoped>
.ssh-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
  min-height: 480px;
  background: #f7f8fa;
}
.ssh-card {
  width: 420px;
  padding: 32px 40px 24px 40px;
}
.form-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #214585;
  letter-spacing: 1px;
}
.ssh-form {
  margin-top: 8px;
}
</style>