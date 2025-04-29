import axios from "axios";

export async function getSpheresByRequest(level) {
  try {
    const response = await axios.get("/filter/get_spheres_by", {
      level: level,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching spheres:", error);
    return [];
  }
}
