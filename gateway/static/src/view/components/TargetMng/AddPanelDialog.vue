<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">add {{title}}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field v-if="!isTartget" label="panel name" :rules="nameRules" required></v-text-field>
            <template v-else>
                    <v-select :items="['0-17', '18-29', '30-54', '54+']" label="select panel" required></v-select>
                    <v-text-field label="target name" :rules="nameRules" required></v-text-field>
            </template>
           </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click.native="commit" color="info">commit</v-btn>
          <v-btn @click.native="close">cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      valid: true,
      nameRules: [
        v => !!v || `${this.title} name is required`,
        v => (v && v.length <= 10) || `${this.title} name must be less than 10 characters`
      ]
    }
  },
  props: {
    dialog: Boolean,
    isTartget: Boolean
  },
  computed: {
    title () {
      return this.isTartget ? 'Target' : 'Panel'
    }
  },
  methods: {
    commit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        axios.post('/api/submit', {
          name: this.name,
          email: this.email,
          select: this.select,
          checkbox: this.checkbox
        })
      }!this.isTartget && this.addPanel()
      this.isTartget && this.addTarget()
    },
    addPanel () {
      console.log('addPanel')
    },
    addTarget () {
      console.log('addTarget')
    },
    close () {
      this.$refs.form.reset()
      this.$emit('update:dialog', false)
    }
  }
}
</script>
