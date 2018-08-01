<template>
  <div>
      <!-- <PositionSummary/> -->
      <div class="align-center mb-3">
      <v-btn @click="all">all</v-btn>
      <v-btn @click="dialog=true">add</v-btn>
    </div>
      <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content v-for="(item,i) in items" :key="i">
        <div slot="header">Item{{i}}</div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <PositionSummary/>
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
      panel: [1],
      items: 5,
      dialog: false
    }
  },
  methods: {
    all () {
      this.panel = [...Array(this.items).keys()].map(_ => true)
    }
  }
}
</script>
