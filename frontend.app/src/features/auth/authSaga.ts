import { PayloadAction } from '@reduxjs/toolkit';
import { loginApi } from 'api/userApi';
import { AxiosResponse } from 'axios';
import { replace } from 'connected-react-router';
import { call, fork, put, take } from 'redux-saga/effects';
import { LoginPayload, authActions } from './authSlice';

function* handleLogin(payload: LoginPayload) {
  try {
    const response: AxiosResponse = yield call(loginApi, payload);
    if (response.status === 201) {
      localStorage.setItem('access_token', response.data.data.accessToken);
      localStorage.setItem('id_data', response.data.data.doctorId);
      localStorage.setItem('firstName_data', response.data.data.firstName);
      localStorage.setItem('lastName_data', response.data.data.lastName);
      localStorage.setItem('avatar_data', response.data.data.avatar);
      localStorage.setItem('type', response.data.data.type);
      localStorage.setItem('id_user', response.data.data.id);
      yield put(
        authActions.loginSuccess({
          id: response.data.data.id,
          firstName: response.data.data.firstName,
          lastName: response.data.data.lastName,
          avatar: response.data.data.avatar,
        })
      );
      if (response.data.data.type === 'DOCTOR') {
        //redirect to doctor home page
        yield put(replace('/doctor/home'));
      } else {
        //redirect to manager home page
        yield put(replace('/manager/home'));
      }
      return response.data.data.accessToken;
    } else {
      yield put(authActions.loginFailed('Nhập sai email hoặc mật khẩu!'));
    }
  } catch (error) {
    alert('Nhập sai email hoặc mật khẩu!');
    yield put(authActions.loginFailed('Nhập sai email hoặc mật khẩu!'));
  }
}

function* watchLoginFlow() {
  while (true) {
    const action: PayloadAction<LoginPayload> = yield take(authActions.login.type);
    yield fork(handleLogin, action.payload);
  }
}

export function* authSaga() {
  yield fork(watchLoginFlow);
}
