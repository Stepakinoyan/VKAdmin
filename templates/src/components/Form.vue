
<template>
    <div class="flex items-center justify-center h-screen">
    <form class="space-y-0.5">
      <InputGroup>
          <InputGroupAddon>
              <i class="pi pi-at"></i>
          </InputGroupAddon>
          <InputText v-model="email" placeholder="email@example.com" />
      </InputGroup>
      <InputGroup>
          <InputGroupAddon>
              <i class="pi pi-user"></i>
          </InputGroupAddon>
          <Password v-model="password" :feedback="false" toggleMask placeholder="Введите пароль"/>
      </InputGroup>
      <InputGroup class="mt-1 flex justify-center ">
        <p class="text-red-600">{{ message }}</p>
      </InputGroup>
      <InputGroup class="mt-1 flex justify-center ">
        <Button label="Войти" @click="authorization()"/>
      </InputGroup>
    </form>
    </div>


</template>

<script>
import axios from "axios"
import VueCookies from 'vue-cookies'

export default {
    data() {
        return {
            email: "",
            password: "",
            message: "",
        }
    },
    methods: {
        authorization(){

            axios.post(`/auth/login`, {
                email: this.email,
                password: this.password
            }) 
                  .then((res) => {
                          VueCookies.set('token', res.data.access_token, 3600)
                          this.$router.push('/dashboard')
                  })
                  .catch((error) => {
                          this.message = error.response.data.detail
                  });
        }
    }
};
</script>