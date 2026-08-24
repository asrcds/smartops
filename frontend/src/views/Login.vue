<template>
  <div class="login-bg">
    <div class="login-container">
      <el-card class="login-card">
        <div class="login-title">登录</div>
        <el-form
          :model="loginForm"
          :rules="rules"
          ref="loginFormRef"
          label-width="0"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              prefix-icon="User"
              placeholder="用户名"
              @keyup.enter.native="handleLogin"
              clearable
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              prefix-icon="Key"
              placeholder="密码"
              show-password
              @keyup.enter.native="handleLogin"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              class="login-btn"
              :loading="loading"
              @click="handleLogin"
              style="width:100%"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        <div class="login-links">
          <router-link class="link" :to="{ name: 'Register' }">注册</router-link>
          <span class="divider">|</span>
          <router-link class="link" :to="{ name: 'ForgotPassword' }">忘记密码？</router-link>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

// 导入正确的 API
import { login as apiLogin, getCurrentUser } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loginForm = ref({
  username: '',
  password: '',
})

const loading = ref(false)

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 24, message: '用户名长度 2-24 位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, max: 32, message: '密码长度 4-32 位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    // 验证表单
    await loginFormRef.value.validate()
    loading.value = true
    
    // 1. 调用登录接口
    const loginRes = await apiLogin(
    loginForm.value.username,  // ✅
    loginForm.value.password   // ✅
    )
    
    if (!loginRes?.access_token) {
      throw new Error('登录失败，未获取到token')
    }
    
    // 2. 保存 token
    userStore.setToken(loginRes.access_token)
    
    // 3. 获取用户信息
    let userInfo = {}
    if (loginRes.user) {
      // 如果登录接口直接返回用户信息
      userInfo = loginRes.user
    } else if (getCurrentUser) {
      // 如果单独有获取用户信息的接口
      userInfo = await getCurrentUser()
    } else {
      // 默认用户信息
      userInfo = {
        username: loginForm.value.username,
        role: 'user'
      }
    }
    
    // 4. 保存用户信息
    userStore.setUserInfo(userInfo)
    
    ElMessage.success('登录成功')
    
    // 5. 跳转到仪表板
    router.replace({ name: 'Dashboard' })
    
  } catch (err) {
    console.error('登录失败:', err)
    ElMessage.error(err.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  min-width: 100vw;
  /* 渐变+模糊叠加样式 */
  background: linear-gradient(120deg,#90aef7 0%,#c7d0ff 50%,#98e1ec 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.login-bg::before {
  content: "";
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  background: inherit;
  filter: blur(16px) brightness(0.9);
  z-index: 1;
}

.login-container {
  position: relative;
  z-index: 2;
  min-width: 340px;
  width: 100%;
  max-width: 380px;
}

.login-card {
  box-shadow: 0 6px 32px 0 rgba(0,24,128,0.08), 0 1.5px 4px #b0c8ee33;
  border-radius: 18px;
  background: rgba(255,255,255,0.96);
  padding: 38px 24px 24px 24px;
  transition: box-shadow 0.2s;
}
.login-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 28px;
  color: #234;
}
.login-btn {
  height: 42px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
}
.login-links {
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
.divider {
  margin: 0 3px;
  color: #bcc;
}
</style>