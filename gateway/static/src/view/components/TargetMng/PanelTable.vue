<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :pagination.sync="pagination"
      :total-items="totalDesserts"
      :loading="loading"
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.code }}</td>
        <td>{{ props.item.time_key }}</td>
        <td>{{ props.item.open }}</td>
        <td>{{ props.item.close }}</td>
        <td>{{ props.item.high }}</td>
        <td>{{ props.item.low }}</td>
        <td>{{ props.item.pe_ratio }}</td>
        <td>{{ props.item.turnover_rate }}</td>
        <td>{{ props.item.volume }}</td>
        <td>{{ props.item.turnover }}</td>
        <td>{{ props.item.change_rate }}</td>
        <td>{{ props.item.last_close }}</td>
      </template>
    </v-data-table>
  </div>
</template>
<script>
export default {
  data () {
    return {
      totalDesserts: 0,
      desserts: [],
      loading: true,
      pagination: {},
      headers: [
        {text: '代码', value: 'code'},
        { text: 'k线时间', value: 'time_key' },
        { text: '开盘价', value: 'open' },
        { text: '收盘价', value: 'close ' },
        { text: '最高价', value: 'high' },
        { text: '最低价', value: 'low' },
        { text: '市盈率', value: 'pe_ratio' },
        { text: '换手率', value: 'turnover_rate' },
        { text: '成交量', value: 'volume' },
        { text: '成交额', value: 'turnover' },
        { text: '涨跌幅', value: 'change_rate' },
        { text: '昨收价', value: 'last_close' }
      ]
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getDataFromApi()
          .then(data => {
            this.desserts = data.items
            this.totalDesserts = data.total
          })
      },
      deep: true
    }
  },
  mounted () {
    this.getDataFromApi()
      .then(data => {
        this.desserts = data.items
        this.totalDesserts = data.total
      })
  },
  methods: {
    getDataFromApi () {
      this.loading = true
      return new Promise((resolve, reject) => {
        const { sortBy, descending, page, rowsPerPage } = this.pagination

        let items = this.getDesserts()
        const total = items.length

        if (this.pagination.sortBy) {
          items = items.sort((a, b) => {
            const sortA = a[sortBy]
            const sortB = b[sortBy]

            if (descending) {
              if (sortA < sortB) return 1
              if (sortA > sortB) return -1
              return 0
            } else {
              if (sortA < sortB) return -1
              if (sortA > sortB) return 1
              return 0
            }
          })
        }

        if (rowsPerPage > 0) {
          items = items.slice((page - 1) * rowsPerPage, page * rowsPerPage)
        }

        setTimeout(() => {
          this.loading = false
          resolve({
            items,
            total
          })
        }, 1000)
      })
    },
    getDesserts () {
      let array = []
      for (let index = 0; index < 10; index++) {
        array.push({
          code: Math.ceil(Math.random() * 1000000),
          time_key: 159 + Math.ceil(Math.random() * 10),
          open: 6.0 + Math.ceil(Math.random() * 10),
          close: 24 + Math.ceil(Math.random() * 10),
          high: 4.0 + Math.ceil(Math.random() * 10),
          low: Math.ceil(Math.random() * 10) + '%',
          pe_ratio: Math.ceil(Math.random() * 10) + '%',
          turnover_rate: Math.ceil(Math.random() * 10) + '%',
          volume: 6.0 + Math.ceil(Math.random() * 10),
          turnover: 24 + Math.ceil(Math.random() * 10),
          change_rate: 4.0 + Math.ceil(Math.random() * 10),
          last_close: Math.ceil(Math.random() * 10)
        })
      }
      return array
    }
  }
}
</script>
