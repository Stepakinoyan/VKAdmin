<template>
    <main class="flex flex-col-reverse mt-2">
        <DataTable :value="stats" removableSort :scrollable="isScrollable" scrollHeight="779px" class="mt-2 text-sm blue-table" :rowStyle="rowStyle">
            <Column field="name" sortable header="Название"frozen></Column>
            <Column field="level" sortable header="Уровень"></Column>
            <Column field="founder" sortable header="Учредитель"></Column>
            <Column field="the_main_state_registration_number" sortable header="ОГРН"></Column>
            <Column field="status" sortable header="Статус"></Column>
            <Column field="channel_id" sortable header="ID канала"></Column>
            <Column field="url" sortable header="URL"></Column>
            <Column field="address" sortable header="Адрес"></Column>
            <Column field="connected" sortable header="Связь"></Column>
            <Column field="state_mark" sortable header="Гос. отметка"></Column>
            <Column field="screen_name" sortable header="Имя в VK"></Column>
            <Column field="name" sortable header="Имя аккаунта"></Column>
            <Column field="city" sortable header="Город"></Column>
            <Column field="activity" sortable header="Активность"></Column>
            <Column field="verified" sortable header="Проверен"></Column>
            <Column field="has_avatar" sortable header="Аватар"></Column>
            <Column field="has_cover" sortable header="Обложка"></Column>
            <Column field="has_description" sortable header="Описание"></Column>
            <Column field="has_gos_badge" sortable header="Гос. значок"></Column>
            <Column field="has_widget" sortable header="Виджет"></Column>
            <Column field="widget_count" sortable header="Кол-во виджетов"></Column>
            <Column field="members_count" sortable header="Кол-во участников"></Column>
            <Column field="site" sortable header="Сайт"></Column>
            <Column field="posts" sortable header="Посты"></Column>
            <Column field="posts_1d" sortable header="Посты за 1 день"></Column>
            <Column field="posts_7d" sortable header="Посты за 7 дней"></Column>
            <Column field="posts_30d" sortable header="Посты за 30 дней"></Column>
            <Column field="post_date" sortable header="Дата поста"></Column>
            <Column v-for="(col, index) in statisticColumns" :key="index" :field="col.field" sortable :header="col.header"></Column>
        </DataTable>

        <div class="flex items-center flex-col lg:flex-row mb-1 w-4/5 space-y-1 lg:space-y-0">
            <InputGroup class="ml-2">
                <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-14rem" @change="() => {getFounders(); getSpheres()}"/>
            </InputGroup>

            <InputGroup class="ml-2">
                <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-14rem" @change="findSpheresByfounder"/>
            </InputGroup>

            <InputGroup class="ml-2">
                <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-14rem"/>
            </InputGroup>
            <InputGroup class="ml-2">
                <Button label="Применить" @click="getStats(selectedlevel, selectedfounder, selectedsphere, checked)"/>
            </InputGroup>
        </div>
    </main>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            selectedlevel: "",
            selectedfounder: "",
            selectedsphere: "",
            founders: [],
            spheres: [],
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
    methods: {
        formatChange(value, isFirst) {
            if (isFirst) return value;
            return value > 0 ? `+${value}` : value;
        },
        getFoundersByLevel(level) {
            axios.get(`/filter/get_founders?level=${level["level"]}`)
                .then((founders) => {
                    this.founders = founders.data;
                });
        },
        getSpheresByLevel(level) {
            axios.get(`/filter/get_spheres_by_level?level=${level["level"]}`)
                .then((spheres) => {
                    this.spheres = spheres.data;
                });
        },
        getSpheresByFounder(founder) {
            axios.get(`/filter/get_spheres_by_founder?founder=${founder["founder"]}`)
                .then((spheres) => {
                    this.spheres = spheres.data;
                });
        },
        getFounders() {
            this.getFoundersByLevel(this.selectedlevel);
        },
        getSpheres() {
            this.getSpheresByLevel(this.selectedlevel);
        },
        findSpheresByfounder() {
            this.getSpheresByFounder(this.selectedfounder);
        },
        getStats(level, founder, sphere, sort) {
            const levelParam = level ? `level=${level.level}` : '';
            const founderParam = founder ? `founder=${founder.founder}` : '';
            const sphereParam = sphere ? `sphere=${sphere.sphere}` : '';
            const sortParam = typeof sort === 'boolean' ? `sort=${sort}` : '';

            const queryParams = [levelParam, founderParam, sphereParam, sortParam].filter(param => param !== '').join('&');

            axios.get(`/filter/get_stats?${queryParams}`)
                .then((response) => {
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
            const averageFulfillment = rowData.statistic ? this.calculateAverageFulfillment(rowData.statistic) : 0;
            let backgroundColor = '';
            let color = '';

            if (!rowData.statistic || (rowData.statistic && rowData.statistic.length === 0)) {
                backgroundColor = '#fca5a5';
            } else if (averageFulfillment >= 90) {
                backgroundColor = '#d9f99d';
            } else if (averageFulfillment >= 70) {
                backgroundColor = '#fef08a';
            } else {
                backgroundColor = '#fca5a5';
            }

            return { backgroundColor, color };
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
