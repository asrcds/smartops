// src/api/auth.js
import { post, get } from './index'

// 用户登录
export function login(username, password) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)
  return post('/login', formData,{headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  }})  // ✅ 添加 /api
}

// 用户注册
export function register(data) {
  return post('/register', data)  // ✅ 添加 /api
}

// 忘记密码
export function forgotPassword(email) {
  return post('/forgot-password', { email })  // ✅ 添加 /api
}

// 重置密码
export function resetPassword(token, new_password) {
  return post('/reset-password', { token, new_password })  // ✅ 添加 /api
}

// 获取当前用户信息
export function getCurrentUser() {
  return get('/me')  // ✅ 添加 /api
}

// 获取用户资料
export function getUserProfile() {
  return get('/profile')  // ✅ 添加 /api
}

// 可选：添加用户相关接口
export function updateUserProfile(data) {
  return put('/profile', data)
}

export function changePassword(data) {
  return post('/change-password', data)
}

export default {
  login,
  register,
  forgotPassword,
  resetPassword,
  getCurrentUser,
  getUserProfile,
  updateUserProfile,
  changePassword
}