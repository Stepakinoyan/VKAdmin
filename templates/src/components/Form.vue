<template>
    <div class="flex items-center justify-center h-screen bg-gosuslugi rounded-lg">
        <form class="bg-white p-6 rounded-md w-full max-w-sm py-20">
            <div class="space-y-3">
                <InputGroup>
                    <InputText v-model="email" placeholder="Почта" class="border border-black placeholder:text-surface-400 p-2.5 rounded-md"/>
                </InputGroup>
                <InputGroup>
                    <Password v-model="password" placeholder="Пароль" :feedback="false" :pt="{
                            input: {
                                    root: ({ props, context, parent }) => {
                                        var _a, _b, _c;
                                        return {
                                            class: [
                                            // Font
                                            'leading-[normal]',
                                            // Flex
                                            { 'flex-1 w-[1%]': parent.instance.$name == 'InputGroup' },
                                            // Spacing
                                            'm-0',
                                            {
                                                'px-4 py-4': props.size == 'large',
                                                'px-2 py-2': props.size == 'small',
                                                'p-3': props.size == null
                                            },
                                            'w-full',
                                            // Shape
                                            { 'rounded-md': parent.instance.$name !== 'InputGroup' },
                                            { 'first:rounded-l-md rounded-none last:rounded-r-md': parent.instance.$name == 'InputGroup' },
                                            { 'border-0 border-y border-l last:border-r': parent.instance.$name == 'InputGroup' },
                                            { 'first:ml-0 -ml-px': parent.instance.$name == 'InputGroup' && !props.showButtons },
                                            // Colors
                                            'text-surface-600 dark:text-surface-200',
                                            'placeholder:text-surface-400 dark:placeholder:text-surface-500',
                                            'bg-surface-0 dark:bg-surface-900',
                                            'border',
                                            { 'border-surface-300 dark:border-surface-600': !parent.props.invalid },
                                            // Invalid State
                                            { 'border-red-500 dark:border-red-400': parent.props.invalid },
                                            // States
                                            // Filled State *for FloatLabel
        
                                            ]
                                        };
                                }
                        }
                    }"/>
                
                </InputGroup>
                <div class="flex justify-center pt-3">
                    <Button label="Войти" severity="info" class="w-full py-2 bg-blue-600 text-white hover:bg-blue-700"  @click="authorization"/>
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
