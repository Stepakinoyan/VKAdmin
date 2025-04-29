<template>
  <InputGroup class="w-full lg:w-1/4 flex justify-end space-x-8 pr-2.5">
    <Button
      icon="pi pi-filter-slash"
      class="w-10 h-10 bg-slate-100 border border-gosuslugi-border"
      @click="$emit('reset-filters')"
      :disabled="fieldDisabled"
    />
    <Button
      icon="pi pi-file-excel"
      class="w-10 h-10 bg-slate-100 border border-gosuslugi-border"
      v-tooltip.bottom="'Экспорт в Excel'"
      @click="
        () => {
          $emit('export-excel');
        }
      "
    />
  </InputGroup>
</template>

<script>
export default {
  props: {
    fieldDisabled: Boolean,
  },
  emits: ["reset-filters", "export-excel"],
};
</script>
