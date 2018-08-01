<template>
  <div>
    <div class="align-center mb-3">
      <v-btn @click="all">all</v-btn>
      <v-btn @click="addPanelTartget(false)">add panel</v-btn>
      <v-btn @click="addPanelTartget(true)">add tartget</v-btn>
    </div>
    <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content v-for="(item,i) in items" :key="i">
        <div slot="header">Item{{i}}</div>
        <v-card>
          <v-card-text>
            <PanelTable/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <AddPanelDialog :dialog.sync="dialog" :isTartget="isTartget"/>
  </div>
</template>

<script>
import AddPanelDialog from './components/TargetMng/AddPanelDialog'
import PanelTable from './components/TargetMng/PanelTable'
export default {
  components: {
    AddPanelDialog,
    PanelTable
  },
  data () {
    return {
      panel: [],
      items: 5,
      dialog: false,
      isTartget: false
    }
  },
  methods: {
    all () {
      this.panel = [...Array(this.items).keys()].map(_ => true)
    },
    addPanelTartget (isTartget) {
      this.isTartget = isTartget
      this.dialog = true
    }
  }
}
</script>
