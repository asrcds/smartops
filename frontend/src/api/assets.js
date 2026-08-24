import { get, post, put, del } from './index'

// 获取资产列表，支持分页参数 skip, limit
export function getAssets(params = {}) {
  return get('/assets', params)
}

// 创建新资产
export function createAsset(data) {
  return post('/assets', data)
}

// 更新资产状态
export function updateAssetStatus(id, status) {
  return put(`/assets/${id}/status`, { status })
}

// 删除资产
export function deleteAsset(id) {
  return del(`/assets/${id}`)
}