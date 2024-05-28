<template>
    <main class="flex flex-col-reverse mt-2">
        <DataTable :value="stats" :scrollable="isScrollable" :scrollHeight="isScrollable ? '779px' : 'auto'" class="mt-2 text-sm blue-table">
            <Column field="name" header="Название" frozen></Column>
            <Column field="level" header="Уровень"></Column>
            <Column field="founder" header="Учредитель"></Column>
            <Column field="the_main_state_registration_number" header="ОГРН"></Column>
            <Column field="status" header="Статус"></Column>
            <Column field="channel_id" header="ID канала"></Column>
            <Column field="url" header="URL"></Column>
            <Column field="address" header="Адрес"></Column>
            <Column field="connected" header="Связь"></Column>
            <Column field="state_mark" header="Гос. отметка"></Column>
            <Column field="account.screen_name" header="Имя в VK"></Column>
            <Column field="account.name" header="Имя аккаунта"></Column>
            <Column field="account.city" header="Город"></Column>
            <Column field="account.activity" header="Активность"></Column>
            <Column field="account.verified" header="Проверен"></Column>
            <Column field="account.has_avatar" header="Аватар"></Column>
            <Column field="account.has_cover" header="Обложка"></Column>
            <Column field="account.has_description" header="Описание"></Column>
            <Column field="account.has_gos_badge" header="Гос. значок"></Column>
            <Column field="account.has_widget" header="Виджет"></Column>
            <Column field="account.widget_count" header="Кол-во виджетов"></Column>
            <Column field="account.members_count" header="Кол-во участников"></Column>
            <Column field="account.site" header="Сайт"></Column>
            <Column field="account.date_added" header="Дата добавления"></Column>
            <Column field="account.posts" header="Посты"></Column>
            <Column field="account.posts_1d" header="Посты за 1 день"></Column>
            <Column field="account.posts_7d" header="Посты за 7 дней"></Column>
            <Column field="account.posts_30d" header="Посты за 30 дней"></Column>
            <Column field="account.post_date" header="Дата поста"></Column>

            
            <Column v-for="(col, index) in statisticColumns" :key="index" :field="col.field" :header="col.header"></Column>
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
            <InputGroup class="space-x-2 ml-2">
                <Checkbox v-model="checked" :binary="true"/>
                <label>Сортировка по возрастанию</label> 
            </InputGroup>
            <InputGroup class="ml-2">
                <Button label="Применить" @click="getStats(selectedlevel, selectedfounder, selectedsphere, checked)"/>
            </InputGroup>
        </div>
    </main>
</template>

<style>
.main {
    margin-top: 2px;
}

.DataTable {
    margin-top: 2px;
    font-size: 0.875rem; /* Уменьшение размера шрифта */
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
</style>


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
                { level: 'Узкоспециальные' },
                { level: 'Регион' }
            ],
            checked: false,
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
                if (item.account) {
                    Object.assign(newItem, item.account);

                    // Calculate change in members count
                    let previousMembersCount = null;
                    item.account.statistic.forEach((stat, index) => {
                        newItem[`statistic_date_id_${index + 1}`] = stat.date_id;

                        if (previousMembersCount !== null) {
                            const change = stat.members_count - previousMembersCount;
                            newItem[`statistic_members_count_${index + 1}`] = this.formatChange(change, false);
                        } else {
                            newItem[`statistic_members_count_${index + 1}`] = this.formatChange(stat.members_count, true);
                        }
                        previousMembersCount = stat.members_count;
                    });
                } else {
                    const emptyFields = [
                        'screen_name', 'name', 'city', 'activity', 'verified', 'has_avatar', 'has_cover',
                        'has_description', 'has_gos_badge', 'has_widget', 'widget_count', 'members_count',
                        'site', 'date_added', 'posts', 'posts_1d', 'posts_7d', 'posts_30d', 'post_date'
                    ];
                    emptyFields.forEach(field => {
                        newItem[`account.${field}`] = null;
                    });
                }
                return newItem;
            });
        },
        generateStatisticColumns(items) {
            const statisticColumns = [];
            if (items.length > 0 && items[0].account && items[0].account.statistic) {
                const statisticCount = items[0].account.statistic.length;
                for (let i = 1; i <= statisticCount; i++) {
                    statisticColumns.push({ field: `statistic_date_id_${i}`, header: `Дата статистики ${i}` });
                    statisticColumns.push({ field: `statistic_members_count_${i}`, header: `Кол-во участников (статистика) ${i}` });
                }
            }
            this.statisticColumns = statisticColumns;
        }
    }
}
</script>
