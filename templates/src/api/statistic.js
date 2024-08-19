import axios from 'axios';
import VueCookies from 'vue-cookies';

export const exportToExcel = (stats) => {
    return axios.post("/excel/xlsx/", stats, {
      headers: {
        'Content-Type': 'application/json',
         headers: { authorization: VueCookies.get('token') }
      },
      responseType: 'blob'
    });
  };

export const getFounders = (level) => {
        return axios.get(`/filter/get_founders?level=${level}`);
};
// headers: { authorization: VueCookies.get('token') }
export const getSpheresBy = (params) => {
        return axios.get('/filter/get_spheres_by');
};
