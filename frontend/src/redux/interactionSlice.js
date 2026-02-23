import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    loading: false,
    response: null,
  },
  reducers: {
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setResponse: (state, action) => {
      state.response = action.payload;
    },
  },
});

export const { setLoading, setResponse } = interactionSlice.actions;
export default interactionSlice.reducer;