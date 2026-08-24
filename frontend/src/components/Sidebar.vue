<template>
  <el-menu
    :default-active="activeMenu"
    class="sidebar-menu"
    :collapse="collapsed"
    background-color="#001529"
    text-color="#fff"
    active-text-color="#409EFF"
    router
  >
    <el-menu-item index="/dashboard">
      <el-icon><Monitor /></el-icon>
      <span slot="title">仪表盘</span>
    </el-menu-item>
    <el-menu-item index="/broadcast">
      <el-icon><Message /></el-icon>
      <span slot="title">命令群发</span>
    </el-menu-item>
    <el-menu-item index="/alert">
      <el-icon><Warning /></el-icon>
      <span slot="title">安全预警</span>
    </el-menu-item>
    <el-menu-item index="/tasks">
      <el-icon><List /></el-icon>
      <span slot="title">任务列表</span>
    </el-menu-item>
    <el-menu-item index="/passwords">
      <el-icon><Key /></el-icon>
      <span slot="title">密码管理</span>
    </el-menu-item>
    <el-menu-item index="/nodes">
      <el-icon><Cpu /></el-icon>
      <span slot="title">节点管理</span>
    </el-menu-item>
    <el-menu-item index="/add-server">
      <el-icon><Plus /></el-icon>
      <span slot="title">添加服务器</span>
    </el-menu-item>
    <el-menu-item
      v-if="isAdmin"
      index="/users"
    >
      <el-icon><User /></el-icon>
      <span slot="title">用户列表</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'

// Element Plus Icons
import { Monitor, Message, Warning, List, Key, Cpu, Plus, User } from '@element-plus/icons-vue'

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  }
})

const route = useRoute()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const activeMenu = computed(() => {
  // only highlight sidebar if path matched, handle nested routes if any
  // Map sub-routes to their sidebar root if needed
  const map = {
    '/dashboard': '/dashboard',
    '/broadcast': '/broadcast',
    '/alert': '/alert',
    '/tasks': '/tasks',
    '/passwords': '/passwords',
    '/nodes': '/nodes',
    '/add-server': '/add-server',
    '/users': '/users',
  }
  // Find the closest parent if sub-page
  const path = route.path
  return Object.keys(map).find(key => path.startsWith(key)) || '/dashboard'
})
</script>

<style scoped>
.sidebar-menu {
  height: 100vh;
  border-right: 0;
  background: #001529;
}
.el-menu-item {
  font-size: 16px;
  min-width: 0;
}
.el-menu .el-icon {
  margin-right: 8px;
}
</style>