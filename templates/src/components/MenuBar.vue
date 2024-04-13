<template>
    <div>
        <Menubar :model="items">
                <template #item="{ item, props}">
                    <a v-ripple class="flex items-center" v-bind="props.action">
                        <span class="ml-2">{{ item.label }}</span>
                    </a>
                </template>
                <template #end>
                    <div class="flex items-center gap-2">
                        <Button label="Выйти" severity="danger" class="w-8rem sm:w-auto mr-3" @click="SignOut()"/>
                    </div>
                </template>
        </Menubar>
    </div>
</template>


<script>
import VueCookies from 'vue-cookies'


export default {
    data() {
        return {
            items: [
                {
                    label: 'Дешборд',
                    command: () => {
                        this.$router.push('/dashboard');
                    }
                },
                {
                    label: 'Добавить Excel',
                    command: () => {
                        this.$router.push('/add');
                    }
                },
            ]
        };
    },
    methods: {
        SignOut(){
            VueCookies.remove('token')
            this.$router.push('/login')
        }
    }
};

</script>