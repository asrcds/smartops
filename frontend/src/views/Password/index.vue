<template>
  <div class="password-page">
    <el-card class="password-card">
      <h2>修改密码</h2>
      <el-form
        :model="form"
        :rules="rules"
        ref="passwordForm"
        label-width="100px"
        class="password-form"
      >
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input
            v-model="form.oldPassword"
            type="password"
            autocomplete="off"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="form.newPassword"
            type="password"
            autocomplete="off"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            autocomplete="off"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset" style="margin-left: 10px;">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordForm = ref(null)

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== form.value.newPassword) {
    callback(new Error('两次输入的新密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '新密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleSubmit = () => {
  passwordForm.value.validate(valid => {
    if (valid) {
      // 模拟调用后端接口
      ElMessage.info('功能开发中')
      // 清空表单：如果期望提交后清空表单可以恢复下面这句
      // handleReset()
    }
  })
}

const handleReset = () => {
  form.value.oldPassword = ''
  form.value.newPassword = ''
  form.value.confirmPassword = ''
  passwordForm.value.clearValidate()
}
</script>

<style scoped>
.password-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 40px 0;
}

.password-card {
  width: 400px;
  padding: 30px 40px 20px 40px;
}

.password-form {
  margin-top: 10px;
}
</style>