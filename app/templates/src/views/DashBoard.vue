<script setup>
import MenuBar from "../components/MenuBar.vue"
// import Results from "../components/Results.vue"
// import Filter from "../components/Filter.vue"
import Search from "../components/Search.vue"
</script>

<template >
  <div class="bg-slate-300" style="height: 100vh;">
    <header>
      <MenuBar/>
    </header>
    <main class="mt-5 flex">
      <Search/>
    </main>
  </div>

</template> 

<!-- <div class="w-4/5">
        <Results/>
      </div>
      <div class="flex justify-center w-1/5 ml-1">
          <Filter/>
      </div> -->