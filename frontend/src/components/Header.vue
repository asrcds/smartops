<template>
  <header class="header">
    <div class="header-title">智能运维监控系统</div>
    <div class="header-actions">
      <el-switch
        v-model="isDark"
        inline-prompt
        active-icon="Moon"
        inactive-icon="Sunny"
        :active-value="true"
        :inactive-value="false"
        @change="toggleTheme"
        class="theme-switch"
      />
      <el-dropdown trigger="click">
        <span class="el-dropdown-link user-info">
          <el-avatar :src="user.avatar" size="small" />
          <span class="user-name">{{ user.name }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/store'
import { ElMessage } from 'element-plus'
import { Sunny, Moon, SwitchButton } from '@element-plus/icons-vue'

// 可以根据实际的用户信息获取方式调整
const store = useStore()
const router = useRouter()

// 假设用户信息存储在 store.user
const user = computed(() => store.user || {
  name: '用户',
  avatar: 'https://api.dicebear.com/6.x/initials/svg?seed=User'
})

// 主题切换
const isDark = ref(false)

onMounted(() => {
  // 初始化时检查当前是暗色还是亮色
  isDark.value = document.body.classList.contains('body-dark')
})

function toggleTheme(val) {
  if (val) {
    document.body.classList.add('body-dark')
    document.body.classList.remove('body-light')
  } else {
    document.body.classList.remove('body-dark')
    document.body.classList.add('body-light')
  }
}

function logout() {
  store.logout()
  // 清除 token 等信息后跳转登录页
  ElMessage.success('退出登录成功')
  router.replace({ name: 'Login' })
}
</script>

<style scoped>
.header {
  height: 56px;
  background: var(--surface-color);
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--box-shadow);
  padding: 0 32px;
  font-weight: 500;
}
.header-title {
  font-size: 20px;
  letter-spacing: 1px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}
.theme-switch {
  margin-right: 10px;
}
.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 8px;
}
.user-name {
  font-size: 15px;
  color: var(--text-color);
  margin-left: 2px;
}
/* 适配暗色模式下样式可以补充 */
</style>