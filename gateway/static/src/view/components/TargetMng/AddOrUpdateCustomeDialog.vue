<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-card-title>
          <span class="headline">custome</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
            label="Code"
            :mask="mask"
            v-model="code"
            :rules="codeRules"
            required></v-text-field>
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
export default {
  data () {
    return {
      valid: true,
      codeRules: [
        v => !!v || `code is required`,
        v => (v && v.length <= 6) || `code must be less than 6 characters`
      ],
      code: ''
    }
  },
  props: {
    dialog: Boolean
  },
  computed: {
    mask () {
      let mask = ''
      for (let index = 0; index < 6; index++) {
        mask += '#'
      }
      return mask
    }
  },
  methods: {
    commit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        this.addCustome()
      }
    },
    addCustome () {
      console.log(this.code)
    },
    updateCustome () {
      console.log('updateCustome')
    },
    close () {
      this.$refs.form.reset()
      this.$emit('update:dialog', false)
    }
  }
}
</script>
