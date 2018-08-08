<template>
  <div>
    <div class="align-center mb-3">
      <v-layout justify-space-between align-center>
      <v-flex xs12 md6>
        <div class="search-input">
          <v-text-field label="代码、名称" prepend-icon="search" clearable clear-icon="cancel" single-line/>
        </div>
      </v-flex>
      <v-flex xs12 md6>
        <div class="handler-btn">
          <v-btn @click="dialog=true" color="info">新增</v-btn>
          <v-btn @click="OffOn">off/on</v-btn>
          &#x3000;&nbsp;
        </div>
      </v-flex>
    </v-layout>
    </div>
      <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content v-for="item in positionList" :key="item.strategy_code">
        <div slot="header">{{item.strategy_name}}
          <!-- <span class="panel-tag">{{item.strategy_code}}</span> -->
        </div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <PositionSummary :index="i" :panel="panel" :dataSource="item.position_list"/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <AddPositionGropDialog :dialog.sync="dialog"/>
  </div>
</template>
<script>
import PositionSummary from './components/PositionMng/PositionSummary'
import AddPositionGropDialog from './components/PositionMng/AddPositionGropDialog'
export default {
  components: {
    PositionSummary,
    AddPositionGropDialog
  },
  data () {
    return {
      panel: [true],
      items: 5,
      dialog: false
    }
  },
  computed: {
    positionList () {
      const {list = []} = this.$store.getters['position/positionSearch']
      return list
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
  }
}
</script>
<style lang="less">
.panel-tag{
  float: right;
  padding-right: 10px;
}
</style>
