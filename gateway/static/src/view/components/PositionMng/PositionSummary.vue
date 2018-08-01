<template>
  <v-layout wrap>
    <v-layout row justify-space-between align-center>
      <v-flex>
        <div class="search-input">
          <v-text-field label="Search" prepend-icon="search" clearable clear-icon="cancel" single-line/>
        </div>
      </v-flex>
      <v-flex>
        <div class="handler-btn">
          <v-btn light @click="dialog=true">add</v-btn>
          <v-btn light @click="isDelete=!isDelete">delete</v-btn>
        </div>
      </v-flex>
    </v-layout>
    <v-container fluid grid-list-md>
      <v-data-iterator :items="items" :rows-per-page-items="rowsPerPageItems" :pagination.sync="pagination" content-tag="v-layout" row wrap>
        <v-flex slot="item" slot-scope="props" xs12 sm6 md4 lg3>
          <v-card>
            <v-badge overlap v-model="isDelete" color="red">
              <v-btn icon small slot="badge">
                <v-icon dark small>clear</v-icon>
              </v-btn>
              <v-card-title>
                <h4>{{ props.item.name }}</h4>
              </v-card-title>
            </v-badge>
            <v-divider></v-divider>
            <v-list dense>
              <v-list-tile>
                <v-list-tile-content>Calories:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.calories }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Fat:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.fat }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Carbs:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.carbs }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Protein:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.protein }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Sodium:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.sodium }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Calcium:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.calcium }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>Iron:</v-list-tile-content>
                <v-list-tile-content class="align-end">{{ props.item.iron }}</v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
      </v-data-iterator>
    </v-container>
    <AddPositionGropDialog :dialog.sync="dialog" />
  </v-layout>
</template>

<script>
import AddPositionGropDialog from './AddPositionGropDialog'
export default {
  components: {
    AddPositionGropDialog
  },
  data () {
    return {
      dialog: false,
      isDelete: false,
      rowsPerPageItems: [4, 8, 12],
      pagination: {
        rowsPerPage: 4
      },
      items: [{
        value: false,
        name: 'Frozen Yogurt',
        calories: 159,
        fat: 6.0,
        carbs: 24,
        protein: 4.0,
        sodium: 87,
        calcium: '14%',
        iron: '1%'
      },
      {
        value: false,
        name: 'Ice cream sandwich',
        calories: 237,
        fat: 9.0,
        carbs: 37,
        protein: 4.3,
        sodium: 129,
        calcium: '8%',
        iron: '1%'
      },
      {
        value: false,
        name: 'Eclair',
        calories: 262,
        fat: 16.0,
        carbs: 23,
        protein: 6.0,
        sodium: 337,
        calcium: '6%',
        iron: '7%'
      },
      {
        value: false,
        name: 'Cupcake',
        calories: 305,
        fat: 3.7,
        carbs: 67,
        protein: 4.3,
        sodium: 413,
        calcium: '3%',
        iron: '8%'
      },
      {
        value: false,
        name: 'Gingerbread',
        calories: 356,
        fat: 16.0,
        carbs: 49,
        protein: 3.9,
        sodium: 327,
        calcium: '7%',
        iron: '16%'
      },
      {
        value: false,
        name: 'Jelly bean',
        calories: 375,
        fat: 0.0,
        carbs: 94,
        protein: 0.0,
        sodium: 50,
        calcium: '0%',
        iron: '0%'
      },
      {
        value: false,
        name: 'Lollipop',
        calories: 392,
        fat: 0.2,
        carbs: 98,
        protein: 0,
        sodium: 38,
        calcium: '0%',
        iron: '2%'
      },
      {
        value: false,
        name: 'Honeycomb',
        calories: 408,
        fat: 3.2,
        carbs: 87,
        protein: 6.5,
        sodium: 562,
        calcium: '0%',
        iron: '45%'
      },
      {
        value: false,
        name: 'Donut',
        calories: 452,
        fat: 25.0,
        carbs: 51,
        protein: 4.9,
        sodium: 326,
        calcium: '2%',
        iron: '22%'
      },
      {
        value: false,
        name: 'KitKat',
        calories: 518,
        fat: 26.0,
        carbs: 65,
        protein: 7,
        sodium: 54,
        calcium: '12%',
        iron: '6%'
      }
      ]
    }
  },
  methods: {
    add () {}
  }
}
</script>
