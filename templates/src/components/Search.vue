<template>
  <main class="flex flex-col">
    <div class="flex items-center flex-col lg:flex-row">
      <InputGroup class="flex flex-col md:flex-row w-full lg:w-1/2 space-x-0 lg:space-x-1 ml-0 md:ml-2">
        <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-1/3 border border-gray-400" @change="onLevelChange" panelClass="min-w-min w-10rem"/>
        <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-1/3 border border-gray-400" @change="onFounderChange" :disabled="!selectedlevel"/>
        <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-1/3 border border-gray-400" @change="onSphereChange" />
        <Dropdown v-model="selectedzone" :options="zones" optionLabel="zone" placeholder="% выполнения" class="w-full md:w-1/3 border border-gray-400" @change="onZoneChange"/>
      </InputGroup>
      <InputGroup class="w-full lg:w-1/2 flex justify-end space-x-8 pr-2.5">
          <Button icon="pi pi-filter-slash" class="w-10 h-10 bg-slate-100" @click="resetFilters()"></Button>
          <Button icon="pi pi-sign-out" class="w-10 h-10 bg-slate-100" @click="SignOut()"></Button>
      </InputGroup>
    </div>
    <DataTable
        :value="stats"
        :loading="loading"
        paginator
        :rows="20"
        :rowsPerPageOptions="[20, 50]"
        removableSort
        scrollable
        scrollHeight="calc(100vh - 121px)"
        :sortField="'average_fulfillment_percentage'"
        :sortOrder="-1"
        class="mx-0 md:mx-2.5 mt-1 border rounded-lg"
        tableStyle="min-width: 50rem"
        :pt="DataTableStyle"
      >
        <Column
          field="name"
          sortable
          header="Название"
          class="text-xs cursor-pointer text-center"
          style="min-width: 240px;"
          frozen
        >
          <template #body="slotProps">
            <span @click="openDialog(slotProps.data)" class="hover:underline">{{ slotProps.data.name }}</span>
          </template>
        </Column>

        <Column
          v-for="(col, index) in statisticColumns"
          :key="index"
          :field="col.field"
          sortable
          :header="col.header"
          class="text-black text-xs text-center"
        >
          <template #body="slotProps">
            <div class="flex justify-center items-center">
              {{ slotProps.data[col.field] }}%
            </div>
          </template>
        </Column>

        <Column
          field="average_week_fulfillment_percentage"
          sortable
          header="% Вып-я недели"
          class="text-black text-xs text-center"
        >
          <template #body="slotProps">
            <Tag v-if="slotProps.data.average_week_fulfillment_percentage >= 90" severity="success">
              {{ slotProps.data.average_fulfillment_percentage }}%
            </Tag>
            <Tag v-else-if="slotProps.data.average_week_fulfillment_percentage >= 70" severity="warning">
              {{ slotProps.data.average_week_fulfillment_percentage }}%
            </Tag>
            <Tag v-else severity="danger">{{ slotProps.data.average_week_fulfillment_percentage }}%</Tag>
          </template>
        </Column>

        <Column
          field="average_fulfillment_percentage"
          sortable
          header="% Вып-я месяца"
          class="text-black text-xs text-center"
        >
          <template #body="slotProps">
            <Tag v-if="slotProps.data.average_fulfillment_percentage >= 90" severity="success">
              {{ slotProps.data.average_fulfillment_percentage }}%
            </Tag>
            <Tag v-else-if="slotProps.data.average_fulfillment_percentage >= 70" severity="warning">
              {{ slotProps.data.average_week_fulfillment_percentage }}%
            </Tag>
            <Tag v-else severity="danger">{{ slotProps.data.average_week_fulfillment_percentage }}%</Tag>
          </template>
        </Column>

        <Column field="members_count" sortable header="Участники" class="text-black text-xs text-center"></Column>
        <Column field="has_avatar" sortable header="Аватар" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.has_avatar" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
        <Column field="has_cover" sortable header="Обложка" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.has_cover" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
        <Column field="has_description" sortable header="Описание" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.has_description" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
        <Column field="has_gos_badge" sortable header="Гос. метка" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.has_gos_badge" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
        <Column field="has_widget" sortable header="Виджет" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.has_widget" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
        <Column field="widget_count" sortable header="Виджеты" class="text-black text-xs text-center"></Column>
        <Column field="posts" sortable header="Посты" class="text-black text-xs text-center"></Column>
        <Column field="posts_1d" sortable header="1 день" class="text-black text-xs text-center"></Column>
        <Column field="posts_7d" sortable header="7 дней" class="text-black text-xs text-center"></Column>
        <Column field="posts_30d" sortable header="30 дней" class="text-black text-xs text-center"></Column>
        <Column field="date_added" sortable header="Дата сбора" class="text-black text-xs text-center"></Column>
        <Column field="level" sortable header="Уровень" class="text-black text-xs text-center"></Column>
        <Column field="founder" sortable header="Учред." class="text-black text-xs text-center"></Column>
        <Column field="activity" sortable header="Тип" class="text-black text-xs text-center"></Column>

        <template #empty>
          <tr>
            <td colspan="30" class="text-center p-4">
              Ничего не найдено
            </td>
          </tr>
        </template>
      </DataTable>

    <Dialog v-model:visible="dialogVisible" :style="{ width: '25rem' }" :modal="true" :closable="true">
      <div class="space-y-2">
        <div class="text-black">
          <h2 class="font-bold">Название</h2>
          <p v-if="!selectedItem['name']" class="text-gray-500">Нет информации</p>
          <p class="text-sm text-gray-500">{{ selectedItem["name"] }}</p>
        </div>
        <div class="text-black">
          <h2 class="font-bold">Ссылка</h2>
          <a class="text-blue-300 hover:underline cursor-pointer" :href="selectedItem['url']" target="_blank">{{ selectedItem["url"] }}</a>
        </div>
        <div class="text-black">
          <h2 class="font-bold">ОГРН</h2>
          <p v-if="!selectedItem['the_main_state_registration_number']" class="text-gray-500">Нет информации</p>
          <p class="text-gray-500">{{ selectedItem["the_main_state_registration_number"] }}</p>
        </div>
        <div class="text-black">
          <h2 class="font-bold">Статус</h2>
          <p v-if="!selectedItem['status']" class="text-gray-500">Нет информации</p>
          <p class="text-gray-500">{{ selectedItem["status"] }}</p>
        </div>
        <div class="text-black">
          <h2 class="font-bold">ID</h2>
          <p class="text-gray-500">{{ selectedItem["channel_id"] }}</p>
        </div>
        <div class="text-black">
          <h2 class="font-bold">Город</h2>
          <p v-if="!selectedItem['city']" class="text-gray-500">Нет информации</p>
          <p class="text-gray-500">{{ selectedItem["city"] }}</p>
        </div>
      </div>
    </Dialog>
  </main>
