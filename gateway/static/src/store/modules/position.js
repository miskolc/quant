import api from '@api/position'
const state = {
  positionSearch: {}
}
const getters = {
  status: state => state.status
}
Object.keys(state).forEach(key => {
  getters[key] = state => state[key]
})
const actions = {
  async positionSearch ({commit}, params = {}) {
    try {
      const {data} = await api.positionSearch(params)
      commit('SET_STATE', {target: 'positionSearch', data})
    } catch (error) {
      throw error
    }
  },
  async positionAdd ({commit}, params = {}) {
    try {
      const {data} = await api.positionAdd(params)
      return data
    } catch (error) {
      throw error
    }
  },

  async positionUpdate ({commit}, params = {}) {
    try {
      const {data} = await api.positionUpdate(params)
      return data
    } catch (error) {
      throw error
    }
  },
  async positionDelete ({commit}, id) {
    try {
      const {data} = await api.positionDelete({id})
      return data
    } catch (error) {
      throw error
    }
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
