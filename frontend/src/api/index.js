import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 公开路径（不需要 token 的接口）
const publicPaths = ['/login', '/register', '/forgot-password', '/reset-password']

// 请求拦截器：添加 token 到 Authorization 头
service.interceptors.request.use(
  config => {
    // 判断是否为公开路径
    const isPublic = publicPaths.some(path => config.url.includes(path))
    
    if (!isPublic) {
      // 从 localStorage 获取 token（而不是从 store）
      const token = localStorage.getItem('token')
      if (token) {
        config.headers['Authorization'] = 'Bearer ' + token
      }
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：统一处理响应
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res && typeof res === 'object') {
      if ('code' in res && res.code !== 200) {
        ElMessage.error(res.msg || '请求出错')
        
        // 处理未授权
        if (res.code === 401) {
          // 清除本地存储
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          
          // 跳转到登录页
          window.location.href = '/login'
        }
        return Promise.reject(res)
      }
      // code === 200
      return res.data !== undefined ? res.data : res
    }
    return res
  },
  error => {
    // 网络或服务器错误
    if (error.response && error.response.status === 401) {
      ElMessage.error('未授权或登录已过期，请重新登录')
      
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      
      // 跳转到登录页
      window.location.href = '/login'
    } else {
      ElMessage.error(error.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

// 通用请求方法
export function get(url, params = {}, config = {}) {
  return service.get(url, {
    params,
    ...config,
  })
}

export function post(url, data = {}, config = {}) {
  return service.post(url, data, config)
}

export function put(url, data = {}, config = {}) {
  return service.put(url, data, config)
}

export function del(url, config = {}) {
  return service.delete(url, config)
}

export default service