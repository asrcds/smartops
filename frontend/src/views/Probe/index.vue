<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = ref({
  target_ip: '',
  protocol: '',
  timeout: 3,
})

const probeForm = ref(null)

const protocolOptions = [
  { label: 'ICMP (Ping)', value: 'icmp' },
  { label: 'TCP', value: 'tcp' },
  { label: 'UDP', value: 'udp' }
]

const rules = {
  target_ip: [
    { required: true, message: '请输入目标 IP', trigger: 'blur' }
  ],
  protocol: [
    { required: true, message: '请选择协议', trigger: 'change' }
  ],
  timeout: [
    { required: true, message: '请输入超时时间', trigger: 'blur' },
    { type: 'number', min: 1, max: 20, message: '超时时间应在 1~20 秒', trigger: 'blur' }
  ]
}

function handleSubmit() {
  ElMessage.info('功能开发中 (Demo 表单，无后端接口)')
}

function handleReset() {
  form.value = {
    target_ip: '',
    protocol: '',
    timeout: 3,
  }
  probeForm.value && probeForm.value.clearValidate()
}
</script>

<template>
  <div class="probe-page">
    <el-card class="probe-card" shadow="hover">
      <div class="form-title">
        拔测任务
      </div>
      <el-alert
        title="功能开发中，当前为表单原型，仅做演示。"
        type="warning"
        show-icon
        class="mb-2"
        :closable="false"
      />
      <el-form
        ref="probeForm"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="probe-form"
      >
        <el-form-item label="目标 IP" prop="target_ip">
          <el-input v-model="form.target_ip" placeholder="例如 8.8.8.8" />
        </el-form-item>
        <el-form-item label="协议" prop="protocol">
          <el-select v-model="form.protocol" placeholder="请选择协议">
            <el-option
              v-for="item in protocolOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="超时时间" prop="timeout">
          <el-input-number
            v-model="form.timeout"
            :min="1"
            :max="20"
            :step="1"
            controls-position="right"
          />
          <span class="timeout-unit">秒</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.probe-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 50px 0;
  min-height: 480px;
  background: #f7f8fa;
}

.probe-card {
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

.probe-form {
  margin-top: 8px;
}

.mb-2 {
  margin-bottom: 18px;
}

.timeout-unit {
  margin-left: 8px;
  color: #888;
  font-size: 14px;
}
</style>