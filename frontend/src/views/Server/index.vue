<template>
  <div class="server-page">
    <el-card class="server-card">
      <div class="form-title">添加服务器</div>
      <el-form
        :model="form"
        :rules="rules"
        ref="serverForm"
        label-width="100px"
        class="server-form"
      >
        <el-form-item label="资产编号" prop="asset_id">
          <el-input v-model="form.asset_id" placeholder="请输入资产编号"/>
        </el-form-item>
        <el-form-item label="IP地址" prop="ip_address">
          <el-input v-model="form.ip_address" placeholder="请输入IP地址"/>
        </el-form-item>
        <el-form-item label="主机名" prop="host_name">
          <el-input v-model="form.host_name" placeholder="请输入主机名"/>
        </el-form-item>
        <el-form-item label="操作系统" prop="os">
          <el-input v-model="form.os" placeholder="请输入操作系统"/>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%;">
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="采购日期" prop="purchase_date">
          <el-date-picker
            v-model="form.purchase_date"
            type="date"
            placeholder="选择采购日期"
            style="width: 100%;"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="所属用户" prop="user_id">
          <el-select v-model="form.user_id" placeholder="请选择所属用户" filterable style="width: 100%;">
            <el-option
              v-for="user in userOptions"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 假设 asset 状态选项
const statusOptions = [
  { label: '在线', value: 'online' },
  { label: '离线', value: 'offline' },
  { label: '维护中', value: 'maintaining' },
  { label: '报废', value: 'deprecated' }
]

const form = reactive({
  asset_id: '',
  ip_address: '',
  host_name: '',
  os: '',
  status: '',
  purchase_date: '',
  user_id: ''
})

const rules = {
  asset_id: [{ required: true, message: '请输入资产编号', trigger: 'blur' }],
  ip_address: [{ required: true, message: '请输入IP地址', trigger: 'blur' }],
  host_name: [{ required: true, message: '请输入主机名', trigger: 'blur' }],
  os: [{ required: true, message: '请输入操作系统', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  purchase_date: [{ required: true, message: '请选择采购日期', trigger: 'change' }],
  user_id: [{ required: true, message: '请选择所属用户', trigger: 'change' }]
}

const userOptions = ref([])
const loading = ref(false)
const serverForm = ref(null)

async function fetchUserList() {
  try {
    // 这里假设有全局 users API
    const res = await users.getUserList()
    userOptions.value = Array.isArray(res) ? res : []
  } catch (e) {
    ElMessage.error('获取用户列表失败')
    userOptions.value = []
  }
}

async function handleSubmit() {
  serverForm.value.validate(async valid => {
    if (!valid) return
    loading.value = true
    try {
      // 提交新资产
      await assets.createAsset({ ...form })
      ElMessage.success('服务器添加成功')
      handleReset()
    } catch (e) {
      ElMessage.error(e?.message || '服务器添加失败')
    }
    loading.value = false
  })
}

function handleReset() {
  Object.assign(form, {
    asset_id: '',
    ip_address: '',
    host_name: '',
    os: '',
    status: '',
    purchase_date: '',
    user_id: ''
  })
  serverForm.value && serverForm.value.clearValidate()
}

onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.server-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
  min-height: 600px;
  background: #f7f8fa;
}
.server-card {
  width: 520px;
  padding: 32px 40px 24px 40px;
}
.form-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #214585;
  letter-spacing: 1px;
}
.server-form {
  margin-top: 8px;
}
</style>