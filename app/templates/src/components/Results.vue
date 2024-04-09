<!-- <template>
    <div>
        <DataTable  tableStyle="min-width: 50rem">
            
            <Column field="organization" header="уровень"></Column>
            <Column field="organization" header="Организация"></Column>
            <Column field="founder" header="Учредитель"></Column>
            <Column field="sphere" header="Сфера"></Column>
            <Column field="address" header="Адрес"></Column>
            <Column field="connected" header="Подключение"></Column>
            <Column field="state_mark" header="Наличие госметки"></Column>
            <Column field="decoration" header="Наличие оформления"></Column>
            <Column field="widgets" header="Кол. виджетов"></Column>
            <Column field="activity" header="Кол. постов"></Column>
            <Column field="followers" header="Кол. Подписчиков"></Column>
            <Column field="weekly_audience" header="Охват аудитории за неделю "></Column>
        </DataTable>
    </div>
</template>


<script>
import axios from "axios"
import Filter from '../components/Filter.vue'

export default {
    data(){
        return {
            stats: []
        }

    },
    methods:{
        
        getFStats(level, founder, sphere, sphere){
                axios.get("/filter/get_stats")
                .then((stats) => {
                    this.stats = stats.data
                })
        }
    }
}

</script> -->