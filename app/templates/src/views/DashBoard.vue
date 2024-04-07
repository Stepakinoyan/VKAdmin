<script setup>
import MenuBar from "../components/MenuBar.vue"
import Results from "../components/Results.vue"
import Filter from "../components/Filter.vue"
</script>

<template>
  <header>
    <MenuBar/>
  </header >
  <main class="mt-5 flex">
      <div class="w-4/5">
        <Results/>
      </div>
      <div class="flex justify-center w-1/5">
          <Filter/>
      </div>
  </main>
</template>