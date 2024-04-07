import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
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
import Column from 'primevue/column';
import 'primeicons/primeicons.css';

const app = createApp(App)
app.component("InputText", InputText);
app.component("Button", Button);
app.component("InputGroup", InputGroup);
app.component("InputGroupAddon", InputGroupAddon);
app.component("InputMask", InputMask)
app.component("Menubar", Menubar)
app.component("DataTable", DataTable)
app.component("Column", Column)
app.component("Dropdown", Dropdown)

app.use(PrimeVue, {
    unstyled: true,
    pt: Lara
});
app.use(router)

app.mount('#app')
