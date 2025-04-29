import axios from "axios";

export let LogOutRequest = async function () {
  return await axios.post("/auth/logout").catch((error) => {
    throw error;
  });
};
