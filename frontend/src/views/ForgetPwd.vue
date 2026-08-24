<template>
  <div class="forgetpwd-page">
    <div class="forgetpwd-card">
      <div class="forgetpwd-title">忘记密码</div>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="forgetpwd-form">
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="form.email" autocomplete="email" placeholder="请输入注册邮箱"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            class="forgetpwd-btn"
            :loading="loading"
            type="primary"
            style="width: 100%"
            @click="onSubmit"
          >
            发送重置链接
          </el-button>
        </el-form-item>
      </el-form>
      <div class="forgetpwd-links">
        <router-link class="link" to="/login">返回登录</router-link>
        <span class="divider">|</span>
        <router-link class="link" to="/register">注册新账号</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 假设auth.forgotPassword方法已在某处实现并可直接调用
import auth from '@/api/auth' // 确认路径符合实际项目结构

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  email: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] }
  ]
}

const onSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await auth.forgotPassword(form.email)
      ElMessage.success('重置链接已发送（请查看控制台）')
    } catch (err) {
      ElMessage.error(err?.message || '重置失败，请稍后再试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.forgetpwd-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(118deg, #b3caf5 0%, #e6eafe 100%);
}
.forgetpwd-card {
  box-shadow: 0 6px 32px 0 rgba(0,24,128,0.09), 0 1.5px 4px #b0c8ee33;
  border-radius: 18px;
  background: rgba(255,255,255,0.97);
  padding: 36px 28px 22px 28px;
  min-width: 340px;
  width: 100%;
  max-width: 420px;
}
.forgetpwd-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 28px;
  color: #234;
}
.forgetpwd-btn {
  height: 42px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  margin-top: 8px;
}
.forgetpwd-links {
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