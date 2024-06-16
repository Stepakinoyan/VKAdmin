import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './style.css'
import 'primevue/resources/themes/lara-light-green/theme.css'; // Импорт светлой темы Lara
import 'primevue/resources/primevue.min.css'; 
import 'primeicons/primeicons.css';


import PrimeVue from 'primevue/config';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputMask from 'primevue/inputmask';
import Menubar from 'primevue/menubar';
import DataTable from 'primevue/datatable';
import Dropdown from 'primevue/dropdown';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup'; 
import InputIcon from 'primevue/inputicon';
import IconField from 'primevue/iconfield';
import Paginator from 'primevue/paginator';

import axios from 'axios';

export const app = createApp(App)
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:7777/';
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Dropdown', Dropdown);
app.component('InputGroup', InputGroup);
app.component('Checkbox', Checkbox);
app.component('Button', Button);
app.component("InputText", InputText);
app.component("InputGroupAddon", InputGroupAddon);
app.component("InputMask", InputMask)
app.component("Menubar", Menubar)
app.component("Password", Password)
app.component("ColumnGroup", ColumnGroup)
app.component("IconField", IconField)
app.component("InputIcon", InputIcon)
app.component("Paginator", Paginator)

app.use(VueCookies)

app.use(PrimeVue);
app.use(router)

app.mount('#app')


    