// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from "./store"
import * as io from "socket.io-client";
import VueSocketIO from "vue-socket.io"

// var socket = io('http://localhost:5000/test')
// socket.on('event', param => {
//     console.log(param)
// });
// console.log('io:', socket)


Vue.config.productionTip = true

// Vue.use(new VueSocketIO({
//   debug: true,
//   connection: "ws://localhost:5000/test"
// }));

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
