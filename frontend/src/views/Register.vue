<template>
  <div class="register-page">
    <div class="register-card">
      <div class="register-title">注册新账号</div>
      <el-form
        :model="form"
        :rules="rules"
        ref="registerForm"
        label-position="top"
        class="register-form"
        @keyup.enter="submit"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" autocomplete="username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱（可选）" prop="email">
          <el-input v-model="form.email" autocomplete="email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" show-password placeholder="请再次输入密码" autocomplete="new-password" />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            class="register-btn"
            :loading="loading"
            style="width: 100%"
            @click="submit"
          >
            注册
          </el-button>
        </el-form-item>
        <div class="register-links">
          已有账号？
          <router-link class="link" :to="{ name: 'Login' }">去登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as auth from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const registerForm = ref(null)

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请确认密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 32, message: '长度为2~32个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度为6~32位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const submit = () => {
  registerForm.value.validate(async valid => {
    if (!valid) return
    loading.value = true
    try {
      await auth.register({
        username: form.username,
        email: form.email || undefined,
        password: form.password
      })
      ElMessage.success('注册成功，请登录')
      router.replace({ name: 'Login' })
    } catch (err) {
        // 拦截器已经弹出错误提示，这里不再重复
      console.error('Register error:', err)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #6fc3ff 0%, #e6eafe 100%);
}
.register-card {
  box-shadow: 0 6px 32px 0 rgba(0,24,128,0.09), 0 1.5px 4px #b0c8ee33;
  border-radius: 18px;
  background: rgba(255,255,255,0.97);
  padding: 36px 28px 22px 28px;
  min-width: 340px;
  width: 100%;
  max-width: 420px;
}
.register-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 28px;
  color: #234;
}
.register-btn {
  height: 42px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  margin-top: 8px;
}
.register-links {
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