import axios from './'
export default {
  targetSearch: params => axios.post('api/target/search', params),
  targetAdd: params => axios.post('api/target', params),
  targetDelete: params => axios.put(`api/target/delete`, params),
  targetUpdate: params => axios.put('api/target', params),
  stockCode: params => axios.get(`api/stock/${params.code}`, params)
}
