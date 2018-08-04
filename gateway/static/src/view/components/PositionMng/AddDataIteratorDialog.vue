<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-card-title>
          <span class="headline">position</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-layout wrap justify-center>
              <v-flex xs12>
                <v-select :items="[{
                  text:'root',
                  value:1
                },{
                  text:'admin',
                  value:2
                }]"
                :rules="selectRules"
                label="Target" required/>
              </v-flex>
              <v-flex xs12>
              <v-text-field
                label="Cone"
                v-model="form.code"
                :rules="nameRules"
                required/>
              </v-flex>
            </v-layout>
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
      form: {
        code: ''
      },
      valid: true,
      selectRules: [
        v => !!v || `Target is required`
      ],
      nameRules: [
        v => !!v || `Cone is required`,
        v => (v && v.length <= 6) || `name must be less than 6 characters`
      ],
      code: ''
    }
  },
  props: {
    dialog: Boolean,
    isEdit: Boolean
  },
  methods: {
    commit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        !this.isEdit && this.addCustome()
        this.isEdit && this.updateCustome()
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
