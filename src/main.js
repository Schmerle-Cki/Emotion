import Vue from 'vue'
import router from './router'
import ElementUI from 'element-ui';
import axios from 'axios'
import VueAxios from 'vue-axios'
import {setCookie,getCookie,GET_Message,POST_Message} from './utils/communication.js'
//import * as getImageList from './utils/loadImage.js'
import 'element-ui/lib/theme-chalk/index.css';



Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.use(VueAxios,axios)
Vue.prototype.$axios = axios
Vue.prototype.$cookieStore={
  setCookie,
  getCookie
}
Vue.prototype.$get = GET_Message
Vue.prototype.$post = POST_Message
//Vue.prototype.$getImage = getImageList

import App from './App.vue'

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
