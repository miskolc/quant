<template>
  <v-layout wrap>
    <v-layout justify-space-between align-center>
      <v-flex xs12 md6>
        <!-- <div class="search-input">
          <v-text-field label="Search" prepend-icon="search" clearable clear-icon="cancel" single-line/>
        </div> -->
      </v-flex>
      <v-flex xs12 md6>
        <div class="handler-btn">
          <v-btn color="info" @click="dialog=true">新增</v-btn>
          <v-btn  @click="isDelete=!isDelete">删除</v-btn>
        </div>
      </v-flex>
    </v-layout>
    <v-container fluid grid-list-md>
      <v-data-iterator loading hide-actions :items="dataSource"  content-tag="v-layout" row wrap>
        <v-flex slot="item" slot-scope="props" xs12 sm6 md4 lg3>
          <v-card>
            <v-badge overlap v-model="isDelete" class="card-badge" color="red">
              <v-btn icon small slot="badge" @click="deleteHandle(props.item)">
                <v-icon dark small>clear</v-icon>
              </v-btn>
              <v-card-title>
                <h4>{{ props.item.code }}</h4>
              </v-card-title>
            </v-badge>
            <v-divider></v-divider>
            <v-list dense>
              <v-list-tile>
                <v-list-tile-content>名称:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.name }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>当前价格:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.price | toFixed }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>买入价:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.price_in }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>利润:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.profit }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>profit_value:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.profit_value }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>股票数量:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.shares }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>strategy_code:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.strategy_code }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>价值:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.worth }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>更新时间:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.update_time }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>创建时间:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.create_time }}</v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
      </v-data-iterator>
    </v-container>
    <AddDataIteratorDialog :dialog.sync="dialog" />
    <DeleteDialog :dialog.sync="deleteDialog" :id.sync="id" @refresh="refresh"/>
  </v-layout>
</template>

<script>
import AddDataIteratorDialog from './AddDataIteratorDialog'
import DeleteDialog from './DeleteDialog'

export default {
  components: {
    AddDataIteratorDialog,
    DeleteDialog
  },
  props: {
    index: [Number, String],
    panel: Array,
    dataSource: Array
  },
  watch: {
    panel: {
      handler (n, o) {
        if (!this.panel[this.index]) this.isDelete = false
      },
      deep: true
    }
  },
  data () {
    return {
      dialog: false,
      deleteDialog: false,
      id: '',
      isDelete: false,
      rowsPerPageItems: [4, 8, 12],
      pagination: {
        rowsPerPage: 4
      },
      items: [{
        value: false,
        name: 'Frozen Yogurt',
        calories: 159,
        fat: 6.0,
        carbs: 24,
        protein: 4.0,
        sodium: 87,
        calcium: '14%',
        iron: '1%'
      },
      {
        value: false,
        name: 'Ice cream sandwich',
        calories: 237,
        fat: 9.0,
        carbs: 37,
        protein: 4.3,
        sodium: 129,
        calcium: '8%',
        iron: '1%'
      },
      {
        value: false,
        name: 'Eclair',
        calories: 262,
        fat: 16.0,
        carbs: 23,
        protein: 6.0,
        sodium: 337,
        calcium: '6%',
        iron: '7%'
      },
      {
        value: false,
        name: 'Cupcake',
        calories: 305,
        fat: 3.7,
        carbs: 67,
        protein: 4.3,
        sodium: 413,
        calcium: '3%',
        iron: '8%'
      },
      {
        value: false,
        name: 'Gingerbread',
        calories: 356,
        fat: 16.0,
        carbs: 49,
        protein: 3.9,
        sodium: 327,
        calcium: '7%',
        iron: '16%'
      },
      {
        value: false,
        name: 'Jelly bean',
        calories: 375,
        fat: 0.0,
        carbs: 94,
        protein: 0.0,
        sodium: 50,
        calcium: '0%',
        iron: '0%'
      },
      {
        value: false,
        name: 'Lollipop',
        calories: 392,
        fat: 0.2,
        carbs: 98,
        protein: 0,
        sodium: 38,
        calcium: '0%',
        iron: '2%'
      },
      {
        value: false,
        name: 'Honeycomb',
        calories: 408,
        fat: 3.2,
        carbs: 87,
        protein: 6.5,
        sodium: 562,
        calcium: '0%',
        iron: '45%'
      },
      {
        value: false,
        name: 'Donut',
        calories: 452,
        fat: 25.0,
        carbs: 51,
        protein: 4.9,
        sodium: 326,
        calcium: '2%',
        iron: '22%'
      },
      {
        value: false,
        name: 'KitKat',
        calories: 518,
        fat: 26.0,
        carbs: 65,
        protein: 7,
        sodium: 54,
        calcium: '12%',
        iron: '6%'
      }
      ]
    }
  },
  methods: {
    deleteHandle (item) {
      this.id = item.name
      this.deleteDialog = true
    },
    refresh () {
      this.isDelete = false
    }
  }
}
</script>
<style lang="less">
.card-badge{
  width: 99%;
}
</style>
