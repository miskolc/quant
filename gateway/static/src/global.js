import Vue from 'vue'
import 'normalize.css'
import * as filters from '@utils/filters'
import Message from '@components/Message'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import '@style/index.less'

Vue.config.productionTip = false

for (let key in filters) {
  Vue.filter(key, filters[key])
}

Vue.use(Vuetify)

Vue.prototype.$message = Message
