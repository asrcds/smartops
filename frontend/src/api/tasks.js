import { get, post } from './index'

// 执行命令
// data: { command: string, target_asset_ids: array }
export function executeCommand(data) {
  return post('/commands/execute', data)
}

// 获取任务历史
// params: { page, page_size }
export function getTaskHistory(params = {}) {
  return get('/commands/history', params)
}

// 获取任务结果
// taskId: string or number
export function getTaskResult(taskId) {
  return get(`/commands/result/${taskId}`)
}