// src/store/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))
  
  const isLoggedIn = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.username || '')
  const role = computed(() => userInfo.value?.role || '')
  
  // 设置 token
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  // 设置用户信息
  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }
  
  // 登录（同时设置 token 和用户信息）
  function login(loginData) {
    token.value = loginData.access_token || ''
    userInfo.value = loginData.user || {}
    
    if (loginData.access_token) {
      localStorage.setItem('token', loginData.access_token)
    }
    if (loginData.user) {
      localStorage.setItem('userInfo', JSON.stringify(loginData.user))
    }
  }
  
  // 登出
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    username,
    role,
    setToken,
    setUserInfo,
    login,
    logout
  }
})