const express = require('express')
const app = express()
const config = require('../config')
const proxyMiddleware = require('http-proxy-middleware')
const proxyTable = config.dev.proxyTable


// 反向代理
Object.keys(proxyTable).forEach(function (context) {
  let options = proxyTable[context]
  if (typeof options === 'string') {
    options = {
      target: options
    }
  }
  app.use(proxyMiddleware(options.filter || context, options))
})

// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')())

// 设置静态资源路径
console.log('静态资源路径', config.build.assetsRoot)
app.use(express.static(config.build.assetsRoot))
app.listen(1234, () => {
  console.log('http://localhost:%s', 1234)
})
