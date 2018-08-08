import axios from 'axios'
// import router from '@router/router'
// axios.options.headers = {'content-type': 'application/json;charset=UTF-8'}
// axios.defaults.timeout = 180000
const api = axios.create({timeout: 20000})
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 500:
          alert('系统错误，请联系管理员')
          break
        case 502:
          alert('系统正在重启...')
          break
        case 503:
          alert('服务暂时不可用...')
          break
        case 504:
          alert('请求超时，请检查网络...')
          break
      }
      return Promise.reject(error.response ? Object.assign(error.response.data,
        {status: error.response.status}) : {message: '页面请求失败！'}) // 返回接口返回的错误信息
    }
  }
)

export default api
