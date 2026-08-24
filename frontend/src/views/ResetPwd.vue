<template>
  <div class="resetpwd-page">
    <div class="resetpwd-card">
      <div class="resetpwd-title">重置密码</div>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="新密码" prop="password">
          <el-input v-model="form.password" show-password autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" show-password autocomplete="new-password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="resetpwd-btn" :loading="loading" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
      <div class="resetpwd-links">
        <router-link class="link" to="/login">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
// 假设你有 auth API
import auth from '@/api/auth'

const route = useRoute()
const router = useRouter()
const token = route.query.token

const formRef = ref(null)
const form = ref({
  password: '',
  confirmPassword: ''
})
const loading = ref(false)

const rules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: (rule, value, callback) => {
        if (value !== form.value.password) {
          callback('两次密码输入不一致')
        } else {
          callback()
        }
      }, trigger: 'blur'
    }
  ]
}

const onSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    if (!token) {
      ElMessage.error('重置链接无效或已过期')
      return
    }
    loading.value = true
    try {
      await auth.resetPassword({
        token,
        form.value.password
      })
      ElMessage.success('密码重置成功，请登录')
      router.replace({ path: '/login' })
    } catch (e) {
      ElMessage.error(e?.message || '重置密码失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.resetpwd-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(118deg, #b3caf5 0%, #e6eafe 100%);
}
.resetpwd-card {
  box-shadow: 0 6px 32px 0 rgba(0,24,128,0.09), 0 1.5px 4px #b0c8ee33;
  border-radius: 18px;
  background: rgba(255,255,255,0.97);
  padding: 36px 28px 22px 28px;
  min-width: 340px;
  width: 100%;
  max-width: 420px;
}
.resetpwd-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 28px;
  color: #234;
}
.resetpwd-btn {
  height: 42px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  margin-top: 8px;
  width: 100%;
}
.resetpwd-links {
  text-align: center;
  margin-top: 16px;
  font-size: 15px;
  color: #456;
  letter-spacing: 0.5px;
}
.link {
  color: #4a83e4;
  text-decoration: none;
  margin: 0 8px;
  font-weight: 500;
  transition: color .2s;
}
.link:hover {
  color: #1666c1;
}
</style>