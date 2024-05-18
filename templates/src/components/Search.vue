<template>
        <main class="flex flex-col-reverse mt-5">
            <DataTable :value="stats" responsiveLayout="scroll" >
                    <Column field="id" header="ID"></Column>
                    <Column field="level" header="Уровень"></Column>
                    <Column field="founder" header="Учредитель"></Column>
                    <Column field="name" header="Название"></Column>
                    <Column field="the_main_state_registration_number" header="ОГРН"></Column>
                    <Column field="sphere_1" header="Сфера 1"></Column>
                    <Column field="sphere_2" header="Сфера 2"></Column>
                    <Column field="sphere_3" header="Сфера 3"></Column>
                    <Column field="status" header="Статус"></Column>
                    <Column field="channel_id" header="ID канала"></Column>
                    <Column field="url" header="URL"></Column>
                    <Column field="address" header="Адрес"></Column>
                    <Column field="connected" header="Связь"></Column>
                    <Column field="state_mark" header="Гос. отметка"></Column>
                    <Column field="account.screen_name" header="Экранное имя аккаунта"></Column>
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
                </DataTable>
                    <!-- <DataTable :value="stats" tableStyle="min-width: 50rem;">
                            <Column field="name" header="Название" class="text-sm"></Column>
                            <Column field="channel_id" header="ID канала" class="text-sm"></Column>
                            <Column field="url" header="Ссылка на госпаблик ВК" class="text-sm"></Column>
                            <Column field="address" header="Адрес, указанный в настройках страницы" class="text-sm"></Column>
                            <Column field="connected" header="Подключение к компоненту «Госпаблики» (да/нет)" class="text-sm"></Column>
                            <Column field="state_mark" header="Госметка (да/нет)" class="text-sm"></Column>
                            <Column field="decoration" header="Оформление (%)" class="text-sm"></Column>
                            <Column field="widgets" header="Виджеты (0/1/2)" class="text-sm"></Column>
                            <Column field="activity" header="Активность (%)" class="text-sm"></Column>
                            <Column field="followers" header="Количество подписчиков" class="text-sm"></Column>
                            <Column field="weekly_audience" header="Общий охват аудитории за неделю" class="text-sm"></Column>
                            <Column field="average_publication_coverage" header="Средний охват одной публикации" class="text-sm"></Column>
                            <Column header="Account">
                                <template #body="stats">
                                    <div v-if="stats.data.account">
                                        {{ stats.data.account.statistic }}
                                    </div>
                                    <div v-else>
                                        No account data
                                    </div>
                                </template>
                            </Column>
                    </DataTable> -->

                <div class="flex items-center flex-col lg:flex-row mb-1 w-4/5 space-y-1 lg:space-y-0">
                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-14rem" @change="() => {getFounders(); getSpheres()}"/>
                    </InputGroup>

                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-14rem" @change="findSpheresByfounder"/>
                    </InputGroup>

                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-14rem"/>
                    </InputGroup>
                    <InputGroup class="space-x-3 ml-3">
                        <Checkbox v-model="checked" :binary="true"/>
                        <label>Сортировка по возрастанию</label> 
                    </InputGroup>
                    <InputGroup class="ml-3">
                        <Button label="Применить" @click="getStats(selectedlevel, selectedfounder, selectedsphere, checked)"/>
                    </InputGroup>
                </div>
                

        </main>
</template>

<script>
import axios from "axios"


export default {
    data(){
        return {
            selectedlevel: "",
            selectedfounder: "",
            selectedsphere: "",
            founders: [],
            spheres: [],
            levels: [
                { level: 'Министерство'},
                { level: 'МО'},
                { level: 'Ведомство' },
                { level: 'Узкоспециальные' },
                { level: 'Регион' }
            ],
            checked: false,
            stats: null,
        }

    },
    methods:{
        // getAllStats(){
        //         axios.get(`/filter/get_all_stats`)
        //         .then((stats) => {
        //             this.stats = stats.data
        //         })
        // },
        getFoundersByLevel(level){
                axios.get(`/filter/get_founders?level=${level["level"]}`)
                .then((founders) => {
                    this.founders = founders.data
                })
        },
        getSpheresByLevel(level){
                axios.get(`/filter/get_spheres_by_level?level=${level["level"]}`)
                .then((spheres) => {
                    this.spheres = spheres.data
                })
        },
        getSpheresByFounder(founder){
                axios.get(`/filter/get_spheres_by_founder?founder=${founder["founder"]}`)
                .then((spheres) => {
                    this.spheres = spheres.data
                })
        },
        getFounders() {
            this.getFoundersByLevel(this.selectedlevel)
        },
        getSpheres() {
            this.getSpheresByLevel(this.selectedlevel)
        },
        findSpheresByfounder() {
            this.getSpheresByFounder(this.selectedfounder)
        },

        getStats(level, founder, sphere, sort){
            const levelParam = level ? `level=${level.level}` : '';
            const founderParam = founder ? `founder=${founder.founder}` : '';
            const sphereParam = sphere ? `sphere=${sphere.sphere}` : '';
            const sortParam = typeof sort === 'boolean' ? `sort=${sort}` : '';

            const queryParams = [levelParam, founderParam, sphereParam, sortParam].filter(param => param !== '').join('&');

            axios.get(`/filter/get_stats?${queryParams}`)
                .then((stats) => {
                    this.stats = stats.data[0].items;
                })
                .catch(error => {
                    console.error('Error fetching stats:', error);
                });
        }
    }
}

</script>