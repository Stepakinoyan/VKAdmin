<template>
    <div class="flex items-center justify-center h-screen bg-gosuslugi rounded-lg">
        <form class="bg-white p-6 rounded-md w-full max-w-sm py-20">
            <div class="space-y-3">
                <InputGroup>
                    <InputText v-model="email" placeholder="Почта" class="bg-slate-100 py-3 px-3 rounded"/>
                </InputGroup>
                <InputGroup>
                    <InputText v-model="password" placeholder="Пароль" class="bg-slate-100 py-3 px-3 rounded" />
                </InputGroup>
                <div class="flex justify-center pt-3">
                    <Button label="Войти" class="w-full py-2 bg-blue-600 text-white hover:bg-blue-700" @click="authorization" />
                </div>
            </div>
            <div class="mt-4 flex justify-center">
                <p class="text-red-600">{{ message }}</p>
            </div>
        </form>
    </div>
</template>

<script>
import axios from "axios";
import VueCookies from 'vue-cookies';

export default {
    data() {
        return {
            email: "",
            password: "",
            message: "",
        };
    },
    methods: {
        authorization() {
            axios.post(`/auth/login`, {
                email: this.email,
                password: this.password
            })
            .then((res) => {
                VueCookies.set('token', res.data.access_token, 3600);
                this.$router.push('/dashboard');
            })
            .catch((error) => {
                this.message = error.response.data.detail;
            });
        }
    }
};
</script>

<!-- <style scoped>
.bg-blue-100 {
    background-color: #f0f4f8;
}
</style> -->