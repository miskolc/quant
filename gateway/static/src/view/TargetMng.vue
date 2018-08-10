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
          <v-btn @click="OffOn">off/on</v-btn>
          &#x3000;&nbsp;
        </div>
      </v-flex>
    </v-layout>
    </div>
    <v-expansion-panel v-model="panel" expand v-if="!isEmty">
      <v-expansion-panel-content v-for="item in targetList" :key="item.strategy_code" v-if="item.target_list.length>0 || item.strategy_code=='custom'">
        <div slot="header">{{item.strategy_name}}
          <span class="panel-tag">{{item.strategy_code}}</span>
        </div>
        <v-card dark>
          <v-card-text style="background-color:#212121" >
            <CustomeTable v-if="item.strategy_code=='custom'"
              :dataSource="item.target_list"
              :loading="loading"
              :strategyCode="item.strategy_code"
              :search="search" @refresh="targetSearch"/>
            <PanelTable v-else :dataSource="item.target_list" :loading="loading" :search="search"/>
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
  </div>
</template>

<script>
import PanelTable from './components/TargetMng/PanelTable'
import CustomeTable from './components/TargetMng/CustomeTable'
export default {
  components: {
    PanelTable,
    CustomeTable
  },
  data () {
    return {
      panel: [true],
      customeDialog: false,
      search: '',
      loading: false,
      timer: null,
      automaticTimer: null
    }
  },
  watch: {
    search (n, o) {
      this.loading = true
      clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        if (this.search) this.panel = [...Array(this.targetList.length).keys()].map(_ => true)
        this.loading = false
      }, 200)
    }
  },
  computed: {
    targetList () {
      let {list = []} = this.$store.getters['target/targetSearch']

      let targetList = []
      list.forEach(target => {
        let newTarget = {...{}, ...target}
        newTarget.target_list = []
        target['target_list'].forEach((item, index) => {
          if (!this.search) {
            newTarget.target_list.push(item)
          } else {
            if (item.code.includes(this.search) || item.name.includes(this.search)) {
              newTarget.target_list.push(item)
            }
          }
        })
        targetList.push(newTarget)
      })
      return targetList
    },
    isEmty () {
      let isEmty = true
      this.targetList.forEach(target => {
        if (target['target_list'].length > 0) isEmty = false
      })
      return isEmty
    }
  },
  methods: {
    OffOn () {
      if (this.panel.length) {
        this.panel = []
      } else {
        this.panel = [...Array(this.targetList.length).keys()].map(_ => true)
      }
    },
    showPanel (list) {
      let isShow = false
      list.forEach(item => {
        if (item.show) isShow = true
      })
      return isShow
    },
    async targetSearch () {
      this.loading = true
      await this.$store.dispatch('target/targetSearch')
      this.loading = false
    }
  },
  async mounted () {
    await this.targetSearch()
    this.automaticTimer = setInterval(async () => {
      await this.targetSearch()
    }, 1000 * 5)
  },
  beforeDestroy () {
    clearInterval(this.automaticTimer)
  }
}
</script>