</template>

<script>
import VueCookies from 'vue-cookies';
import axios from 'axios';

export default {
  data() {
    return {
      loading: false,
      dialogVisible: false,
      DataTableStyle: {
        loadingoverlay: {
          class: ['absolute', 'top-0 left-0', 'z-20', 'flex items-center justify-center', 'w-full h-full', 'bg-surface-100/40', 'transition duration-200'],
        },
      },
      selectedlevel: null,
      selectedfounder: null,
      selectedsphere: null,
      selectedzone: null,
      founders: [],
      spheres: [],
      zones: [
        { zone: '90-100%' },
        { zone: '70-89%' },
        { zone: '0-69%' },
      ],
      levels: [
        { level: 'Регион' },
        { level: 'Министерство' },
        { level: 'МО' },
        { level: 'Ведомство' },
        { level: 'Законодательный орган' },
        { level: 'Другое' },
        { level: 'ВУЗ' },
      ],
      stats: [],
      statisticColumns: [],
      memberColumns: [],
      selectedItem: {},
    };
  },
  mounted() {
    this.loadAllData();
    this.getSpheres();
  },
  methods: {
    openDialog(item) {
      this.selectedItem = item;
      this.dialogVisible = true;
    },
    loadAllData() {
      this.loading = true;
      axios.get('/filter/get_stats')
        .then(response => {
          const items = response.data[0].items;
          this.stats = this.transformData(items);
          this.generateStatisticColumns(items);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching stats:', error);
          this.loading = false;
        });
    },
    transformData(items) {
      return items.map(item => {
        const newItem = { ...item };
        if (item.statistic) {
          item.statistic.forEach((stat, index) => {
            newItem[`statistic_percentage_${index + 1}`] = stat.fulfillment_percentage;
            newItem[`statistic_members_count_${index + 1}`] = stat.members_count;
          });
        }
        return newItem;
      });
    },
    generateStatisticColumns(items) {
      const statisticColumns = [];
      const memberColumns = [];
      if (items.length > 0 && items[0].statistic) {
        // Сортировка по возрастанию дат
        const sortedStatistics = items[0].statistic.sort((a, b) => new Date(a.date_added) - new Date(b.date_added));
        sortedStatistics.forEach((stat, index) => {
          const date = new Date(stat.date_added);
          const formattedDate = date.toLocaleDateString("ru-RU", {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
          statisticColumns.push({ field: `statistic_percentage_${index + 1}`, header: formattedDate });
          memberColumns.push({ field: `statistic_members_count_${index + 1}`, header: formattedDate });
        });
      }
      this.statisticColumns = statisticColumns;
      this.memberColumns = memberColumns;
    },
    onLevelChange() {
      this.selectedfounder = null;
      this.selectedsphere = null;
      this.getFounders();
      this.getSpheres();
      this.loadFilteredData();
    },
    onFounderChange() {
      this.selectedsphere = null;
      this.getSpheres();
      this.loadFilteredData();
    },
    onSphereChange() {
      this.loadFilteredData();
    },
    onZoneChange() {
      this.loadFilteredData();
    },
    getFounders() {
      if (this.selectedlevel) {
        axios.get(`/filter/get_founders?level=${this.selectedlevel.level}`)
          .then(response => {
            this.founders = response.data;
          })
          .catch(error => {
            console.error('Error fetching founders:', error);
          });
      } else {
        this.founders = [];
      }
    },
    getSpheres() {
      const params = {};
      if (this.selectedfounder) {
        params.founder = this.selectedfounder.founder;
      }
      if (this.selectedlevel) {
        params.level = this.selectedlevel.level;
      }
      axios.get('/filter/get_spheres_by', { params })
        .then(response => {
          this.spheres = response.data;
        })
        .catch(error => {
          console.error('Error fetching spheres:', error);
        });
    },
    loadFilteredData() {
      this.loading = true;
      const levelParam = this.selectedlevel ? `level=${this.selectedlevel.level}` : '';
      const founderParam = this.selectedfounder ? `founder=${this.selectedfounder.founder}` : '';
      const sphereParam = this.selectedsphere ? `sphere=${this.selectedsphere.sphere}` : '';
      const zoneParam = this.selectedzone ? `zone=${this.selectedzone.zone}` : '';

      const queryParams = [levelParam, founderParam, sphereParam, zoneParam]
        .filter(param => param !== '')
        .join('&');

      axios.get(`/filter/get_stats?${queryParams}`)
        .then(response => {
          const items = response.data[0].items;
          this.stats = this.transformData(items);
          this.generateStatisticColumns(items);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching stats:', error);
          this.loading = false;
        });
    },
    resetFilters() {
      this.selectedlevel = null;
      this.selectedfounder = null;
      this.selectedsphere = null;
      this.selectedzone = null;
      this.founders = [];
      this.spheres = [];
      this.stats = [];
      this.loadAllData();
    },
    SignOut() {
      VueCookies.remove('token');
      this.$router.push('/login');
    }
  }
};
</script>







<style>
html{
  scrollbar-width: thin;
}

.p-paginator-page.p-highlight {
    background-color: #3b82f6;
    color: white;
    border: none;
}

.p-datatable-wrapper{
  scrollbar-width: thin;
}


.p-dialog-header{
  @apply flex justify-end
}
</style>

