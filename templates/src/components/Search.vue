<template>
        <main class="flex flex-col-reverse mt-5">
            <div>
                <DataTable :value="stats" tableStyle="min-width: 50rem">   
                        <Column field="organization" header="Организация"></Column> 
                        <Column field="founder" header="Учредитель"></Column>
                        <Column field="sphere" header="Сфера"></Column>
                        <Column field="address" header="Адрес"></Column>
                        <Column field="connected" header="Подключение"></Column>
                        <Column field="state_mark" header="Госметка"></Column>
                        <Column field="decoration" header="Оформление"></Column>
                        <Column field="widgets" header="Виджеты"></Column>
                        <Column field="activity" header="Активность"></Column>
                        <Column field="followers" header="Количество Подписчиков"></Column>
                        <Column field="weekly_audience" header="Охват аудитории за неделю"></Column>
                        <Column field="average_publication_coverage" header="Средний охват публикации "></Column>
                        <Column field="total" header="Итог"></Column>
                        
                </DataTable>
            </div>

        <div class="mb-1">
                <div class="flex flex-row items-center space-x-5">
                        <div>
                            <Dropdown v-model="selectedlevel" :options="levels" optionLabel="level" placeholder="Уровень" class="w-full md:w-14rem" />
                        </div>
                        <div>
                            <Dropdown v-model="selectedfounder" :options="founders" optionLabel="founder" placeholder="Учредитель" class="w-full md:w-14rem" @click="getFoundersByLevel(selectedlevel)"/>
                        </div>
                        <div>
                            <Dropdown v-model="selectedsphere" :options="spheres" optionLabel="sphere" placeholder="Сфера" class="w-full md:w-14rem" @click="getSpheresByFounder(selectedfounder)"/>
                        </div>
                        <div>
                            <Checkbox v-model="checked" :binary="true"/>
                            <label for="ingredient1">Сортировка по возрастанию</label>
                        </div>
                        <div>
                            <Button label="Применить" @click="getStats(selectedlevel, selectedfounder, selectedsphere, checked)"/>
                        </div>
                        <div>
                            <h4 class="text-red-600">{{ error }}</h4>
                        </div>
                </div>
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
            spheres: [
                { sphere: 'Спорт'},
                { sphere: 'Культура'},
                { sphere: 'Образование' },
                { sphere: 'Здравоохранение' },
                { sphere: 'Администрации' },
                { sphere: 'ЖКХ' },
                { sphere: 'Социальная защита' }
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
                })
        },
        getStats(level, founder, sphere, sort){
                axios.get(`/filter/get_stats?level=${level["level"]}&founder=${founder["founder"]}&sphere=${sphere["sphere"]}&sort=${sort}`)
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