<template>
    <div>
        <div>
            <Dropdown v-model="selectedCity" :options="levels" optionLabel="name" placeholder="Уровень" class="w-full md:w-14rem" />
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";

const selectedCity = ref();
const levels = ref([
    { name: 'уровень 1', code: 1},
    { name: 'уровень 2', code: 2},
    { name: 'уровень 3', code: 3 },
]);
</script>