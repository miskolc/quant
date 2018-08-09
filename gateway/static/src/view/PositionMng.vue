<template>
  <div>
    <div class="align-center mb-3">
      <v-layout justify-space-between align-center>
      <v-flex xs12 md6>
        <div class="search-input">
          <v-text-field label="代码、名称" v-model="search" prepend-icon="search" clearable clear-icon="cancel" single-line/>
        </div>
      </v-flex>
      <v-flex xs12 md6>
        <div class="handler-btn">
          <!-- <v-btn @click="dialog=true" color="info">新增</v-btn> -->
          <v-btn @click="OffOn">off/on</v-btn>
          &#x3000;&nbsp;
        </div>
      </v-flex>
    </v-layout>
    </div>
      <v-expansion-panel v-model="panel" expand v-if="!isEmty">
      <v-expansion-panel-content v-for="(item,i) in positionList" :key="item.strategy_code" v-if="item.position_list.length>0">
        <div slot="header">{{item.strategy_name}}
          <span class="panel-tag">{{item.strategy_code}}</span>
        </div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <PositionSummary :index="i" :panel="panel" :dataSource="item.position_list" :strategyCode="item.strategy_code"/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
     <v-alert
      :value="isEmty"
      color="white"
      icon="priority_high"
      outline
    >
      No data available
    </v-alert>
    <AddPositionGroupDialog :dialog.sync="dialog"/>
  </div>
</template>
<script>
import PositionSummary from './components/PositionMng/PositionSummary'
import AddPositionGroupDialog from './components/PositionMng/AddPositionGroupDialog'
export default {
  components: {
    PositionSummary,
    AddPositionGroupDialog
  },
  data () {
    return {
      panel: [true],
      dialog: false,
      search: '',
      timer: null,
      automaticTimer: null
    }
  },
  computed: {
    positionList () {
      let {list = []} = this.$store.getters['position/positionSearch']
      let positionList = []
      list.forEach(position => {
        let newPosition = {...{}, ...position}
        newPosition.position_list = []
        position['position_list'].forEach((item, index) => {
          if (!this.search) {
            newPosition.position_list.push(item)
          } else {
            if (item.code.includes(this.search) || item.name.includes(this.search)) {
              newPosition.position_list.push(item)
            }
          }
        })
        positionList.push(newPosition)
      })
      return positionList
    },
    isEmty () {
      let isEmty = true
      this.positionList.forEach(position => {
        if (position['position_list'].length > 0) isEmty = false
      })
      return isEmty
    }
  },
  watch: {
    search (n, o) {
      this.loading = true
      clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        if (this.search) this.panel = [...Array(this.positionList.length).keys()].map(_ => true)
        this.loading = false
      }, 200)
    }
  },
  methods: {
    OffOn () {
      if (this.panel.length) {
        this.panel = []
      } else {
        this.panel = [...Array(this.items).keys()].map(_ => true)
      }
    },
    async positionSearch () {
      await this.$store.dispatch('position/positionSearch')
    }
  },
  async mounted () {
    await this.positionSearch()
    this.automaticTimer = setInterval(async () => {
      await this.positionSearch()
    }, 1000 * 10)
  },
  beforeDestroy () {
    clearInterval(this.automaticTimer)
  }
}
</script>
<style lang="less">

</style>
