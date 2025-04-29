<template>
  <div>
    <header>
      <Menu />
    </header>
    <main class="container mx-auto mt-5">
      <Instruction class="" />
    </main>
  </div>
</template>

<script>
import Menu from "../components/Menu.vue";
import Instruction from "../components/Instruction.vue";

export default {
  components: {
    Menu,
    Instruction,
  },
};
</script>
