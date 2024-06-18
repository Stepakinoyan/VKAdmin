<template>
    <main class="flex flex-col-reverse mt-2">
      <DataTable
        :value="stats"
        :loading="loading"
        paginator
        :rows="20"
        :rowsPerPageOptions="[20, 50]"
        removableSort
        scrollable
        scrollHeight="calc(100vh - 153px)"
        :sortField="'fulfillment_percentage'"
        :sortOrder="-1"
        class="ml-2.5"
        tableStyle="min-width: 50rem"
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
        <Column
          field="fulfillment_percentage"
          sortable
          header="% Вып-я"
          class="text-black text-xs text-center px-0.5"
        >
          <template #body="slotProps">
            <Tag v-if="slotProps.data.fulfillment_percentage >= 90" severity="success">
              {{ slotProps.data.fulfillment_percentage }}%
            </Tag>
            <Tag v-else-if="slotProps.data.fulfillment_percentage >= 70" severity="warn">
              {{ slotProps.data.fulfillment_percentage }}%
            </Tag>
            <Tag v-else severity="danger">{{ slotProps.data.fulfillment_percentage }}%</Tag>
          </template>
        </Column>
        <Column
          v-for="(col, index) in statisticColumns"
          :key="index"
          :field="col.field"
          sortable
          :header="col.header"
          class="text-black text-xs text-center"
        ></Column>
        <Column field="members_count" sortable header="Участники" class="text-black text-xs text-center"></Column>
        <Column field="verified" sortable header="Проверен" class="text-black text-xs text-center">
          <template #body="slotProps" style="font-size: 1.5rem">
            <i v-if="slotProps.data.verified" class="pi pi-check-circle" style="color: green;"></i>
            <i v-else class="pi pi-times-circle" style="color: red;"></i>
          </template>
        </Column>
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
  
      <Dialog v-model:visible="dialogVisible" :style="{ width: '75vw' }" modal>
        <DataTable :value="[selectedItem]" scrollable scrollHeight="flex" tableStyle="min-width: 50rem">
          <Column field="the_main_state_registration_number" header="ОГРН"></Column>
          <Column field="status" header="Статус"></Column>
          <Column field="channel_id" header="ID"></Column>
          <Column field="url" header="URL">
            <template #body="slotProps">
              <a :href="slotProps.data.url" class="text-cyan-400 underline" target="_blank">{{ slotProps.data.url }}</a>
            </template>
          </Column>
          <Column field="name" header="Акк. имя"></Column>
          <Column field="city" header="Город"></Column>
        </DataTable>
        <template #footer>
          <Button label="Ok" severity="info" icon="pi pi-check" @click="dialogVisible = false" />
        </template>
      </Dialog>
  
      <div class="flex items-center flex-col lg:flex-row mb-1 space-y-1 lg:space-y-0">
        <InputGroup class="ml-2">
          <Select v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-56" :class="$style.mydropdown" @change="onLevelChange" />
        </InputGroup>
  
        <InputGroup class="ml-2">
          <Select v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-56" @change="onFounderChange" :disabled="!selectedlevel"/>
        </InputGroup>
  
        <InputGroup class="ml-2">
          <Select v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-56" @change="onSphereChange"/>
        </InputGroup>
        <InputGroup class="ml-2">
          <Select v-model="selectedzone" :options="zones" optionLabel="zone" placeholder="% выполнения" class="w-full md:w-14rem" @change="onZoneChange"/>
        </InputGroup>
        
        <InputGroup class="ml-2">
          <Button icon="pi pi-filter-slash" severity="secondary" class="w-10 h-10" @click="resetFilters()"></Button>
        </InputGroup>
        
        <InputGroup class="flex justify-end mr-4">
          <Button icon="pi pi-sign-out" severity="secondary" class="w-10 h-10" @click="SignOut()"></Button>
        </InputGroup>
      </div>
    </main>
  </template>

<script>
import VueCookies from 'vue-cookies'
import axios from "axios";

export default {
    data() {
        return {
            loading: false,
            dialogVisible: false,
            selectedlevel: null,
            selectedfounder: null,
            selectedsphere: null,
            selectedzone: null,
            founders: [],
            spheres: [],
            zones: [
                { zone: "90-100%" },
                { zone: "70-89%" },
                { zone: "0-69%" }
            ],
            levels: [
                { level: 'Министерство' },
                { level: 'МО' },
                { level: 'Ведомство' },
                { level: 'Законодательный орган' },
                { level: 'Другое' },
                { level: 'ВУЗ' }
            ],
            stats: [],
            statisticColumns: [],
            
        }
    },
    mounted() {
        this.loadAllData();
    },
    methods: {
        openDialog(item){
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
                });
        },
        transformData(items) {
            return items.map(item => {
                const newItem = { ...item };
                if (item.statistic) {
                    item.statistic.forEach((stat, index) => {
                        newItem[`statistic_date_id_${index + 1}`] = stat.date_id;
                        newItem[`statistic_members_count_${index + 1}`] = stat.members_count;
                    });
                    newItem.fulfillment_percentage = this.calculateAverageFulfillment(item.statistic);
                }
                return newItem;
            });
        },
        generateStatisticColumns(items) {
            const statisticColumns = [];
            if (items.length > 0 && items[0].statistic) {
                const statisticCount = items[0].statistic.length;
                for (let i = 1; i <= statisticCount; i++) {
                    statisticColumns.push({ field: `statistic_members_count_${i}`, header: `Участников ${i}` });
                }
            }
            this.statisticColumns = statisticColumns;
        },
        calculateAverageFulfillment(statistics) {
            if (!statistics || statistics.length === 0) return 0;
            const total = statistics.reduce((sum, stat) => sum + stat.fulfillment_percentage, 0);
            return total / statistics.length;
        },
        rowStyle(rowData) {
            const averageFulfillment = rowData.fulfillment_percentage || 0;
            let backgroundColor = '';

            if (averageFulfillment >= 90) {
                backgroundColor = '#E6F4EA';  // Зеленый
            } else if (averageFulfillment >= 70) {
                backgroundColor = '#FDF4E4';  // Желтый
            } else {
                backgroundColor = '#FDEAEA';  // Красный
            }

            return { backgroundColor };
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
            if (this.selectedfounder && this.selectedlevel) {
                axios.get(`/filter/get_sphere_by_founder_and_level?founder=${this.selectedfounder.founder}&level=${this.selectedlevel.level}`)
                    .then(response => {
                        this.spheres = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching spheres:', error);
                    });
            } else if (this.selectedlevel) {
                axios.get(`/filter/get_spheres_by_level?level=${this.selectedlevel.level}`)
                    .then(response => {
                        this.spheres = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching spheres:', error);
                    });
            } else if (this.selectedfounder) {
                axios.get(`/filter/get_spheres_by_founder?founder=${this.selectedfounder.founder}`)
                    .then(response => {
                        this.spheres = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching spheres:', error);
                    });
            } else {
                this.spheres = [];
            }
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
                });
        },
        resetFilters() {
            this.selectedlevel = null;
            this.selectedfounder = null;
            this.selectedsphere = null;
            this.selectedzone = null;
            this.founders = [];
            this.spheres = [];
            this.stats = []
            this.loadAllData();
        },
        SignOut(){
            VueCookies.remove('token')
            this.$router.push('/login')
        }
    }
};
</script>

<style>
html{
  scrollbar-width: thin;
}
</style>

