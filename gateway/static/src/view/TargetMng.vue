<template>
  <div>
    <div class="align-center mb-3">
      <v-btn @click="OffOn">off/on</v-btn>
    </div>
    <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content>
        <div slot="header">custome</div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <CustomeTable/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
      <v-expansion-panel-content v-for="(item,i) in items" :key="i">
        <div slot="header">Item{{i}}</div>
        <v-card style="background-color:#212121">
          <v-card-text>
            <PanelTable/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import PanelTable from './components/TargetMng/PanelTable'
import CustomeTable from './components/TargetMng/CustomeTable'
export default {
  components: {
    PanelTable,
    CustomeTable },
  data () {
    return {
      panel: [true],
      items: 5,
      customeDialog: false
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
