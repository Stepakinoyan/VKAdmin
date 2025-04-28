<template>
  <div class="w-full h-full flex items-center flex-col lg:flex-row pt-3">
    <div
      class="flex flex-col lg:flex-row w-full lg:w-3/4 space-x-0 lg:space-x-1 ml-0 lg:ml-2"
    >
      <Dropdown
        v-if="levels.length != 1"
        :value="selectedLevel"
        @update:model-value="$emit('update:selectedLevel', $event)"
        :options="levels"
        optionLabel="level"
        placeholder="Уровень"
        class="w-full lg:w-1/3 mt-2 lg:mt-0"
        @change="$emit('level-change')"
        :disabled="fieldDisabled"
        panelClass="min-w-min w-10rem"
        emptyMessage="Нет доступных опций"
        :pt="{ root: ['border', 'border-gosuslugi-border'] }"
      />
      <Dropdown
        v-if="AdminVerify"
        :value="selectedFounder"
        @update:model-value="$emit('update:selectedFounder', $event)"
        :options="founders"
        optionLabel="founder"
        placeholder="Учредитель"
        class="w-full lg:w-1/3 mt-2 lg:mt-0"
        @change="$emit('founder-change')"
        :disabled="!selectedLevel || fieldDisabled"
        emptyMessage="Нет доступных опций"
        :pt="{ root: ['border', 'border-gosuslugi-border'] }"
      />
      <Dropdown
        v-if="spheres.length != 1"
        :value="selectedSphere"
        @update:model-value="$emit('update:selectedSphere', $event)"
        :options="spheres"
        optionLabel="sphere"
        placeholder="Сфера"
        class="w-full lg:w-1/3 mt-2 lg:mt-0"
        @change="$emit('filter-change')"
        :disabled="fieldDisabled"
        emptyMessage="Нет доступных опций"
        :pt="{ root: ['border', 'border-gosuslugi-border'] }"
      />
      <Dropdown
        :value="selectedZone"
        @update:model-value="$emit('update:selectedZone', $event)"
        :options="zones"
        optionLabel="zone"
        placeholder="% выполнения"
        class="w-full lg:w-1/3 mt-2 lg:mt-0"
        @change="$emit('filter-change')"
        :disabled="fieldDisabled"
        emptyMessage="Нет доступных опций"
        :pt="{ root: ['border', 'border-gosuslugi-border'] }"
      />
      <Calendar
        :value="dates"
        @update:model-value="$emit('update:dates', $event); $emit('filter-change')"
        @click="$emit('update:dates', [])"
        @touchstart="$emit('update:dates', [])"
        :hide-on-range-selection="true"
        dateFormat="dd-mm-yy"
        selectionMode="range"
        :manualInput="false"
        placeholder="Диапазон"
        :showOtherMonths="true"
        :selectOtherMonths="true"
        showIcon
        iconDisplay="input"
        class="w-full lg:w-2/3 mt-2 lg:mt-0 py-2 lg:py-0 rounded-lg"
        :pt="{
          root: ['border', 'border-gosuslugi-border'],
          input: { class: ['pl-[12px]', 'placeholder:text-gray-500'] },
        }"
        :disabled="fieldDisabled"
        :minDate="minDateDisabled"
        :maxDate="maxDateDisabled"
      />
      <InputText
        type="text"
        :value="searchingName"
        @update:model-value="$emit('update:searchingName', $event)"
        @input="$emit('filter-change')"
        placeholder="Организация"
        class="w-full lg:w-2/3 placeholder:text-gray-500 pl-[12px] py-2 lg:py-0 mt-2 lg:mt-0"
        :disabled="fieldDisabled"
        :pt="{ root: ['border', 'border-gosuslugi-border'] }"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    levels: Array,
    founders: Array,
    spheres: Array,
    zones: Array,
    selectedLevel: Object,
    selectedFounder: Object,
    selectedSphere: Object,
    selectedZone: Object,
    dates: Array,
    searchingName: String,
    fieldDisabled: Boolean,
    minDateDisabled: Date,
    maxDateDisabled: Date,
    AdminVerify: Boolean,
  },
  emits: [
    'update:selectedLevel',
    'update:selectedFounder',
    'update:selectedSphere',
    'update:selectedZone',
    'update:dates',
    'update:searchingName',
    'level-change',
    'founder-change',
    'filter-change',
  ],
};
</script>