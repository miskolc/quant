<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="dataSource"
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
    loading: Boolean
  }
}
</script>
