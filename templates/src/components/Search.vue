<template style="font-size: 14px;">
  <main class="flex flex-col">
    <div class="w-full flex items-center flex-col lg:flex-row">
      <div class="flex flex-col md:flex-row w-full lg:w-3/4 space-x-0 lg:space-x-1 ml-0 md:ml-2">
        <Dropdown 
          v-model="selectedlevel" 
          :options="levels" 
          optionLabel="level" 
          placeholder="Уровень" 
          class="w-full md:w-1/3 border border-gray-400 mt-2 md:mt-0" 
          @change="onLevelChange" 
          panelClass="min-w-min w-10rem"
          emptyMessage="Нет доступных опций"
        />
        <Dropdown 
          v-model="selectedfounder" 
          :options="founders" 
          optionLabel="founder" 
          placeholder="Учредитель" 
          class="w-full md:w-1/3 border border-gray-400 mt-2 md:mt-0" 
          @change="onFounderChange" 
          :disabled="!selectedlevel"
          emptyMessage="Нет доступных опций"
        />
        <Dropdown 
          v-model="selectedsphere" 
          :options="spheres" 
          optionLabel="sphere" 
          placeholder="Сфера" 
          class="w-full md:w-1/3 border border-gray-400 mt-2 md:mt-0" 
          @change="StatChange" 
          emptyMessage="Нет доступных опций"
        />
        <Dropdown 
          v-model="selectedzone" 
          :options="zones" 
          optionLabel="zone" 
          placeholder="% выполнения" 
          class="w-full md:w-1/3 border border-gray-400 mt-2 md:mt-0" 
          @change="StatChange"
          emptyMessage="Нет доступных опций"
        />
        <Calendar v-model="dates" dateFormat="dd-mm-yy" selectionMode="range" :manualInput="false" placeholder="Диапазон" showIcon iconDisplay="input" class="w-full md:w-2/3 border border-gray-400 mt-2 md:mt-0 py-2 md:py-0 rounded-lg" @date-select="StatChange" :pt="{input: {class: ['pl-[12px]', 'placeholder:text-gray-500']}}"/>

        <InputText 
          type="text" 
          v-model="searching_name" 
          placeholder="Организация" 
          class="w-full md:w-2/3 border border-gray-400 placeholder:text-gray-500 pl-[12px] py-2 md:py-0 mt-2 md:mt-0" 
          @input="StatChange"
        />
      </div>

      <InputGroup class="w-full lg:w-1/4 flex justify-end space-x-8 pr-2.5">
          <Button icon="pi pi-filter-slash" class="w-10 h-10 bg-slate-100" @click="resetFilters()"></Button>
          <Button icon="pi pi-file-excel" class="w-10 h-10 bg-slate-100" v-tooltip.bottom="'Экспорт в Excel'" @click="exportToExcel()"></Button>
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
          scrollHeight="calc(100vh - 127px)"
          :sortField="'average_fulfillment_percentage'"
          :sortOrder="-1"
          class="mx-0 md:mx-2 mt-3 border border-gray-400"
          tableStyle="min-width: 50rem"
          :pt="DataTableStyle"
        >
        
        <Column
          field="name"
          sortable
          header="Название"
          class="text-xs cursor-pointer text-left"
          style="min-width: 240px;"
          frozen
        >
          <template #body="slotProps">
            <span @click="openDialog(slotProps.data)" class="hover:underline">{{ slotProps.data.name }}</span>
          </template>
        </Column>

        <template>
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
              <i v-if="index == 0 || statisticColumns[index].fulfillment_percentage == statisticColumns[index-1].fulfillment_percentage"></i>

              <i class="pi pi-arrow-up text-green-400 pb-1.4" v-else-if="statisticColumns[index].fulfillment_percentage > statisticColumns[index-1].fulfillment_percentage" ></i>
              <i class="pi pi-arrow-down text-red-600 pb-1.4" v-else></i>
              {{ statisticColumns[index].fulfillment_percentage }}%


            </div>
          </template>
          </Column>
        </template>

        <Column
          field="average_week_fulfillment_percentage"
          sortable
          header="% за неделю"
          class="text-black text-xs text-center"
          v-if="!dates"
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
          header="% за месяц"
          class="text-black text-xs text-center"
          v-if="!dates"
        >
          <template #body="slotProps">
            <Tag v-if="slotProps.data.average_fulfillment_percentage >= 90" severity="success">
              {{ slotProps.data.average_fulfillment_percentage }}%
            </Tag>
            <Tag v-else-if="slotProps.data.average_fulfillment_percentage >= 70" severity="warning">
              {{ slotProps.data.average_fulfillment_percentage }}%
            </Tag>
            <Tag v-else severity="danger">{{ slotProps.data.average_fulfillment_percentage }}%</Tag>
          </template>
        </Column>

        <Column field="members_count" sortable header="Участники" class="text-black text-xs text-center"></Column>

        <Column field="statistic" header="Кол. подписок за день" :sortable="true" class="text-black text-xs text-center">
            <template #body="slotProps">
              <span v-if="slotProps.data.statistic && slotProps.data.statistic.length > 0 && slotProps.data.statistic[slotProps.data.statistic.length - 1].activity">
                {{slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.subscribed}}
              </span>
              <span v-else>0</span>
            </template>
        </Column>
        <Column field="statistic" header="Кол. лайк. за день" :sortable="true" class="text-black text-xs text-center">
            <template #body="slotProps">
              <span v-if="slotProps.data.statistic && slotProps.data.statistic.length > 0 && slotProps.data.statistic[slotProps.data.statistic.length - 1].activity">
                {{slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.likes}}
              </span>
              <span v-else>0</span>
            </template>
        </Column>
        <Column field="statistic" header="Кол. ком. за день" :sortable="true" class="text-black text-xs text-center">
            <template #body="slotProps">
              <span v-if="slotProps.data.statistic && slotProps.data.statistic.length > 0 && slotProps.data.statistic[slotProps.data.statistic.length - 1].activity">
                {{slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.comments}}
              </span>
              <span v-else>0</span>
            </template>
        </Column>

        <Column field="has_gos_badge" sortable header="Гос. метка" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.has_gos_badge"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+10%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>


        <Column field="has_avatar" sortable header="Аватар" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.has_avatar"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+5%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>

        <Column field="has_cover" sortable header="Обложка" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.has_cover"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+10%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>

        <Column field="has_description" sortable header="Описание" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.has_description"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+5%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>

        <Column field="has_widget" sortable header="Виджет" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.has_widget"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+10%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>
        <Column field="connected" sortable header="Подключение" class="text-black text-xs text-center cursor-pointer">
          <template #body="slotProps">
            <i
              v-if="slotProps.data.connected"
              class="pi pi-check-circle"
              style="color: green;"
              v-tooltip="'+10%'"
            ></i>
            <i
              v-else
              class="pi pi-times-circle"
              style="color: red;"
              v-tooltip="'0%'"
            ></i>
          </template>
        </Column>

        <Column field="widget_count" sortable header="Виджеты" class="text-black text-xs text-center cursor-pointer">
            <template #body="slotProps">
              <span
                v-if="slotProps.data.widget_count >= 2"
                v-tooltip="'+10%'"
              >
                {{ slotProps.data.widget_count }}
              </span>
              <span
                v-else-if="slotProps.data.widget_count == 1"
                v-tooltip="'+5%'"
              >
                {{ slotProps.data.widget_count }}
              </span>
              <span
                v-else
                v-tooltip="'0%'"
              >
                {{ slotProps.data.widget_count || "0" }}
              </span>
            </template>
          </Column>

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
import {
  exportToExcel,
  getFounders,
  getSpheresBy,
} from '@/api/statistic.js';

