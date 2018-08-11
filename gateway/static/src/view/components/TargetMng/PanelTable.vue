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
        { text: 'code', value: 'code' },
        { text: 'name', value: 'name', sortable: false },
        { text: 'price', value: 'price', sortable: false },
        { text: 'pointcut', value: 'pointcut', sortable: false }
      ]
    }
  },
  props: {
    dataSource: Array,
    loading: Boolean
  }
}
</script>
