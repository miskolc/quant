<template>
  <v-app id="inspire" dark>
    <v-navigation-drawer
      fixed
      app>
      <v-list dense>
        <template v-for="item in items">
          <v-layout
            v-if="item.heading"
            :key="item.heading"
            row
            align-center
          >
            <v-flex xs6>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
            <v-flex xs6 class="text-xs-center">
              <a href="#!" class="body-2 black--text">EDIT</a>
            </v-flex>
          </v-layout>
          <v-list-group
            v-else-if="item.children"
            v-model="item.model"
            :key="item.text"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon=""
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
              v-for="(child, i) in item.children"
              :key="i"
              @click="skipPage(child.path)"
              :class="{'url-active':currentPath===child.path}"
            >
              <v-list-tile-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ child.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
          <v-list-tile v-else :key="item.text" @click="skipPage(item.path)"
              :class="{'url-active':currentPath === item.path}">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar dark fixed app>
      <v-toolbar-title>Stock</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout>
          <v-flex text-xs-left>
            <slot></slot>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer app>
      <span class="white--text">&copy; 2018</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      routes: [],
      items: [
        // {
        //   icon: 'keyboard_arrow_up',
        //   'icon-alt': 'keyboard_arrow_down',
        //   text: 'Target Mng',
        //   model: true,
        //   children: [
        //     { text: 'panel1', path: '/target/panel1' },
        //     { text: 'panel2', path: '/target/panel2' }
        //     // { icon: 'add', text: 'Create label' }
        //   ]
        // },
        { icon: 'keyboard_arrow_down', text: 'Target Mng', path: '/target/mng' },
        { icon: 'contacts', text: 'Position Mng', path: '/position/mng' }
      ]
    }
  },
  computed: {
    currentPath () {
      return this.$route.path
    }
  },
  methods: {
    skipPage (path) {
      if (path) return this.$router.push(path)
      console.log(1)
    }
  },
  mounted () {
    const {routes} = this.$router.options
    console.log()
    for (const key in routes) {
      if (routes[key].path === '/') this.routes = routes[key].children
    }
  }
}
</script>
<style lang="less">
.url-active{
  a{
    color: red
  }
}
</style>
