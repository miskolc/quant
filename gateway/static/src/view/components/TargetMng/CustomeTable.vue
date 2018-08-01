<template>
  <div>
    <v-data-table
    v-model="selected"
    :headers="headers"
    :items="desserts"
    :total-items="totalDesserts"
    :loading="loading"
    :pagination.sync="pagination"
    select-all
    item-key="name"
    class="elevation-1"
  >
    <template slot="items" slot-scope="props">
      <tr :active="props.selected" >
        <td>
          <v-checkbox
          @click="props.selected = !props.selected"
            :input-value="props.selected"
            primary
            hide-details
          ></v-checkbox>
        </td>
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.calories }}</td>
        <td>{{ props.item.fat }}</td>
        <td>{{ props.item.carbs }}</td>
        <td>{{ props.item.protein }}</td>
        <td>{{ props.item.iron }}</td>
        <td>{{ props.item.fat }}</td>
        <td>{{ props.item.carbs }}</td>
        <td>{{ props.item.protein }}</td>
        <td>{{ props.item.iron }}</td>
        <td>{{ props.item.protein }}</td>
        <td>{{ props.item.iron }}</td>
        <td>
          <v-btn flat icon color="red" @click="openDelete(0)">
            <v-icon>delete_outline</v-icon>
          </v-btn>
        </td>
      </tr>
    </template>
  </v-data-table>
  <DeleteDialog :dialog.sync="deleteDialog" :id="id"/>
  </div>
</template>
<script>
import DeleteDialog from './DeleteDialog'
export default {
  components: {
    DeleteDialog
  },
  data () {
    return {
      deleteDialog: false,
      id: '',
      pagination: {
        sortBy: 'name'
      },
      selected: [],
      totalDesserts: 0,
      desserts: [],
      loading: true,
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
        { text: '昨收价', value: 'last_close' },
        { text: '删除', sortable: false }
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
  methods: {
    openDelete (id) {
      this.id = id
      this.deleteDialog = true
    },
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
        }, 500)
      })
    },
    getDesserts () {
      return [
        {
          value: false,
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%'
        },
        {
          value: false,
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: '1%'
        },
        {
          value: false,
          name: 'Eclair',
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          iron: '7%'
        },
        {
          value: false,
          name: 'Cupcake',
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          iron: '8%'
        },
        {
          value: false,
          name: 'Gingerbread',
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          iron: '16%'
        },
        {
          value: false,
          name: 'Jelly bean',
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          iron: '0%'
        },
        {
          value: false,
          name: 'Lollipop',
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          iron: '2%'
        },
        {
          value: false,
          name: 'Honeycomb',
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          iron: '45%'
        },
        {
          value: false,
          name: 'Donut',
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          iron: '22%'
        },
        {
          value: false,
          name: 'KitKat',
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          iron: '6%'
        }
      ]
    }
  },
  mounted () {
    this.getDataFromApi()
      .then(data => {
        this.desserts = data.items
        this.totalDesserts = data.total
      })
  }
}
</script>
