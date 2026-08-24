<script setup>
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 用户和主题的本地存储键
const USER_KEY = 'user'
const THEME_KEY = 'theme'

export const useMainStore = defineStore('main', () => {
  // 用户状态：{ token, username, role, isLoggedIn }
  const user = ref({
    token: '',
    username: '',
    role: '',
    isLoggedIn: false,
  })

  // 主题
  const theme = ref('light')

  // 初始化时从 localStorage 恢复
  function init() {
    // 用户信息
    try {
      const savedUser = JSON.parse(localStorage.getItem(USER_KEY))
      if (savedUser && savedUser.token) {
        user.value = { ...savedUser, isLoggedIn: true }
      }
    } catch {}
    // 主题
    const savedTheme = localStorage.getItem(THEME_KEY)
    if (savedTheme === 'dark' || savedTheme === 'light') {
      theme.value = savedTheme
    }
  }
  init()

  // 登录
  function login(token, userInfo) {
    user.value = {
      token,
      username: userInfo.username || '',
      role: userInfo.role || '',
      isLoggedIn: true,
    }
    localStorage.setItem(USER_KEY, JSON.stringify(user.value))
  }

  // 登出
  function logout() {
    user.value = {
      token: '',
      username: '',
      role: '',
      isLoggedIn: false,
    }
    localStorage.removeItem(USER_KEY)
  }

  // 设置主题
  function setTheme(nextTheme) {
    if (nextTheme === 'dark' || nextTheme === 'light') {
      theme.value = nextTheme
      localStorage.setItem(THEME_KEY, nextTheme)
    }
  }

  // 是否为管理员
  const isAdmin = computed(() => user.value.role === 'admin' && user.value.isLoggedIn)

  return {
    user,
    theme,
    login,
    logout,
    setTheme,
    isAdmin,
  }
})
</script>