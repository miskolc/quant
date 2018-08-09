<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title primary-title>确认删除</v-card-title>
        <v-card-text>确认删除选中股票？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click.native="commit" color="info">确定</v-btn>
          <v-btn @click.native="close">取消</v-btn>
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
    ids: Array
  },
  methods: {
    async commit () {
      try {
        let idlist = []
        const ids = this.ids || []
        ids.forEach(item => {
          idlist.push(item.id)
        })
        await this.$store.dispatch('target/targetDelete', idlist)
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
