<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title primary-title>Confirm</v-card-title>
        <v-card-text>Confirm deletion of selected stocks?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click.native="commit" color="info">ok</v-btn>
          <v-btn @click.native="close">cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
import {errormsg} from '@utils/filters.js'
export default {
  props: {
    dialog: Boolean,
    id: [String, Number]
  },
  methods: {
    async commit () {
      try {
        await this.$store.dispatch('position/positionDelete', this.id)
        this.$message.success('delete successfully')
        this.$emit('refresh')
        this.close()
      } catch (error) {
        this.$message.error(errormsg(error.error))
      }
    },
    close () {
      this.$emit('update:dialog', false)
    }
  }
}
</script>
