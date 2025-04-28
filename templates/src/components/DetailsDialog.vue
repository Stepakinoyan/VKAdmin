<template>
  <Dialog
    :visible="dialogVisible"
    @update:visible="$emit('update:dialogVisible', $event)"
    :style="{ width: '25rem' }"
    :modal="true"
    :closable="true"
  >
    <div class="space-y-2">
      <div class="text-black">
        <h2 class="font-bold">Название</h2>
        <p v-if="!selectedItem['name']" class="text-gray-500">Нет информации</p>
        <p class="text-sm text-gray-500">{{ selectedItem["name"] }}</p>
      </div>
      <div class="text-black">
        <h2 class="font-bold">Ссылка</h2>
        <a
          class="text-blue-600 hover:underline cursor-pointer"
          :href="selectedItem['url']"
          target="_blank"
          >{{ selectedItem["url"] }}</a
        >
      </div>
      <div class="text-black">
        <h2 class="font-bold">ОГРН</h2>
        <p
          v-if="!selectedItem['the_main_state_registration_number']"
          class="text-gray-500"
        >
          Нет информации
        </p>
        <p class="text-gray-500">
          {{ selectedItem["the_main_state_registration_number"] }}
        </p>
      </div>
      <div class="text-black">
        <h2 class="font-bold">Статус</h2>
        <p v-if="!selectedItem['status']" class="text-gray-500">
          Нет информации
        </p>
        <p class="text-gray-500">{{ selectedItem["status"] }}</p>
      </div>
      <div class="text-black">
        <h2 class="font-bold">ID</h2>
        <p class="text-gray-500">{{ selectedItem["channel_id"] }}</p>
      </div>
      <div class="text-black">
        <h2 class="font-bold">Город</h2>
        <p v-if="!selectedItem['city']" class="text-gray-500">Нет информации</p>
        <p class="text-gray-500">{{ selectedItem["city"] }}</p>
      </div>
    </div>
  </Dialog>
</template>

<script>
export default {
  props: {
    dialogVisible: Boolean,
    selectedItem: Object,
  },
  emits: ['update:dialogVisible'],
};
</script>

<style scoped>
.p-dialog-header {
  @apply flex justify-end;
}
</style>  