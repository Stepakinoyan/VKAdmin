<template>
    <main class="flex flex-col-reverse mt-2">
        <!-- scrollHeight="746px" -->
        <DataTable :value="stats" paginator :rowsPerPageOptions="[10, 20, 50]" :rows="10" scrollHeight="calc(100vh - 164px)" removableSort  :scrollable="isScrollable" :sortField="'fulfillment_percentage'" :sortOrder="-1" class="mt-2 text-sm blue-table h-max-[839px]" :rowStyle="rowStyle">
            <Column field="name" sortable header="Название" frozen class="px-7 text-xs py-7"></Column>
            <Column field="fulfillment_percentage" sortable header="Процент выполнения" class="text-black"></Column>
            <Column v-for="(col, index) in statisticColumns" :key="index" :field="col.field" sortable :header="col.header" class="text-black"></Column>
            <Column field="level" sortable header="Уровень" class="text-black"></Column>
            <Column field="founder" sortable header="Учредитель" class="text-black"></Column>
            <Column field="the_main_state_registration_number" sortable header="ОГРН" class="text-black"></Column>
            <Column field="status" sortable header="Статус" class="text-black" style="min-width: 300px"></Column>
            <Column field="channel_id" sortable header="ID канала" class="text-black"></Column>
            <Column field="url" sortable header="URL" class="text-black"></Column>
            <Column field="address" sortable header="Адрес" class="text-black"></Column>
            <Column field="connected" sortable header="Связь" class="text-black"></Column>
            <Column field="state_mark" sortable header="Гос. отметка" class="text-black"></Column>
            <Column field="screen_name" sortable header="Имя в VK" class="text-black"></Column>
            <Column field="name" sortable header="Имя аккаунта" class="text-xs text-black"></Column>
            <Column field="city" sortable header="Город" class="text-black"></Column>
            <Column field="activity" sortable header="Активность" class="text-black"></Column>
            <Column field="verified" sortable header="Проверен" class="text-black"></Column>
            <Column field="has_avatar" sortable header="Аватар" class="text-black"></Column>
            <Column field="has_cover" sortable header="Обложка" class="text-black"></Column>
            <Column field="has_description" sortable header="Описание" class="text-black"></Column>
            <Column field="has_gos_badge" sortable header="Гос. значок" class="text-black"></Column>
            <Column field="has_widget" sortable header="Виджет" class="text-black"></Column>
            <Column field="widget_count" sortable header="Кол-во виджетов" class="text-black"></Column>
            <Column field="members_count" sortable header="Кол-во участников" class="text-black"></Column>
            <Column field="site" sortable header="Сайт" class="text-black"></Column>
            <Column field="posts" sortable header="Посты" class="text-black"></Column>
            <Column field="posts_1d" sortable header="Посты за 1 день" class="text-black"></Column>
            <Column field="posts_7d" sortable header="Посты за 7 дней" class="text-black"></Column>
            <Column field="posts_30d" sortable header="Посты за 30 дней" class="text-black"></Column>
            <Column field="post_date" sortable header="Дата поста" class="text-black"></Column>
        </DataTable>

        <div class="flex items-center flex-col lg:flex-row mb-1 w-4/5 space-y-1 lg:space-y-0">
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

            <InputGroup class="ml-2 space-x-4">
                <Button label="Сбросить" @click="resetFilters" />
                <i class="pi pi-sign-out cursor-pointer" style="font-size: 2rem" @click="SignOut()"></i>
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
            statisticColumns: []
        }
    },
    mounted() {
        this.loadAllData();
    },
    methods: {
        loadAllData() {
            axios.get('/filter/get_stats')
                .then(response => {
                    const items = response.data[0].items;
                    this.stats = this.transformData(items);
                    this.generateStatisticColumns(items);
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
</style>