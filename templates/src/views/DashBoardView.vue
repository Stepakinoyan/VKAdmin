<template style="font-size: 14px">
  <header>
    <Menu />
  </header>
  <main class="flex flex-col">
    <div class="w-full flex items-center flex-col lg:flex-row pt-3">
      <div
        class="flex flex-col lg:flex-row w-full lg:w-3/4 space-x-0 lg:space-x-1 ml-0 lg:ml-2"
      >
        <Dropdown
          v-model="selectedLevel"
          :options="levels"
          optionLabel="level"
          placeholder="Уровень"
          class="w-full lg:w-1/3 mt-2 lg:mt-0"
          @change="onLevelChange"
          :disabled="fieldDisabled"
          panelClass="min-w-min w-10rem"
          emptyMessage="Нет доступных опций"
          :pt="{
            root: ['border', 'border-gosuslugi-border'],
          }"
        />
        <Dropdown
          v-model="selectedFounder"
          :options="founders"
          optionLabel="founder"
          placeholder="Учредитель"
          class="w-full lg:w-1/3 mt-2 lg:mt-0"
          @change="onFounderChange"
          :disabled="!selectedLevel || fieldDisabled"
          emptyMessage="Нет доступных опций"
          v-if="isAdmin"
          :pt="{
            root: ['border', 'border-gosuslugi-border'],
          }"
        />
        <Dropdown
          v-if="spheres.length !== 1"
          v-model="selectedSphere"
          :options="spheres"
          optionLabel="sphere"
          placeholder="Сфера"
          class="w-full lg:w-1/3 mt-2 lg:mt-0"
          @change="loadFilteredData"
          :disabled="fieldDisabled"
          emptyMessage="Нет доступных опций"
          :pt="{
            root: ['border', 'border-gosuslugi-border'],
          }"
        />
        <Dropdown
          v-model="selectedZone"
          :options="zones"
          optionLabel="zone"
          placeholder="% выполнения"
          class="w-full lg:w-1/3 mt-2 lg:mt-0"
          @change="loadFilteredData"
          :disabled="fieldDisabled"
          emptyMessage="Нет доступных опций"
          :pt="{
            root: ['border', 'border-gosuslugi-border'],
          }"
        />
        <Calendar
          v-model="dates"
          :hide-on-range-selection="true"
          @update:model-value="handleDateSelection"
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
          v-model="searchName"
          placeholder="Организация"
          class="w-full lg:w-2/3 placeholder:text-gray-500 pl-[12px] py-2 lg:py-0 mt-2 lg:mt-0"
          @input="debouncedLoadFilteredData"
          :disabled="fieldDisabled"
          :pt="{
            root: ['border', 'border-gosuslugi-border'],
          }"
        />
      </div>
      <ActionButtons
        :fieldDisabled="fieldDisabled"
        @reset-filters="resetFilters"
        @export-excel="exportToExcel"
      />
    </div>
    <StatsTable
      :stats="stats"
      :loading="loading"
      :columns="columns"
      :statisticsMap="statisticsMap"
      :showColumns="showColumns"
      :DataTableStyle="DataTableStyle"
      @open-dialog="openDialog"
    />
    <DetailsDialog
      v-model:dialogVisible="dialogVisible"
      :selectedItem="selectedItem"
    />
  </main>
</template>

<script>
import axios from "axios";
import { getFounders } from "@/api/GetFoundersRequest";
import { getLevelsRequest } from "@/api/getLevelsRequest";
import { getSpheresByRequest } from "@/api/GetSpheresRequest";
import { exportToExcelRequest } from "@/api/exportToExcelRequest";
import Menu from "@/components/Menu.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import StatsTable from "@/components/StatsTable.vue";
import DetailsDialog from "@/components/DetailsDialog.vue";
import { GosPublicStatDataTableStyle } from "@/assets/GosPublicStatDataTableStyle";
import debounce from "lodash/debounce";

