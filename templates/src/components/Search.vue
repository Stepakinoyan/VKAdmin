<template>
    <main class="flex flex-col-reverse mt-2">
        <DataTable
        :value="stats"
        :loading="loading"
        size="small"
        paginator
        :rowsPerPageOptions="[20, 50]"
        :rows="20"
        removableSort
        resizableColumns
        columnResizeMode="fit"
        scrollHeight="calc(100vh - 164px)"
        :scrollable="isScrollable"
        :sortField="'fulfillment_percentage'"
        :sortOrder="-1"
        class="mt-2 text-sm"
        :rowStyle="rowStyle"
        tableStyle="min-width: 50rem"   
    >
        <Column field="name" sortable header="Название" frozen class="px-4 text-xs" style="min-width: 170px;"></Column>
        <Column field="fulfillment_percentage" sortable header="Процент выполнения" class="text-black text-xs"></Column>
        <Column v-for="(col, index) in statisticColumns" :key="index" :field="col.field" sortable :header="col.header" class="text-black"></Column>
        <Column field="members_count" sortable header="Всего участников" class="text-black text-xs"></Column>
        <Column field="verified" sortable header="Проверен" class="text-black text-xs">
            <template #body="slotProps">
                <i v-if="slotProps.data.verified" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="has_avatar" sortable header="Аватар" class="text-black">
            <template #body="slotProps">
                <i v-if="slotProps.data.has_avatar" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="has_cover" sortable header="Обложка" class="text-black">
            <template #body="slotProps">
                <i v-if="slotProps.data.has_cover" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="has_description" sortable header="Описание" class="text-black">
            <template #body="slotProps">
                <i v-if="slotProps.data.has_description" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="has_gos_badge" sortable header="Гос. метка" class="text-black">
            <template #body="slotProps">
                <i v-if="slotProps.data.has_gos_badge" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="has_widget" sortable header="Виджет" class="text-black">
            <template #body="slotProps">
                <i v-if="slotProps.data.has_widget" class="pi pi-check-circle" style="color: green; font-size: 1.25rem"></i>
                <i v-else class="pi pi-times-circle" style="color: red; font-size: 1.25rem"></i>
            </template>
        </Column>
        <Column field="widget_count" sortable header="Кол-во виджетов" class="text-black text-xs"></Column>
        <Column field="posts" sortable header="Посты" class="text-black text-xs"></Column>
        <Column field="posts_1d" sortable header="Посты за 1 день" class="text-black text-xs"></Column>
        <Column field="posts_7d" sortable header="Посты за 7 дней" class="text-black"></Column>
        <Column field="posts_30d" sortable header="Посты за 30 дней" class="text-black text-xs"></Column>
        <Column field="post_date" sortable header="Дата последнего сбора" class="text-black text-xs"></Column>
        <Column field="level" sortable header="Уровень" class="text-black text-xs"></Column>
        <Column field="founder" sortable header="Учредитель" class="text-black text-xs"></Column>
        <Column field="the_main_state_registration_number" sortable header="ОГРН" class="text-black text-xs"></Column>
        <Column field="status" sortable header="Статус" class="text-black" style="min-width: 300px"></Column>
        <Column field="channel_id" sortable header="ID канала" class="text-black"></Column>
        <Column field="url" sortable header="URL" class="text-black text-xs"></Column>
        <Column field="screen_name" sortable header="Имя в VK" class="text-black text-xs"></Column>
        <Column field="name" sortable header="Имя аккаунта" class="text-xs text-black"></Column>
        <Column field="city" sortable header="Город" class="text-black text-xs"></Column>
        <Column field="activity" sortable header="Тип" class="text-black text-xs"></Column>

        <template #empty>
            <tr>
                <td colspan="30" class="text-center p-4">
                    Ничего не найдено
                </td>
            </tr>
        </template>
        

        <template #paginator="{ state, firstPage, lastPage, totalPages, previousPage, nextPage }">
                <div class="flex justify-center items-center mt-2 fixed-paginator">
                    <button @click="firstPage" :disabled="state.firstPage">««</button>
                    <button @click="previousPage" :disabled="state.firstPage">«</button>
                    <span v-for="page in totalPages" :key="page" class="px-1">
                        <button
                            :class="{'bg-green-500 text-white': state.currentPage === page, 'bg-white': state.currentPage !== page}"
                            @click="state.changePage(page)"
                        >
                            {{ page }}
                        </button>
                    </span>
                    <button @click="nextPage" :disabled="state.lastPage">»</button>
                    <button @click="lastPage" :disabled="state.lastPage">»»</button>
                </div>
            </template>
    </DataTable>

    <div class="flex items-center flex-col lg:flex-row mb-1 space-y-1 lg:space-y-0">
            <InputGroup class="ml-2">
                <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-14rem" @change="onLevelChange"/>
            </InputGroup>

            <InputGroup class="ml-2">
                <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-14rem" @change="onFounderChange"/>
            </InputGroup>

            <InputGroup class="ml-2">
                <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-14rem" @change="onSphereChange"/>
            </InputGroup>

            <InputGroup class="ml-2">
                <Dropdown
                    v-model="selectedzone"
                    :options="zones"
                    optionLabel="zone"
                    placeholder="Зона"
                    class="w-full md:w-14rem"
                    @change="onZoneChange"
                />
            </InputGroup>
            
            <InputGroup class="ml-2" @click="resetFilters()">
                <i class="pi pi-filter-slash cursor-pointer" style="font-size: 1.25rem"></i>   
            </InputGroup>
            <InputGroup class="flex justify-end mr-4">
                <i class="pi pi-sign-out cursor-pointer" style="font-size: 1.25rem" @click="SignOut()"></i>
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
                    statisticColumns.push({ field: `statistic_members_count_${i}`, header: `Кол-во участников (статистика) ${i}` });
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
                backgroundColor = '#f0fdf4';  // Зеленый
            } else if (averageFulfillment >= 70) {
                backgroundColor = '#fefce8';  // Желтый
            } else {
                backgroundColor = '#fef2f2';  // Красный
            }

            return { backgroundColor };
        },
        onLevelChange() {
            this.selectedfounder = null;  // Сбросить учредителя
            this.selectedsphere = null;   // Сбросить сферу
            this.getFounders();           // Обновить список учредителей
            this.getSpheres();            // Обновить список сфер
            this.loadFilteredData();      // Загрузить отфильтрованные данные
        },
        onFounderChange() {
            this.selectedsphere = null;   // Сбросить сферу
            this.getSpheres();            // Обновить список сфер
            this.loadFilteredData();      // Загрузить отфильтрованные данные
        },
        onSphereChange() {
            this.loadFilteredData();      // Загрузить отфильтрованные данные
        },
        onZoneChange() {
            this.loadFilteredData();      // Загрузить отфильтрованные данные
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
            if (this.selectedlevel) {
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


.main {
    margin-top: 2px;
}

.DataTable {
    margin-top: 2px;
    font-size: 0.875rem;
    min-height: calc(100vh - 164px); /* Обеспечивает минимальную высоту */
    display: flex;
    flex-direction: column;
}



.p-datatable-tbody tr {
    height: 100%; /* Заполнить высоту пустыми строками */
}

.InputGroup {
    margin-left: 2px;
}

.space-x-2 {
    margin-left: 2px;
}

.mb-1 {
    margin-bottom: 0.25rem;
}

.yellow-zone {
    color: black;
}

.yellow-zone-name {
    color: inherit;
}

.p-datatable-empty-message {
    text-align: center;
    padding: 1rem;
}

.p-paginator-page.p-highlight {
    background-color: #4caf50;
    color: white;
    border: none;
}
</style>