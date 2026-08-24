<template>
  <div :class="theme">
    <div v-if="showLayout">
      <!-- 顶部栏 -->
      <header class="app-header">
        <span class="app-title">智能运维监控系统</span>
        <button class="theme-toggle-btn" @click="toggleTheme">
          {{ theme === 'dark' ? '切换为亮色' : '切换为暗色' }}
        </button>
      </header>
      <div class="app-layout">
        <!-- 侧边栏 -->
        <aside class="app-sidebar">
          <nav>
            <router-link to="/">首页</router-link>
            <router-link to="/dashboard">仪表板</router-link>
            <router-link to="/login">登录</router-link>
          </nav>
        </aside>
        <!-- 主内容区 -->
        <main class="app-main">
          <router-view />
        </main>
      </div>
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 需要不展示布局的页面路径
const hiddenLayoutRoutes = ['/login', '/register']

const showLayout = computed(() => {
  return !hiddenLayoutRoutes.includes(route.path)
})

// 主题切换
const theme = ref('light')

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

// 监听主题变化
watch(theme, (val) => {
  document.documentElement.classList.toggle('dark', val === 'dark')
}, { immediate: true })
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 24px;
  background: var(--header-bg, #fff);
  border-bottom: 1px solid #eee;
}

.app-title {
  font-size: 1.2em;
  font-weight: bold;
}

.theme-toggle-btn {
  padding: 6px 12px;
  background: var(--el-color-primary, #409eff);
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.app-layout {
  display: flex;
  height: calc(100vh - 56px);
}

.app-sidebar {
  width: 200px;
  background: var(--sidebar-bg, #f7f7fa);
  border-right: 1px solid #eee;
  padding: 20px 10px;
  box-sizing: border-box;
}

.app-sidebar a {
  display: block;
  color: #333;
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.2s;
}
.app-sidebar a.router-link-exact-active {
  color: var(--el-color-primary, #409eff);
}

.app-main {
  flex: 1;
  padding: 24px;
  background: var(--main-bg, #fafbfc);
  min-width: 0;
}

/* 暗色主题简单样式 */
.dark {
  --header-bg: #222;
  --sidebar-bg: #181818;
  --main-bg: #181c20;
  color: #f3f4f6;
}
.dark .app-header {
  background: var(--header-bg);
  border-bottom: 1px solid #303030;
}
.dark .app-sidebar {
  background: var(--sidebar-bg);
  border-right: 1px solid #252525;
}
.dark .app-main {
  background: var(--main-bg);
}
.dark .theme-toggle-btn {
  background: #444;
}
</style>