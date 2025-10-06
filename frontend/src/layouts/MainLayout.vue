<template>
  <q-layout view="hHh LpR fFf">
    <q-header class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <strong>Azure Tables</strong>
        </q-toolbar-title>
        <q-btn flat round dense icon="ion-logo-github" @click="openGithub()"/>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" :width=400>
      <div class="q-table-filter">
        <q-input square filled dense v-model="tableFilter">
          <template v-slot:append>
            <q-icon v-if="tableFilter === ''" name="search" />
            <q-icon v-else name="clear" class="cursor-pointer" @click="tableFilter = ''" />
          </template>
        </q-input>
      </div>
      <q-scroll-area style="height: 100%; max-width: 400px;">
        <q-list dense class="rounded-borders q-tables-list">
          <q-item
            clickable
            v-ripple
            v-for="table in tablesFiltered" v-bind:key="table['properties']['schema']['name']"
            @click="selectTable(table)"
          >
            <q-item-section class="q-icon-section">
              <q-icon name="table_view" size="20px"/>
            </q-item-section>
            <q-item-section class="q-table-name-section">
              {{ table["properties"]["schema"]["name"] }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <template v-if="selectedTable !== null">
        <div class="q-table-container">
          <q-card flat style="height: 100%;">
            <q-card-section>
              <div class="text-h6">
                <q-icon name="data_object" size="25px"/>
                {{ selectedTable["properties"]["schema"]["name"] }}
              </div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <q-badge
                class="q-solution-badge"
                color="primary"
                v-for="solution in selectedTable['properties']['schema']['solutions']"
                v-bind:key="solution"
              >
                {{ solution }}
              </q-badge>
            </q-card-section>

            <q-card-section>
              <q-markup-table flat dense>
                <thead>
                  <tr>
                    <th class="text-left">Column Name</th>
                    <th class="text-left">Data Type</th>
                    <th class="text-left">Hidden</th>
                    <th class="text-left">Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="column in selectedTable['properties']['schema']['standardColumns']"
                    v-bind:key="selectedTable['properties']['schema']['name'] + '.' + column['name']"
                  >
                    <td class="text-left">{{ column['name'] }}</td>
                    <td class="text-left"><q-badge color="grey-7">{{ column['type'] }}</q-badge></td>
                    <td class="text-left">{{ column['isHidden'] }}</td>
                    <td class="text-left" v-if="column['description']">{{ column['description'] }}</td>
                    <td class="text-left" v-else>-</td>
                  </tr>
                </tbody>
              </q-markup-table>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, watch } from 'vue';
import { useQuasar } from 'quasar';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const leftDrawerOpen = ref(false);
const tables = ref([]);
const tableFilter = ref("");
const selectedTable = ref(null);
const $q = useQuasar();

const toggleLeftDrawer = () => leftDrawerOpen.value = !leftDrawerOpen.value;

const selectTable = (table) => {
  selectedTable.value = table;
  router.push({
    query: {
      ...route.query,
      selected: selectedTable.value["properties"]["schema"]["name"]
    }
  });
};

const tablesFiltered = computed(() => {
  let filter = tableFilter.value;
  if (!filter.length) return tables.value;

  // The .filter function doesn't work here for some reason
  const filtered = [];
  tables.value.forEach((table) => {
    if (table["properties"]["schema"]["name"].includes(filter))
      filtered.push(table);
  });
  return filtered;
});

const findTableByName = (name) => {
  let foundTable = null;
  tables.value.forEach((table) => {
    if (table["properties"]["schema"]["name"].trim() == name.trim()) {
      foundTable = table;
    }
  });
  return foundTable;
}

const openGithub = () => {
  window.open("https://github.com/Null0x47/azure-tables", "_blank");
}

axios.get('https://raw.githubusercontent.com/Null0x47/azure-tables/refs/heads/main/tables.json')
  .then((response) => {
    tables.value = response.data.sort((a, b) => {
      if (a["properties"]["schema"]["name"] < b["properties"]["schema"]["name"]) { return -1; }
      if (a["properties"]["schema"]["name"] > b["properties"]["schema"]["name"]) { return 1; }
      return 0;
    });

    if (!("selected" in route.query)) {
      selectedTable.value = tables.value[0];
    } else {
      const selected = route.query.selected;
      const table = findTableByName(selected);
      if (table !== null) {
        selectTable(table);
      } else {
        selectedTable.value = tables.value[0];
      }
    }

    if ("filter" in route.query) {
      tableFilter.value = route.query.filter;
    }
  }).catch((error) => $q.notify(error));

watch(tableFilter, (n, o) => {
  if (n !== o) {
    router.push({
      query: {
        ...route.query,
        filter: n
      }
    });
  }
});

</script>
