<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-card-title>
          <span class="headline">{{isEdit?'编辑':'新增'}}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              label="代码"
              :mask="mask"
              v-model="form.code"
              :error-messages="codeError"
              :disabled="isEdit"
              @input="codeCheck"
              @blur="codeCheck"
              required/>
            <v-text-field
              label="名称"
              v-model="form.name"
              disabled/>
            <v-text-field
              label="买入点"
              v-model="form.pointcut"
              :rules="rules.pointcut"
              required/>
           </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click.native="commit" color="info">{{isEdit?'编辑':'新增'}}</v-btn>
          <v-btn @click.native="close">取消</v-btn>
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
              return '请输入正整数或者两位小数'
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
        this.codeError = '代码是必填字段'
        this.form.name = ''
        return
      }
      if (code.length < 6) {
        this.codeError = '代码必须为6位数字'
        this.form.name = ''
        return
      }
      try {
        const data = await this.$store.dispatch('target/stockCode', code)
        this.form.name = data.name || ''
        this.codeError = ''
      } catch (error) {
        this.codeError = '代码不存在'
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
        const {message, description} = error.error
        this.$message.error(description || message)
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
        const {message, description} = error.error
        this.$message.error(description || message)
      }
    },

    close () {
      this.$refs.form.reset()
      this.$emit('update:dialog', false)
    }
  }
}
</script>
