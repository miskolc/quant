<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-card-title>
          <span class="headline">strategy {{strategyCode}}</span>
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
              disabled
              v-if="form.name"/>
            <v-text-field
              label="price in"
              v-model="form.price_in"
              :rules="rules.price_in"
              required/>
              <v-text-field
              label="shares"
              v-model="form.shares"
              :rules="rules.shares"
              required/>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click.native="commit" color="info">{{isEdit?'edit':'new'}}</v-btn>
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
      form: {
        code: '',
        name: '',
        strategy_code: '',
        shares: '',
        price_in: ''
      },
      valid: true,
      rules: {
        price_in: [
          v => {
            const reg = /^[0-9]+([.]{1}[0-9]{1,3})?$/
            if (!v) return 'price in is required'
            if (!reg.test(v)) {
              return 'please enter a positive integer or two decimal places'
            }
            return true
          }
        ],
        shares: [
          v => {
            const reg = /^[1-9]\d*00$/
            if (!v) return 'shares is required'
            if (!reg.test(v)) {
              return 'please enter a value of 100'
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
    isEdit: Boolean,
    strategyCode: String,
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
    dialog () {
      this.codeError = ''
    },
    detail: {
      handler (n, o) {
        let {detail, strategyCode} = this
        if (this.isEdit) {
          this.form = {
            code: detail.code,
            name: detail.name,
            shares: detail.shares,
            price_in: detail.price_in,
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
        this.form.name = ''
        this.codeError = 'the code must be 6 digits'
        return
      }
      try {
        const data = await this.$store.dispatch('position/stockCode', code)
        this.form.name = data.name || ''
        this.codeError = ''
      } catch (error) {
        this.codeError = 'code does not exist'
      }
    },
    commit () {
      this.codeCheck()
      if (this.$refs.form.validate()) {
        if (this.codeError) return false
        this.$emit('refresh')
        let params = {...this.form}
        params.strategy_code = this.strategyCode
        params.shares = Number(params.shares)
        params.price_in = Number(params.price_in)
        !this.isEdit && this.addPosition(params)
        this.isEdit && this.updatePosition(params)
      }
    },
    async addPosition (params) {
      try {
        await this.$store.dispatch('position/positionAdd', params)
        this.$emit('refresh')
        this.$message.success('create successfully')
        this.close()
      } catch (error) {
        const {message, description} = error.error
        this.$message.error(description || message)
      }
    },
    async updatePosition (params) {
      const {id} = this.detail
      try {
        await this.$store.dispatch('position/positionUpdate', {
          id,
          price_in: params.price_in,
          shares: params.shares
        })
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
