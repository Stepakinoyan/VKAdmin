import axios from "axios";

export async function getFounders(selectedLevel) {
  try {
    if (!selectedLevel) {
      return [];
    }
    const response = await axios.get(
      `/filter/get_founders?level=${selectedLevel.level}`,
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching founders:", error);
    return [];
  }
}
