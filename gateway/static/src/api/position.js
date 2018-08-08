import axios from './'
export default {
  positionSearch: params => axios.post('api/position/search', params),
  positionAdd: params => axios.post('api/position', params),
  positionDelete: params => axios.delete(`api/position/${params.id}`, params),
  positionUpdate: params => axios.put('api/position', params)
}
