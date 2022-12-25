import { configureStore, ThunkAction, Action, combineReducers } from '@reduxjs/toolkit';
import createSagaMiddleware from '@redux-saga/core';
import rootSaga from './rootSaga';
import authReducer from 'features/auth/authSlice';
import { appointmentReducer } from 'features/appointment/appointmentSlice';
// import { HealthRecordReducer } from 'features/health_record/health_recordSlice';
import { connectRouter, routerMiddleware } from 'connected-react-router';
import { history } from 'utils';
import { contractFilterReducer } from 'features/contract/contractSlice';

const rootReducer = combineReducers({
  router: connectRouter(history),
  auth: authReducer,
  appointment: appointmentReducer,
  contract: contractFilterReducer
});

const sagaMiddleware = createSagaMiddleware();
export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(sagaMiddleware, routerMiddleware(history)),
});

sagaMiddleware.run(rootSaga);

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
