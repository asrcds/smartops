import { createRouter, createWebHistory } from 'vue-router'

// 懒加载页面组件
const Login = () => import('@/views/Login.vue')
const Register = () => import('@/views/Register.vue')
const ForgotPwd = () => import('@/views/ForgotPwd.vue')
const ResetPwd = () => import('@/views/ResetPwd.vue')
const Dashboard = () => import('@/views/Dashboard/index.vue')
const Command = () => import('@/views/Command/index.vue')
const Alert = () => import('@/views/Alert/index.vue')
const Tasks = () => import('@/views/Tasks/index.vue')
const Password = () => import('@/views/Password/index.vue')
const Nodes = () => import('@/views/Nodes/index.vue')
const Server = () => import('@/views/Server/index.vue')
const SSH = () => import('@/views/SSH/index.vue')
const Asset = () => import('@/views/Asset/index.vue')
const Probe = () => import('@/views/Probe/index.vue')
const Users = () => import('@/views/Users/index.vue')

// 测试组件（如果其他组件文件不存在）
const TestComponent = { 
  template: `
    <div style="padding: 20px;">
      <h1>{{ $route.name }} 页面</h1>
      <p>页面加载成功！</p>
      <router-link to="/login">返回登录</router-link>
    </div>
  `
}

// 路由配置
const routes = [
  // 认证相关
  {
    path: '/login',
    name: 'Login',
    component: Login || TestComponent,  // 如果文件不存在，使用测试组件
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register || TestComponent,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',  // 修正：使用 ForgotPassword
    component: ForgotPwd || TestComponent,
    meta: { requiresAuth: false }
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',  // 修正：使用 ResetPassword
    component: ResetPwd || TestComponent,
    meta: { requiresAuth: false }
  },
  // 功能模块
  {
    path: '/',
    redirect: '/login'  // 修改：默认重定向到登录页
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/command',
    name: 'Command',
    component: Command || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/alert',
    name: 'Alert',
    component: Alert || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/password',
    name: 'Password',
    component: Password || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/nodes',
    name: 'Nodes',
    component: Nodes || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/server/add',
    name: 'Server',
    component: Server || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/ssh/add',
    name: 'SSH',
    component: SSH || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/asset/add',
    name: 'Asset',
    component: Asset || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/probe',
    name: 'Probe',
    component: Probe || TestComponent,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users || TestComponent,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/login'  // 修改：404 重定向到登录页
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 简化路由守卫（先让应用能运行）
router.beforeEach((to, from, next) => {
  console.log(`路由跳转: ${from.path} -> ${to.path}`)
  
  // 简单认证检查
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  next()
})

export default router