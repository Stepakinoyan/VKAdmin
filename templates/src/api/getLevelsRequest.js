import axios from "axios";


export async function getLevelsRequest() {
  try {
      const response = await axios.get(`/filter/get_levels`);
      return response.data;
  } catch (error) {
      console.error("Error fetching Levels:", error);
      return [];
  }
}