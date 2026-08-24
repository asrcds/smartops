<template>
  <div class="user-list-container">
    <div class="actions-bar">
      <el-button type="primary" @click="goToRegisterPage">新增用户</el-button>
    </div>
    <el-table :data="users" border style="width: 100%">
      <el-table-column prop="username" label="用户名" width="140" />
      <el-table-column prop="email" label="邮箱" width="220" />
      <el-table-column prop="role" label="角色" width="120">
        <template #default="scope">
          <el-select v-model="scope.row.role" placeholder="请选择角色" @change="updateUserRole(scope.row)">
            <el-option label="管理员" value="admin" />
            <el-option label="用户" value="user" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="scope">
          <el-popconfirm
            title="确定软删除该用户？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="softDeleteUser(scope.row)"
          >
            <el-button size="small" type="warning" slot="reference">软删除</el-button>
          </el-popconfirm>
          <el-popconfirm
            title="确定硬删除？不可恢复"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="hardDeleteUser(scope.row)"
          >
            <el-button
              size="small"
              type="danger"
              slot="reference"
              style="margin-left: 10px"
            >硬删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import users from '@/api/users' // 假设有 users.getUsers, users.updateUserRole, users.deleteUser, users.adminDeleteUser

const router = useRouter()
const users = ref([])

// 获取所有用户
const fetchUsers = async () => {
  try {
    const res = await usersApi.getUsers()
    users.value = res.data
  } catch (err) {
    ElMessage.error('获取用户列表失败')
  }
}

// 格式化日期
const formatDate = (val) => {
  if (!val) return ''
  const d = new Date(val)
  return d.toLocaleString()
}

// 修改角色
const updateUserRole = async (row) => {
  try {
    await usersApi.updateUserRole({ id: row.id, role: row.role })
    ElMessage.success('角色修改成功')
    fetchUsers()
  } catch (err) {
    ElMessage.error('角色修改失败')
    fetchUsers()
  }
}

// 软删除
const softDeleteUser = async (row) => {
  try {
    await usersApi.deleteUser({ id: row.id })
    ElMessage.success('用户已软删除')
    fetchUsers()
  } catch (err) {
    ElMessage.error('软删除失败')
  }
}

// 硬删除
const hardDeleteUser = async (row) => {
  try {
    await usersApi.adminDeleteUser({ id: row.id })
    ElMessage.success('用户已硬删除')
    fetchUsers()
  } catch (err) {
    ElMessage.error('硬删除失败')
  }
}

// 跳转注册页
const goToRegisterPage = () => {
  router.push({ name: 'Register' })
}

onMounted(fetchUsers)

// 兼容API模块命名
const usersApi = users.default ? users.default : users

</script>

<style scoped>
.user-list-container {
  padding: 24px;
  background: #fff;
}
.actions-bar {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>