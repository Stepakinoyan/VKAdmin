import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './style.css'

import Lara from '@primevue/themes/lara';
import PrimeVue from 'primevue/config';

import Button from 'primevue/button';
import InputGroup from 'primevue/inputgroup';
import DataTable from 'primevue/datatable';
import Select from 'primevue/select';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import ColumnGroup from 'primevue/columngroup';
import Dialog from 'primevue/dialog';
import Tag from 'primevue/tag';
import Column from 'primevue/column';
import 'primeicons/primeicons.css'
import { definePreset } from '@primevue/themes';

import axios from 'axios';

export const app = createApp(App)
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Select', Select);
app.component('InputGroup', InputGroup);
app.component('Button', Button);
app.component("InputText", InputText);
app.component("Password", Password)
app.component("ColumnGroup", ColumnGroup)
app.component("Tag", Tag)
app.component("Dialog", Dialog)

app.use(VueCookies)



app.use(PrimeVue, {
    theme: {
        preset: Lara,
        options: {
            prefix: 'p',
            darkModeSelector: 'null'
        }
    }
});
app.use(router)

app.mount('#app')


    