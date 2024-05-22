import axios from 'axios'
import type { App } from 'vue'
import { router } from '@/router/index'

const baseURL = 'http://127.0.0.1:5000/api'

axios.defaults.withCredentials=true

const axiosInstance = axios.create({
  baseURL: baseURL, // 设置统一的基础 URL
  timeout: 5000, // 设置请求超时时间
  withCredentials: true, // 允许携带 cookie
})

export default {
  install(app: App<Element>) {
    // 添加实例方法
    app.config.globalProperties.$http = axiosInstance
  }
}

export { baseURL }
