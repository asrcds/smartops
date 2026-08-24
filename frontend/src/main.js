import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import './assets/styles/index.css'

import 'nprogress/nprogress.css'
import NProgress from 'nprogress'

// 可选：配置 NProgress 全局进度条
NProgress.configure({ showSpinner: false })

// 路由导航守卫中启动/停止 NProgress（可选增强，后续具体可按需要在 router/index.js 内处理）
router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})
router.afterEach(() => {
  NProgress.done()
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')