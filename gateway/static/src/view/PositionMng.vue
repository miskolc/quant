<template>
  <div>
      <PositionSummary/>
      <hr>
      <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content v-for="(item,i) in items" :key="i">
        <div slot="header">Item{{i}}</div>
        <v-card>
          <v-card-text>
            <PositionSummary/>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>
<script>
import PositionSummary from './components/PositionMng/PositionSummary'
import PositionTable from './components/PositionMng/PositionTable'
export default {
  components: {
    PositionSummary,
    PositionTable
  },
  data () {
    return {
      panel: [],
      items: 5
    }
  },
  methods: {
    all () {
      this.panel = [...Array(this.items).keys()].map(_ => true)
    }
  }
}
</script>