export default {
  components: {
    Menu,
    ActionButtons,
    StatsTable,
    DetailsDialog,
  },
  data() {
    return {
      loading: false,
      dialogVisible: false,
      fieldDisabled: false,
      minDateDisabled: null,
      maxDateDisabled: null,
      selectedLevel: null,
      selectedFounder: null,
      selectedSphere: null,
      selectedZone: null,
      dates: [],
      searchName: "",
      founders: [],
      spheres: [],
      zones: [{ zone: "90-100%" }, { zone: "70-89%" }, { zone: "0-69%" }],
      levels: [],
      stats: [],
      columns: [],
      statisticsMap: {},
      selectedItem: {},
      isAdmin: false,
      DataTableStyle: GosPublicStatDataTableStyle,
      debouncedLoadFilteredData: null
    };
  },
  mounted() {
    this.loadAllData();
    this.getLevels();
    this.getSpheres();
    this.checkAdmin();
  },
  computed: {
    showColumns() {
      if (Array.isArray(this.dates) && this.dates.length > 0) {
        const [start, end] = this.dates;
        return !(start && end);
      }
      return true;
    },
  },
  created() {
    this.debouncedLoadFilteredData = debounce(this.loadFilteredData, 1000);
  },
  methods: {
    debounce,
    async checkAdmin() {
      try {
        const response = await axios.get("/auth/me");
        this.isAdmin = response.data.role === "admin";
      } catch (error) {
        console.error("Error checking admin status:", error);
        this.isAdmin = false;
      }
    },
    async exportToExcel() {
      try {
        this.loading = true;
        this.fieldDisabled = true;
        const response = await exportToExcelRequest(this.stats);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "organizations.xlsx");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error("Error exporting to Excel:", error);
      } finally {
        this.loading = false;
        this.fieldDisabled = false;
      }
    },
    openDialog(item) {
      this.selectedItem = item;
      this.dialogVisible = true;
    },
    async loadAllData() {
      try {
        this.loading = true;
        const response = await axios.get("/filter/get_stats");
        const items = response.data;
        this.stats = this.transformData(items);
        this.generateStatisticColumns(items);
      } catch (error) {
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
        console.error("Error fetching stats:", error);
      } finally {
        this.loading = false;
      }
    },
    transformData(items) {
      return items.map((item) => {
        const newItem = { ...item };
        if (item.statistic) {
          item.statistic.forEach((stat, index) => {
            newItem[`statistic_percentage_${index + 1}`] =
              stat.fulfillment_percentage;
            newItem[`statistic_members_count_${index + 1}`] =
              stat.members_count;
          });
        }
        return newItem;
      });
    },
    generateStatisticColumns(items) {
      const columns = [];
      const statisticsMap = {};

      if (items.length > 0 && items[0].statistic) {
        items.forEach((item) => {
          const sortedStatistics = item.statistic
            .sort((a, b) => new Date(b.date_added) - new Date(a.date_added))
            .reverse();

          sortedStatistics.forEach((stat, statIndex) => {
            const date = new Date(stat.date_added);
            const formattedDate = date.toLocaleDateString("ru-RU", {
              year: "numeric",
              month: "2-digit",
              day: "2-digit",
            });

            if (!columns[statIndex]) {
              columns[statIndex] = {
                field: `statistic_percentage_${statIndex + 1}`,
                header: formattedDate,
              };
            }

            if (!statisticsMap[item.name]) {
              statisticsMap[item.name] = [];
            }

            statisticsMap[item.name][statIndex] = stat.fulfillment_percentage;
          });
        });
      }

      this.columns = columns;
      this.statisticsMap = statisticsMap;
    },
    async onLevelChange() {
      this.selectedFounder = null;
      this.selectedSphere = null;
      await Promise.all([this.getFounders(), this.getSpheres()]);
      this.loadFilteredData();
    },
    async onFounderChange() {
      this.selectedSphere = null;
      await this.getSpheres();
      this.loadFilteredData();
    },
    async getFounders() {
      try {
        this.founders = await getFounders(this.selectedLevel);
      } catch (error) {
        console.error("Error fetching founders:", error);
        this.founders = [];
      }
    },
    async getLevels() {
      try {
        this.levels = await getLevelsRequest();
      } catch (error) {
        console.error("Error fetching levels:", error);
        this.levels = [];
      }
    },
    async getSpheres() {
      try {
        this.spheres = await getSpheresByRequest(this.selectedLevel);
      } catch (error) {
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
        console.error("Error fetching spheres:", error);
        this.spheres = [];
      }
      console.log(this.spheres);
    },
    async loadFilteredData() {
      try {
        this.loading = true;
        this.minDateDisabled = new Date(9999, 12, 31);
        this.maxDateDisabled = new Date(1, 1, 1);

        const params = {
          level: this.selectedLevel?.level,
          founder: this.selectedFounder?.founder,
          sphere: this.selectedSphere?.sphere,
          zone: this.selectedZone?.zone,
          name: this.searchName,
          date_from: this.dates?.[0]
            ? this.formatDate(this.dates[0])
            : undefined,
          date_to: this.dates?.[1] ? this.formatDate(this.dates[1]) : undefined,
        };

        const queryString = Object.entries(params)
          .filter(([_, value]) => value !== undefined)
          .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
          .join("&");

        const response = await axios.get(`/filter/get_stats?${queryString}`);
        const items = response.data;
        this.stats = this.transformData(items);
        this.generateStatisticColumns(items);
      } catch (error) {
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
        console.error("Error fetching filtered stats:", error);
      } finally {
        this.loading = false;
        this.minDateDisabled = null;
        this.maxDateDisabled = null;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const dateObj = new Date(dateStr);
      const day = String(dateObj.getDate()).padStart(2, "0");
      const month = String(dateObj.getMonth() + 1).padStart(2, "0");
      const year = dateObj.getFullYear();
      return `${year}-${month}-${day}`;
    },
    resetFilters() {
      this.selectedLevel = null;
      this.selectedFounder = null;
      this.selectedSphere = null;
      this.selectedZone = null;
      this.dates = [];
      this.searchName = "";
      this.founders = [];
      this.spheres = [];
      this.stats = [];
      this.loadAllData();
      this.getSpheres();
    },
    handleDateSelection(dates) {
      this.dates = dates;
      this.loadFilteredData();
    },
  },
};
</script>

<style>
html {
  scrollbar-width: thin;
}

.p-paginator-page.p-highlight {
  background-color: #3b82f6;
  color: white;
  border: none;
}

.p-datatable-wrapper {
  scrollbar-width: thin;
}

.p-datatable .p-datatable-tbody > tr:hover {
  background-color: #f4f4f4;
}

.p-tooltip-text {
  background-color: #fff;
  color: black;
  border: #9ca3af 1px solid;
  border-radius: 4px;
  padding: 8px;
}

.p-sortable-column:not(.p-highlight) .p-sortable-column-icon {
  display: none;
}

.p-sortable-column.p-highlight .p-sortable-column-icon {
  display: inline-block;
}
</style>
