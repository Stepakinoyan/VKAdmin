<template>
        <main class="flex flex-col-reverse mt-5">
                    <DataTable :value="stats" tableStyle="min-width: 50rem">
                            <Column field="level" header="Уровень" ></Column> 
                            <Column field="founder" header="Организация"></Column> 
                            <Column field="name" header="Название"></Column>
                            <Column field="reason" header="Причина"></Column>
                            <Column field="the_main_state_registration_number" header="ОГРН"></Column>
                            <Column field="sphere_1" header="Сфера 1"></Column>
                            <Column field="sphere_2" header="Сфера 2"></Column>
                            <Column field="sphere_3" header="Сфера 3"></Column>
                            <Column field="status" header="Статус"></Column>
                            <Column field="channel_id" header="ID канала"></Column>
                            <Column field="url" header="Ссылка на госпаблик ВК"></Column>
                            <Column field="address" header="Адрес, указанный в настройках страницы"></Column>
                            <Column field="connected" header="Подключение к компоненту «Госпаблики» (да/нет)"></Column>
                            <Column field="state_mark" header="Госметка (да/нет)"></Column>
                            <Column field="decoration" header="Оформление (%)"></Column>
                            <Column field="widgets" header="Виджеты (0/1/2)"></Column>
                            <Column field="activity" header="Активность (%)"></Column>
                            <Column field="followers" header="Количество подписчиков"></Column>
                            <Column field="weekly_audience" header="Общий охват аудитории за неделю"></Column>
                            <Column field="average_publication_coverage" header="Средний охват одной публикации"></Column>

                    </DataTable>

                <div class="flex items-center flex-col lg:flex-row mb-1 w-4/5 space-y-1 lg:space-y-0">
                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-14rem" />
                    </InputGroup>

                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-14rem" @click="getFoundersByLevel(selectedlevel)"/>
                    </InputGroup>

                    <InputGroup class="ml-3">
                        <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-14rem" @click="getSpheresByFounder(selectedfounder)"/>
                    </InputGroup>
                    <InputGroup class="space-x-3 ml-3">
                        <Checkbox v-model="checked" :binary="true"/>
                        <label>Сортировка по возрастанию</label> 
                    </InputGroup>
                    <InputGroup class="ml-3">
                        <Button label="Применить" @click="getStats(selectedlevel, selectedfounder, selectedsphere, checked)"/>
                    </InputGroup>
                    <InputGroup class="ml-3">
                        <p class="text-red-600">{{ error }}</p>
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
            stats: this.getAllStats(),
            error: ""
        }

    },
    methods:{
        getAllStats(){
                axios.get(`/filter/get_all_stats`)
                .then((stats) => {
                    this.stats = stats.data
                })
        },
        getFoundersByLevel(level){
                axios.get(`/filter/get_founders?level=${level["level"]}`)
                .then((founders) => {
                    this.founders = founders.data
                })
        },
        getSpheresByFounder(founder){
                axios.get(`/filter/get_spheres?founder=${founder["founder"]}`)
                .then((spheres) => {
                    this.spheres = spheres.data
                    this.spheres.push("")
                })
        },
        getStats(level, founder, sphere, sort){
                if (sphere === ""){

                    axios.get(`/filter/get_stats?level=${level["level"]}&founder=${founder["founder"]}&sort=${sort}`)
                        .then((stats) => {
                            this.stats = stats.data[0]["items"]
                            this.error = ""
                        })
                        .catch((error) => {
                                this.error = "Все поля не заполнены"
                        });
                }
                else{
                    axios.get(`/filter/get_stats?level=${level["level"]}&founder=${founder["founder"]}&sphere=${sphere['sphere']}&sort=${sort}`)
                    .then((stats) => {
                        this.stats = stats.data[0]["items"]
                        this.error = ""
                    })
                    .catch((error) => {
                            this.error = "Все поля не заполнены"
                    });
                }
                axios.get(`/filter/get_stats?level=${level["level"]}&founder=${founder["founder"]}&sphere=${sphere}&sort=${sort}`)
                .then((stats) => {
                    this.stats = stats.data[0]["items"]
                    this.error = ""
                })
                .catch((error) => {
                          this.error = "Все поля не заполнены"
                  });
        }
    }
}

</script>