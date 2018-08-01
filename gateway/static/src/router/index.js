import Vue from 'vue'
import Router from 'vue-router'
import routes from './routes'
import 'nprogress/nprogress.css'
import NProgress from 'nprogress'

Vue.use(Router)
NProgress.configure({
  showSpinner: false,
  easing: 'ease',
  speed: 450
})
const router = new Router({
  routes
})
router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})

router.afterEach((to, from) => {
  NProgress.done()
})
export default router
