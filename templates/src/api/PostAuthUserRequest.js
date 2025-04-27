import axios from "axios";

export let authorize_user = async function (email, password) {
  return await axios
    .post(`/auth/login`, {
      email: email,
      password: password,
    })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      throw error;
    });
};
