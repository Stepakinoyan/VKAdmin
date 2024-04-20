<template>
    <div>
        <Menubar>
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
    methods: {
        SignOut(){
            VueCookies.remove('token')
            this.$router.push('/login')
        }
    }
};

</script>