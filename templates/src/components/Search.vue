<template>
        <main class="flex flex-col-reverse mt-5">
                    <DataTable :value="stats" tableStyle="min-width: 50rem;">
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

                    </DataTable>

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