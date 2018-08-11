<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-card-title>
          <span class="headline">{{isEdit?'Edit':'New'}}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              label="code"
              :mask="mask"
              v-model="form.code"
              :error-messages="codeError"
              :disabled="isEdit"
              @input="codeCheck"
              @blur="codeCheck"
              required/>
            <v-text-field
              label="name"
              v-model="form.name"
              disabled/>
            <v-text-field
              label="pointcut"
              v-model="form.pointcut"
              :rules="rules.pointcut"
              required/>
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
import {errormsg} from '@utils/filters.js'
export default {
  data () {
    return {
      valid: true,
      form: {
        code: '',
        name: '',
        pointcut: '',
        strategy_code: ''
      },
      rules: {
        pointcut: [
          v => {
            const reg = /^[0-9]+([.]{1}[0-9]{1,2})?$/
            if (!v) return true
            if (!reg.test(v)) {
              return 'please enter a positive integer or two decimal places'
            }
            return true
          }
        ]
      },
      codeError: ''
    }
  },
  props: {
    dialog: Boolean,
    strategyCode: String,
    isEdit: Boolean,
    detail: Object
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
  watch: {
    dialog (n, o) {
      this.codeError = ''
      let { strategyCode } = this
      this.form.strategy_code = strategyCode
    },
    detail: {
      handler (n, o) {
        let {detail, strategyCode} = this
        if (this.isEdit) {
          this.form = {
            code: detail.code,
            name: detail.name,
            pointcut: detail.pointcut,
            strategy_code: strategyCode
          }
        }
      },
      deep: true
    }
  },
  methods: {
    async codeCheck () {
      const {code} = this.form
      if (!code) {
        this.codeError = 'code is required'
        this.form.name = ''
        return
      }
      if (code.length < 6) {
        this.codeError = 'the code must be 6 digits'
        this.form.name = ''
        return
      }
      try {
        const data = await this.$store.dispatch('target/stockCode', code)
        this.form.name = data.name || ''
        this.codeError = ''
      } catch (error) {
        this.codeError = 'code does not exist'
      }
    },
    async commit () {
      this.codeCheck()
      if (this.$refs.form.validate()) {
        if (this.codeError) return false
        let params = {...this.form}
        params.strategy_code = this.strategyCode
        params.pointcut = Number(params.pointcut) || null
        if (!this.isEdit) return this.addCustome(params)
        this.updateCustome(params)
      }
    },
    async addCustome (params) {
      try {
        await this.$store.dispatch('target/targetAdd', params)
        this.$emit('refresh')
        this.$message.success('create successfully')
        this.close()
      } catch (error) {
        this.$message.error(errormsg(error.error))
      }
    },
    async updateCustome (params) {
      const {id} = this.detail
      const {pointcut} = params
      try {
        await this.$store.dispatch('target/targetUpdate', {id, pointcut})
        this.$message.success('update successfully')
        this.$emit('refresh')
        this.close()
      } catch (error) {
        this.$message.error(errormsg(error.error))
      }
    },

    close () {
      this.$refs.form.reset()
      this.$emit('update:dialog', false)
    }
  }
}
</script>
