<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="dataResult"
      hide-actions
      :loading="loading"
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.code }}</td>
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.price | toFixed }}</td>
        <td>{{ props.item.pointcut | toFixed }}</td>
      </template>
    </v-data-table>
  </div>
</template>
<script>
export default {
  data () {
    return {
      headers: [
        { text: '代码', value: 'code' },
        { text: '名称', value: 'name', sortable: false },
        { text: '当前价格', value: 'price', sortable: false },
        { text: '买入点', value: 'pointcut', sortable: false }
      ]
    }
  },
  props: {
    dataSource: Array,
    loading: Boolean,
    search: String
  },
  computed: {
    dataResult () {
      let dataSource = this.dataSource || []
      if (!this.search) return dataSource
      return dataSource.filter(item => {
        return item.code.includes(this.search) || item.name.includes(this.search)
      })
    }
  }
}
</script>
