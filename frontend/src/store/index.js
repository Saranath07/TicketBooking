import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';


Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    user: {
      username : "",
      role : "",
      admin : false,
      public_id : "",
      access_token : "",

    }
  },
  getters: {
    getUser: state => state.user
  
  },
  mutations: {
    SET_USER(state, user) {
     state.user = user;
    }
  },
  actions: {
    setUser({ commit }, user) {
      commit('SET_USER', user);
    }
  },
  modules: {
  }
});


