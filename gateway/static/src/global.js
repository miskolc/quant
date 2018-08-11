import Vue from 'vue'
import 'normalize.css'
import * as filters from '@utils/filters'
import Message from '@components/Message'
import Loading from '@components/Loading'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import '@style/index.less'
// import VueWebsocket from 'vue-websocket'
Vue.config.productionTip = false

for (let key in filters) {
  Vue.filter(key, filters[key])
}

Vue.use(Vuetify)
Vue.use(Loading.directive)
Vue.prototype.$message = Message
Vue.prototype.$loading = Loading.service
// Vue.use(VueWebsocket, 'ws://localhost:8080')
