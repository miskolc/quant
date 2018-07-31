<template>
  <v-card class="data-table__card">
    <v-data-table :headers="headers" :items="data" hide-actions class="elevation-1" item-key="name">
      <template slot="headerCell" slot-scope="props">
        <slot name="headerCell" :header="props.header"></slot>
      </template>

  <template slot="headers" slot-scope="props">
    <slot name="headers" :headers="props.headers">
  </slot>
</template>

<template slot="items" slot-scope="props">
    <slot name="items" :indeterminate="props.indeterminate" :all="props.all" :item="props.item"></slot>
</template>
      <!--<template slot="page-text" slot-scope="props">
  <slot name="page-text" :headers="props['page-text']">
  </slot>
</template>-->
<template slot="no-data">
  <slot name="no-data">
  </slot>
</template>

<template slot="no-results">
  <slot name="no-results">
  </slot>
</template>

<template slot="footer">
  <slot name="footer">
  </slot>
</template>
  </v-data-table>
  <v-layout justify-center class="pa-2" v-if="showPage">
        <v-pagination v-model="page" :length="pageTotal" :total-visible="totalVisible" :circle="circlePage||true"/>
      </v-layout>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      page: this.currentPage
    }
  },
  props: {
    data: Array,
    headers: Array,
    showPage: Boolean,
    currentPage: Number,
    circlePage: Boolean,
    totalVisible: {
      type: Number,
      default: 10
    },
    pageCount: {
      type: Number,
      default: 0
    },
    pageSize: {
      type: Number,
      default: 10
    }
  },
  watch: {
    page (n, o) {
      this.$emit('update:currentPage', n)
      this.$emit('current-change', n)
    }
  },
  computed: {
    pageTotal () {
      return Math.ceil(this.pageCount / this.pageSize)
    }
  }
}
</script>
