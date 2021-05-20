import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)

const state = {
    login: false,
    username:"",
    ip:'',
    peerId: '',
    skywayKey: 'c7a61801-29ab-4d90-8529-98760ec84aed',
}

const store = new Vuex.Store({
    state,
})

const getters = {
    username: state => state.username
}

export default store
