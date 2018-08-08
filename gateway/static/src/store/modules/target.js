import api from '@api/target'
const state = {
  targetSearch: {}
}
const getters = {
  status: state => state.status
}
Object.keys(state).forEach(key => {
  getters[key] = state => state[key]
})
const actions = {
  async targetSearch ({commit}, params = {}) {
    try {
      const {data} = await api.targetSearch(params)
      commit('SET_STATE', {target: 'targetSearch', data})
    } catch (error) {
      throw error
    }
  },
  async stockCode ({commit}, code) {
    try {
      const {data} = await api.stockCode({code})
      return data
    } catch (error) {
      throw error
    }
  },
  async targetAdd ({commit}, params = {}) {
    try {
      const {data} = await api.targetAdd(params)
      return data
    } catch (error) {
      throw error
    }
  },

  async targetUpdate ({commit}, params = {}) {
    try {
      const {data} = await api.targetUpdate(params)
      return data
    } catch (error) {
      throw error
    }
  },
  async targetDelete ({commit}, ids = []) {
    try {
      const {data} = await api.targetDelete({'id_list': ids})
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
