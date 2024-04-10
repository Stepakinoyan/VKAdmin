import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './style.css'
import Lara from '@/presets/lara';
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
import 'primeicons/primeicons.css';
import axios from 'axios';

const app = createApp(App)
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://78.24.216.129:7777/';
app.component("InputText", InputText);
app.component("Button", Button);
app.component("InputGroup", InputGroup);
app.component("InputGroupAddon", InputGroupAddon);
app.component("InputMask", InputMask)
app.component("Menubar", Menubar)
app.component("DataTable", DataTable)
app.component("Column", Column)
app.component("Dropdown", Dropdown)
app.component("Password", Password)
app.component("Checkbox", Checkbox)
app.use(VueCookies)

app.use(PrimeVue, {
    unstyled: true,
    pt: Lara
});
app.use(router)

app.mount('#app')