export default {
  data() {
    return {
      loading: false,
      dialogVisible: false,
      previousValues: {},
      DataTableStyle: {
        root: ({ props }) => ({
          class: [
            'relative',
            { 'flex flex-col': props.scrollable && props.scrollHeight === 'flex' },
            { 'h-full': props.scrollable && props.scrollHeight === 'flex' },
            'rounded-lg'
          ]
        }),
        loadingoverlay: {
          class: ['absolute', 'top-0 left-0', 'z-20', 'flex items-center justify-center', 'w-full h-full', 'bg-surface-100/40', 'transition duration-200', 'rounded-lg']
        },
        wrapper: ({ props }) => ({
          class: [
            { relative: props.scrollable, 'flex flex-col grow': props.scrollable && props.scrollHeight === 'flex' },
            { 'h-full': props.scrollable && props.scrollHeight === 'flex' },
            'rounded-lg'
          ]
        }),
        header: ({ props }) => ({
          class: [
            'font-bold',
            props.showGridlines ? 'border-x border-t border-b-0' : 'border-y border-x-0',
            'p-4',
            'bg-surface-50 dark:bg-surface-800',
            'border-surface-200 dark:border-surface-700',
            'text-surface-700 dark:text-white/80',
            'rounded-t-lg'
          ]
        }),
        table: {
          class: 'w-full border-spacing-0 border-separate rounded-lg'
        },
        tbody: ({ instance, context }) => ({
          class: [
            {
              'sticky z-20': instance.frozenRow && context.scrollable
            },
            'bg-surface-50 dark:bg-surface-800 rounded-lg'
          ]
        }),
        footer: {
          class: ['font-bold', 'border-t-0 border-b border-x-0', 'p-4', 'bg-surface-50 dark:bg-surface-800', 'border-surface-200 dark:border-surface-700', 'text-surface-700 dark:text-white/80', 'rounded-b-lg']
        },
        filteroverlay: {
          class: ['absolute top-0 left-0', 'border-0 dark:border', 'rounded-md', 'shadow-md', 'min-w-[12.5rem]', 'bg-surface-0 dark:bg-surface-800', 'text-surface-800 dark:text-white/80', 'dark:border-surface-700', 'rounded-lg']
        },
      },
      selectedlevel: null,
      selectedfounder: null,
      selectedsphere: null,
      selectedzone: null,
      dates: null,
      searching_name: '',
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
    exportToExcel() {
      exportToExcel(this.stats)
      .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'accounts_data.xlsx');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          })
          .catch(error => {
            console.error('Error downloading the file', error);
          });
    },
    openDialog(item) {
      this.selectedItem = item;
      this.dialogVisible = true;
    },
    loadAllData() {
      this.loading = true;
      axios.get('/filter/get_stats')
        .then(response => {
          const items = response.data;
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
        // Изменение сортировки на порядок убывания
        const sortedStatistics = items[0].statistic.sort((a, b) => new Date(b.date_added) - new Date(a.date_added));
        sortedStatistics.forEach((stat, index) => {
          const date = new Date(stat.date_added);
          const formattedDate = date.toLocaleDateString("ru-RU", {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
          statisticColumns.push({ field: `statistic_percentage_${index + 1}`, fulfillment_percentage: sortedStatistics[index].fulfillment_percentage,  header: formattedDate });
        });
      }
      this.statisticColumns = statisticColumns;
      this.memberColumns = memberColumns;
      
      statisticColumns.reverse()
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
    StatChange() {
      this.loadFilteredData();
    },
    getFounders() {
      if (this.selectedlevel) {
        getFounders(this.selectedlevel.level)
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
      getSpheresBy(params)
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
      const nameParam = this.searching_name ? `name=${this.searching_name}` : '';
      const dateFromParam = this.dates && this.dates[0] ? `date_from=${this.formatDate(this.dates[0])}` : '';
      const dateToParam = this.dates && this.dates[1] ? `date_to=${this.formatDate(this.dates[1])}` : '';

      const queryParams = [levelParam, founderParam, sphereParam, zoneParam, nameParam, dateFromParam, dateToParam]
        .filter(param => param !== '')
        .join('&');
        

      axios.get(`/filter/get_stats?${queryParams}`)
        .then(response => {
          const items = response.data;
          this.stats = this.transformData(items);
          this.generateStatisticColumns(items);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching stats:', error);
          this.loading = false;
        });
    },
    formatDate(dateStr) {
      const dateObj = new Date(dateStr);
      const day = String(dateObj.getDate()).padStart(2, '0');
      const month = String(dateObj.getMonth() + 1).padStart(2, '0'); // Months are 0-based
      const year = dateObj.getFullYear();
      return `${year}-${month}-${day}`;
    },
    resetFilters() {
      this.selectedlevel = null;
      this.selectedfounder = null;
      this.selectedsphere = null;
      this.selectedzone = null;
      this.dates = null;
      this.searching_name = '';
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
}
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

.p-datatable .p-datatable-tbody > tr:hover {
    background-color: #f4f4f4;
}

.p-tooltip-text {
    background-color: #fff;
    color: black;
    border: #9ca3af 1px solid;
    border-radius: 4px;
    padding: 8px;
}


.p-dialog-header{
  @apply flex justify-end
}
</style>

