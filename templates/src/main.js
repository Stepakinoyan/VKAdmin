import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './style.css'

import PrimeVue from 'primevue/config';

import Button from 'primevue/button';
import InputGroup from 'primevue/inputgroup';
import DataTable from 'primevue/datatable';

import Dropdown from 'primevue/dropdown';

import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Dialog from 'primevue/dialog';
import Tag from 'primevue/tag';
import Column from 'primevue/column';
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
app.component("Tag", Tag)
app.component("Dialog", Dialog)

app.use(VueCookies)



app.use(PrimeVue, {
    unstyled: false,
});

app.use(router)

app.mount('#app')


    