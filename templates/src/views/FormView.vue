<template>
  <div class="flex items-center justify-center h-screen">
    <form
      action=""
      class="bg-white p-6 rounded-md w-full max-w-sm border border-gosuslugi-border"
    >
      <div class="space-y-3">
        <GosPublicStatLogo class="mx-auto mb-2" />
        <InputGroup>
          <EmailInput v-model="email" />
        </InputGroup>
        <InputGroup>
          <PasswordInput v-model="password" />
        </InputGroup>
        <Button
          label="Войти"
          severity="info"
          class="w-full py-2 bg-blue-600 text-white hover:bg-blue-700"
          @click="AuthUser"
        />
        <p class="text-red-600 pt-3 text-center">{{ message }}</p>
      </div>
    </form>
  </div>
</template>

<script>
import GosPublicStatLogo from "@/assets/GosPublicStatLogo.vue";
import EmailInput from "@/components/EmailInput.vue";
import PasswordInput from "@/components/PasswordInput.vue";
import { authorize_user } from "@/api/PostAuthUserRequest";

export default {
  data() {
    return {
      email: null,
      password: null,
      message: null,
    };
  },
  components: {
    GosPublicStatLogo,
    EmailInput,
    PasswordInput,
  },
  methods: {
    async AuthUser() {
      if (!this.email || !this.password) {
        this.message = "Заполните все поля";
        return;
      }
      try {
        await authorize_user(this.email, this.password);
        this.$router.push("/dashboard");
      } catch (error) {
        this.message = error.response.data.detail;
      }
    },
  },
};
</script>
