<template>
  <v-layout wrap>
    <v-layout justify-space-between align-center>
      <v-flex xs12 md6>
      </v-flex>
      <v-flex xs12 md6>
        <div class="handler-btn">
          <v-btn color="info" @click="addHandle">new</v-btn>
          <v-btn  @click="isHandle=!isHandle">handler</v-btn>
        </div>
      </v-flex>
    </v-layout>
    <v-container fluid grid-list-md>
      <v-data-iterator :loading="loading" hide-actions :items="dataSource"  content-tag="v-layout" row wrap>
        <v-flex slot="item" slot-scope="props" xs12 sm6 md4 lg3>
          <v-card class="iterator-card">
           <v-fade-transition>
            <span class="iterator-card__handle" v-if="isHandle">
                <v-btn icon small color="white" light @click="updateHandle(props.item)">
                  <v-icon dark small >edit</v-icon>
                </v-btn>
                <v-btn icon small color="red" @click="deleteHandle(props.item)">
                  <v-icon dark small>clear</v-icon>
                </v-btn>
              </span>
            </v-fade-transition>
              <v-card-title>
                <h4>{{ props.item.code }}</h4>
              </v-card-title>
            <v-divider></v-divider>
            <v-list dense>
              <v-list-tile>
                <v-list-tile-content>name:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.name || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>price:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.price || 0 }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>price in:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.price_in || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>profit:</v-list-tile-content>
                <v-list-tile-content class="align-end">
                  <span :class="{
                  'make-text':props.item.profit>0,
                  'kui-text':props.item.profit<0
                }">{{ props.item.profit || '—' }}
                </span>
                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>profit value:</v-list-tile-content>
                <v-list-tile-content class="align-end">
                  <span :class="{
                  'make-text':props.item.profit_value>0,
                  'kui-text':props.item.profit_value<0
                }">{{ props.item.profit_value || '—' }}</span>
                  </v-list-tile-content>
                </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>shares:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.shares || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>strategy code:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.strategy_code || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>worth:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.worth || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>update_time:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.update_time || '—' }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>create_time:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.create_time || '—' }}</v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
      </v-data-iterator>
    </v-container>
    <AddOrUpdateDataIteratorDialog
      :isEdit="isEdit"
      :dialog.sync="dialog"
      @refresh="refresh"
      :detail="currentItem"
      :strategyCode="strategyCode"/>
    <DeleteDialog :dialog.sync="deleteDialog" :id.sync="currentItem.id" @refresh="refresh"/>
  </v-layout>
</template>

<script>
import AddOrUpdateDataIteratorDialog from './AddOrUpdateDataIteratorDialog'
import DeleteDialog from './DeleteDialog'

export default {
  components: {
    AddOrUpdateDataIteratorDialog,
    DeleteDialog
  },
  props: {
    index: [Number, String],
    panel: Array,
    dataSource: Array,
    strategyCode: String,
    loading: Boolean
  },
  watch: {
    panel: {
      handler (n, o) {
        if (!this.panel[this.index]) this.isHandle = false
      },
      deep: true
    }
  },
  data () {
    return {
      dialog: false,
      deleteDialog: false,
      currentId: '',
      isHandle: false,
      currentItem: {},
      isEdit: false
    }
  },
  methods: {
    addHandle () {
      this.isEdit = false
      this.dialog = true
    },
    updateHandle (item) {
      this.isEdit = true
      this.currentItem = item
      this.dialog = true
    },
    deleteHandle (item) {
      this.currentItem = item
      this.deleteDialog = true
    },
    async refresh () {
      this.isHandle = false
      await this.$store.dispatch('position/positionSearch')
    }
  }
}
</script>
<style lang="less">
.card-badge{
  width: 99%;
}
.iterator-card{
  position: relative;
  &__handle{
    position: absolute;
    top: -18px;
    right: -4px;
    .v-btn--icon.v-btn--small{
      width: 24px;
      height: 24px;
    }
  }
}
</style>
