<template>
  <div>
    <v-expansion-panel v-model="panel" expand>
      <v-expansion-panel-content>
        <div slot="header">custome</div>
        <v-card dark>
          <v-card-text style="background-color:#212121">
            <v-layout row justify-space-between align-center>
              <v-flex>
                <div class="search-input">
                  <v-text-field label="Code" prepend-icon="search" clearable clear-icon="cancel" single-line/>
                </div>
              </v-flex>
              <v-flex>
                <div class="handler-btn">
                  <v-btn light @click="addPanelTartget(false)">add</v-btn>
                  <v-btn light>delete</v-btn>
                </div>
              </v-flex>
            </v-layout>
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
    <AddOrUpdateCustomeDialog :dialog.sync="customeDialog" :isEdit="isEdit" />
  </div>
</template>

<script>
import AddOrUpdateCustomeDialog from './components/TargetMng/AddOrUpdateCustomeDialog'
import PanelTable from './components/TargetMng/PanelTable'
import CustomeTable from './components/TargetMng/CustomeTable'
export default {
  components: {
    AddOrUpdateCustomeDialog,
    PanelTable,
    CustomeTable },
  data () {
    return {
      panel: [1],
      items: 5,
      customeDialog: false,
      isEdit: false
    }
  },
  methods: {
    all () {
      this.panel = [...Array(this.items).keys()].map(_ => true)
    },
    addPanelTartget (isEdit) {
      this.isEdit = isEdit
      this.customeDialog = true
    }
  }
}
</script>
