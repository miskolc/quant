import axios from '@api'
const state = {
  status: false
}
const getters = {
  status: state => state.status
}
const actions = {
  async getStatusd ({commit}, params = {}) {
    const {data} = await axios.get('url', params)
    commit('SET_STATE', {target: 'status', data})
  }
}
const mutations = {
  SET_STATE (state, payload) {
    const { target, data } = payload
    state[target] = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
