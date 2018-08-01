<template>
  <div>
      <!-- <PositionSummary/> -->
    <div class="align-center mb-3">
      <v-btn @click="OffOn">off/on</v-btn>
      <v-btn @click="dialog=true">add</v-btn>
    </div>
      <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content v-for="(item,i) in items" :key="i">
        <div slot="header">Item{{item}} <span class="panel-tag">tag{{item}}</span></div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <PositionSummary :index="i" :panel="panel"/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <AddPositionGropDialog :dialog.sync="dialog"/>
  </div>
</template>
<script>
import PositionSummary from './components/PositionMng/PositionSummary'
import PositionTable from './components/PositionMng/PositionTable'
import AddPositionGropDialog from './components/PositionMng/AddPositionGropDialog'
export default {
  components: {
    PositionSummary,
    PositionTable,
    AddPositionGropDialog
  },
  data () {
    return {
      panel: [true],
      items: 5,
      dialog: false
    }
  },
  methods: {
    OffOn () {
      if (this.panel.length) {
        this.panel = []
      } else {
        this.panel = [...Array(this.items).keys()].map(_ => true)
      }
    }
  }
}
</script>
<style lang="less">
.panel-tag{
  float: right;
  padding-right: 10px;
}
</style>
