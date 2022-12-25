import { RootState } from './../../app/store';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { UserStorage } from 'models/userStorage';

export interface LoginPayload {
  email: string | undefined;
  password: string | undefined;
  type: string;
}

export interface AuthState {
  isLoggedIn: boolean;
  logging?: boolean;
  currentUser?: UserStorage;
}

const initialState: AuthState = {
  isLoggedIn: Boolean(localStorage.getItem('access_token')),
  logging: false,
  currentUser: {
    id: Number(localStorage.getItem('id_data')),
    firstName: String(localStorage.getItem('firstName_data')),
    lastName: String(localStorage.getItem('lastName_data')),
    avatar: String(localStorage.getItem('avatar_data')),
  },
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login(state, action: PayloadAction<LoginPayload>) {
      state.logging = true;
    },
    loginSuccess(state, action: PayloadAction<UserStorage>) {
      state.isLoggedIn = true;
      state.logging = false;
      state.currentUser = action.payload;
    },
    loginFailed(state, action: PayloadAction<string>) {
      state.logging = false;
    },

    logout(state) {
      state.isLoggedIn = false;
      state.currentUser = undefined;
    },
  },
});

//Actions
export const authActions = authSlice.actions;

//Selectors
export const selectIsLoggedIn = (state: RootState) => state.auth.isLoggedIn;
export const selectIsLogging = (state: RootState) => state.auth.logging;
export const selectCurrentUser = (state: RootState) => state.auth.currentUser;

//Reducer
const authReducer = authSlice.reducer;
export default authReducer;
