<template>
  <div>
    <v-layout row justify-space-between align-center>
      <v-flex>
        <div class="handler-btn" :style="{
          'padding-bottom':'10px'
        }">
          <v-btn @click="addCustome" color="info">new</v-btn>
          <v-btn @click="openDelete(true)" :disabled="!selected.length">delete</v-btn>
        </div>
      </v-flex>
    </v-layout>
    <v-data-table v-model="selected"
      :headers="headers"
      :items="dataSource"
      :loading="loading"
      hide-actions
      select-all
      item-key="id"
      class="elevation-1">
      <template slot="items" slot-scope="props">
        <tr :active="props.selected">
          <td>
            <v-checkbox
              color="info"
              @click="props.selected = !props.selected"
              :input-value="props.selected"
              primary
              hide-details
            ></v-checkbox>
          </td>
          <td>{{ props.item.code }}</td>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.price | toFixed }}</td>
          <td>{{ props.item.pointcut | toFixed }}</td>
          <td>
            <v-btn flat icon @click="openUpdate(props.item)">
              <v-icon>edit</v-icon>
            </v-btn>
            <v-btn flat icon color="red" @click="openDelete(false,props.item)">
              <v-icon>delete_outline</v-icon>
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
    <AddOrUpdateCustomeDialog :isEdit="isEdit"
    :detail="currentItem"
    :dialog.sync="customeDialog"
    :strategyCode="strategyCode"
    @refresh="refresh"/>
    <DeleteDialog :dialog.sync="deleteDialog" :ids.sync="ids" @refresh="refresh"/>
  </div>
</template>

<script>
import AddOrUpdateCustomeDialog from './AddOrUpdateCustomeDialog'
import DeleteDialog from './DeleteDialog'
export default {
  components: {
    DeleteDialog,
    AddOrUpdateCustomeDialog
  },
  props: {
    dataSource: Array,
    loading: Boolean,
    strategyCode: String
  },
  data () {
    return {
      customeDialog: false,
      updateCustomeDialog: false,
      deleteDialog: false,
      ids: [],
      currentItem: {},
      selected: [],
      headers: [
        { text: 'code', value: 'code' },
        { text: 'name', value: 'name', sortable: false },
        { text: 'price', value: 'price', sortable: false },
        { text: 'pointcut', value: 'pointcut', sortable: false },
        { text: 'handler', sortable: false }
      ],
      isEdit: false
    }
  },
  methods: {
    addCustome () {
      this.isEdit = false
      this.customeDialog = true
    },
    openUpdate (item) {
      this.currentItem = {...item}
      this.isEdit = true
      this.customeDialog = true
    },
    openDelete (multiple = false, item) {
      this.ids = []
      if (!multiple) this.ids = [item]
      if (multiple) this.ids = this.selected

      this.deleteDialog = true
    },
    refresh () {
      this.selected = []
      this.$emit('refresh')
    }
  }
}
</script>
