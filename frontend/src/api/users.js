import { get, put, del } from './index'

// 获取用户列表，支持分页参数
export function getUsers(params = {}) {
  return get('/users', params)
}

// 获取用户详情
export function getUserDetail(id) {
  return get(`/users/${id}`)
}

// 更新用户角色
export function updateUserRole(id, role) {
  return put(`/users/${id}/role`, { role })
}

// 删除用户（软删除）
export function deleteUser(id) {
  return del(`/users/${id}`)
}

// 管理员删除用户（硬删除）
export function adminDeleteUser(id) {
  return del(`/admin/users/${id}`)
}