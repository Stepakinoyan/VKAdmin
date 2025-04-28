import axios from "axios";

export async function exportToExcelRequest(stats) {
    return axios.post("/excel/xlsx/", stats, {
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "blob",
      });
}