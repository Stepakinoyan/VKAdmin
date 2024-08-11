import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './style.css'

import PrimeVue from 'primevue/config';

import Button from 'primevue/button';
import InputGroup from 'primevue/inputgroup';
import DataTable from 'primevue/datatable';
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';

import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Dialog from 'primevue/dialog';
import Tag from 'primevue/tag';
import Column from 'primevue/column';
import Tooltip from 'primevue/tooltip';
import 'primevue/resources/themes/aura-light-blue/theme.css';
import 'primevue/resources/primevue.min.css'; 
import 'primeicons/primeicons.css';
import axios from 'axios';

export const app = createApp(App)
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dropdown', Dropdown)
app.component('InputGroup', InputGroup)
app.component('Button', Button)
app.component("InputText", InputText)
app.component("Password", Password)
app.component("Calendar", Calendar)
app.component("Tag", Tag)
app.component("Dialog", Dialog)



app.directive('tooltip', Tooltip);
app.use(VueCookies)



app.use(PrimeVue, {
    unstyled: false,
    locale: {
        firstDayOfWeek: 1,
        dayNames: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
        dayNamesShort: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        monthNamesShort: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
        today: 'Сегодня'
    } 
});

app.use(router)

app.mount('#app')


    