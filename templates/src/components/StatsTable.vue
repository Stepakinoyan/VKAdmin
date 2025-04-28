<!-- StatsTable.vue -->
<template>
    <DataTable
      :value="stats"
      :loading="loading"
      paginator
      :rows="20"
      :rowsPerPageOptions="[20, 50]"
      removableSort
      scrollable
      scrollHeight="calc(100vh - 182px)"
      :sortField="'average_fulfillment_percentage'"
      :sortOrder="-1"
      class="mx-0 md:mx-2 mt-3 border"
      tableStyle="min-width: 50rem"
      :pt="DataTableStyle"
    >
      <Column
        field="name"
        header="Название"
        class="text-xs cursor-pointer text-left"
        style="min-width: 240px; max-width: 240px"
        frozen
      >
        <template #body="slotProps">
          <span @click="$emit('open-dialog', slotProps.data)" class="hover:underline">{{
            slotProps.data.name
          }}</span>
        </template>
      </Column>
  
      <Column
        v-for="(col, colIndex) in columns"
        :key="colIndex"
        :field="col.field"
        sortable
        :header="col.header"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <div class="flex justify-center items-center">
            <i
              v-if="
                colIndex === 0 ||
                getFulfillmentPercentage(slotProps.data.name, colIndex) ===
                  getFulfillmentPercentage(slotProps.data.name, colIndex - 1)
              "
            ></i>
            <i
              class="pi pi-arrow-up text-green-400 pb-1.4"
              v-else-if="
                getFulfillmentPercentage(slotProps.data.name, colIndex) >
                getFulfillmentPercentage(slotProps.data.name, colIndex - 1)
              "
            ></i>
            <i class="pi pi-arrow-down text-red-600 pb-1.4" v-else></i>
            {{ getFulfillmentPercentage(slotProps.data.name, colIndex) }}%
          </div>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="average_week_fulfillment_percentage"
        sortable
        header="% за неделю"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <Tag
            v-if="slotProps.data.average_week_fulfillment_percentage >= 90"
            severity="success"
          >
            {{ slotProps.data.average_fulfillment_percentage }}%
          </Tag>
          <Tag
            v-else-if="slotProps.data.average_week_fulfillment_percentage >= 70"
            severity="warning"
          >
            {{ slotProps.data.average_week_fulfillment_percentage }}%
          </Tag>
          <Tag v-else severity="danger">
            {{ slotProps.data.average_week_fulfillment_percentage }}%
          </Tag>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="average_fulfillment_percentage"
        sortable
        header="% за месяц"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <Tag
            v-if="slotProps.data.average_fulfillment_percentage >= 90"
            severity="success"
          >
            {{ slotProps.data.average_fulfillment_percentage }}%
          </Tag>
          <Tag
            v-else-if="slotProps.data.average_fulfillment_percentage >= 70"
            severity="warning"
          >
            {{ slotProps.data.average_fulfillment_percentage }}%
          </Tag>
          <Tag v-else severity="danger">
            {{ slotProps.data.average_fulfillment_percentage }}%
          </Tag>
        </template>
      </Column>
  
      <Column
        field="members_count"
        sortable
        header="Участники"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <div class="flex justify-center items-center">
            <i
              v-if="
                slotProps.data.statistic.length <= 1 ||
                slotProps.data.members_count ===
                  slotProps.data.statistic[slotProps.data.statistic.length - 2]?.members_count
              "
            ></i>
            <i
              class="pi pi-arrow-up text-green-400 pb-1.4"
              v-else-if="
                slotProps.data.members_count >
                slotProps.data.statistic[slotProps.data.statistic.length - 2]?.members_count
              "
            ></i>
            <i class="pi pi-arrow-down text-red-600 pb-1.4" v-else></i>
            {{ slotProps.data.members_count || 0 }}
          </div>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="statistic.activity.subscribed"
        header="подписок за день"
        sortable
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <span
            v-if="
              slotProps.data.statistic &&
              slotProps.data.statistic.length > 0 &&
              slotProps.data.statistic[slotProps.data.statistic.length - 1].activity
            "
          >
            {{ slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.subscribed }}
          </span>
          <span v-else>0</span>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="statistic.activity.likes"
        header="лайков за день"
        sortable
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <span
            v-if="
              slotProps.data.statistic &&
              slotProps.data.statistic.length > 0 &&
              slotProps.data.statistic[slotProps.data.statistic.length - 1].activity
            "
          >
            {{ slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.likes }}
          </span>
          <span v-else>0</span>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="statistic.activity.comments"
        header="ком. за день"
        sortable
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <span
            v-if="
              slotProps.data.statistic &&
              slotProps.data.statistic.length > 0 &&
              slotProps.data.statistic[slotProps.data.statistic.length - 1].activity
            "
          >
            {{ slotProps.data.statistic[slotProps.data.statistic.length - 1].activity.comments }}
          </span>
          <span v-else>0</span>
        </template>
      </Column>
  
      <Column
        field="has_gos_badge"
        header="Гос. метка"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.has_gos_badge"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+10%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="has_avatar"
        header="Аватар"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.has_avatar"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+5%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="has_cover"
        header="Обложка"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.has_cover"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+10%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="has_description"
        header="Описание"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.has_description"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+5%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="has_widget"
        header="Виджет"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.has_widget"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+10%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="connected"
        header="Подключение"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <i
            v-if="slotProps.data.connected"
            class="pi pi-check-circle"
            style="color: green"
            v-tooltip="'+10%'"
          ></i>
          <i
            v-else
            class="pi pi-times-circle"
            style="color: red"
            v-tooltip="'0%'"
          ></i>
        </template>
      </Column>
  
      <Column
        field="widget_count"
        sortable
        header="Виджеты"
        class="text-black text-xs text-center cursor-pointer"
      >
        <template #body="slotProps">
          <div class="flex justify-center items-center">
            <i
              v-if="
                slotProps.data.statistic.length <= 1 ||
                slotProps.data.widget_count ===
                  slotProps.data.statistic[slotProps.data.statistic.length - 2]?.activity.widget_count
              "
            ></i>
            <i
              class="pi pi-arrow-up text-green-400 pb-1.4"
              v-else-if="
                slotProps.data.widget_count >
                slotProps.data.statistic[slotProps.data.statistic.length - 2]?.activity.widget_count
              "
            ></i>
            <i class="pi pi-arrow-down text-red-600 pb-1.4" v-else></i>
            <span v-if="slotProps.data.widget_count >= 2" v-tooltip="'+10%'">
              {{ slotProps.data.widget_count }}
            </span>
            <span v-else-if="slotProps.data.widget_count == 1" v-tooltip="'+5%'">
              {{ slotProps.data.widget_count }}
            </span>
            <span v-else v-tooltip="'0%'">
              {{ slotProps.data.widget_count || "0" }}
            </span>
          </div>
        </template>
      </Column>
  
      <Column
        v-if="showColumns"
        field="posts"
        sortable
        header="Посты"
        class="text-black text-xs text-center"
      />
      <Column
        v-if="showColumns"
        field="posts_1d"
        sortable
        header="1 день"
        class="text-black text-xs text-center"
      />
      <Column
        v-if="showColumns"
        field="posts_7d"
        sortable
        header="7 дней"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <div>
            <span v-if="slotProps.data.posts_7d >= 3" class="cursor-pointer" v-tooltip="'+40%'">
              {{ slotProps.data.posts_7d }}
            </span>
            <span v-else class="cursor-pointer" v-tooltip="'0%'">
              {{ slotProps.data.posts_7d }}
            </span>
          </div>
        </template>
      </Column>
      <Column
        v-if="showColumns"
        field="posts_30d"
        sortable
        header="30 дней"
        class="text-black text-xs text-center"
      />
      <Column
        v-if="showColumns"
        field="weekly_audience_reach"
        sortable
        header="Охват за неделю"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          <div>
            <span
              v-if="(slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 >= 70"
              class="cursor-pointer"
              v-tooltip="'+40%'"
            >
              {{ slotProps.data.weekly_audience_reach }}
            </span>
            <span
              v-else-if="
                (slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 >= 50 &&
                (slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 < 70
              "
              class="cursor-pointer"
              v-tooltip="'+7%'"
            >
              {{ slotProps.data.weekly_audience_reach }}
            </span>
            <span
              v-else-if="
                (slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 >= 30 &&
                (slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 < 50
              "
              class="cursor-pointer"
              v-tooltip="'+5%'"
            >
              {{ slotProps.data.weekly_audience_reach }}
            </span>
            <span
              v-else-if="
                (slotProps.data.weekly_audience_reach / slotProps.data.members_count) * 100 == 0
              "
              class="cursor-pointer"
              v-tooltip="'0%'"
            >
              {{ slotProps.data.weekly_audience_reach }}
            </span>
          </div>
        </template>
      </Column>
      <Column
        v-if="showColumns"
        field="date_added"
        header="Дата сбора"
        class="text-black text-xs text-center"
      >
        <template #body="slotProps">
          {{ formatDate(slotProps.data.date_added) }}
        </template>
      </Column>
    </DataTable>
  </template>
  
  <script>
  export default {
    props: {
      stats: Array,
      loading: Boolean,
      columns: Array,
      statisticsMap: Object,
      showColumns: Boolean,
      DataTableStyle: Object,
    },
    emits: ['open-dialog'],
    methods: {
      getFulfillmentPercentage(name, index) {
        return this.statisticsMap[name] ? this.statisticsMap[name][index] : 0;
      },
      formatDate(date) {
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, "0");
        const month = String(d.getMonth() + 1).padStart(2, "0");
        const year = d.getFullYear();
        return `${day}.${month}.${year}`;
      },
    },
  };
  </script>