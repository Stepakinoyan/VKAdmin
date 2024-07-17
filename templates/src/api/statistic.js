import axios from 'axios';


export const exportToExcel = (stats) => {
    return axios.post("/excel/xlsx/", stats, {
      headers: {
        'Content-Type': 'application/json'
      },
      responseType: 'blob'
    });
  };

export const getFounders = (level) => {
        return axios.get(`/filter/get_founders?level=${level}`);
};

export const getSpheresBy = (params) => {
        return axios.get('/filter/get_spheres_by', { params });
};
