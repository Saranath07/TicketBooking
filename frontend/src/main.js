import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import NavBar from './components/NavBar.vue';


Vue.component('navbar', NavBar);




Vue.config.productionTip = false




new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
