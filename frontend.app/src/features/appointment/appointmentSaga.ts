import { PayloadAction } from "@reduxjs/toolkit";
import { checkInAppointment, completeAppointment, loadAppointment } from "api/appointmentApi";
import { store } from "app/store";
import { AxiosResponse } from "axios";
import { IAppointment, IAppointmentFilter } from "models/appointment";
import { take, fork, call, put } from "redux-saga/effects";
import { AppointmentPayload, appointmentAction } from "./appointmentSlice";


function* handleFilterChange(payload: IAppointmentFilter) {
    let resData: AxiosResponse = yield call (loadAppointment,payload);
    yield put (appointmentAction.loadAppointment(resData.data.data));
}

function* handleLoadAppointment(payload: IAppointment[]) {
    console.warn('appointments', payload)
}

function* hanldeCheckInAppoitment(payload: AppointmentPayload) {
    yield checkInAppointment(payload.id, payload.checkInCode!);
}

function* handleCompleteAppointment(payload: AppointmentPayload) {
    yield completeAppointment(payload.id);
}

function* watchCheckInAppointment() {
    const action: PayloadAction<AppointmentPayload> = yield take(appointmentAction.checkIn.type);
    yield fork(hanldeCheckInAppoitment, action.payload);
}

function* watchCompleteAppointment() {
    const action: PayloadAction<AppointmentPayload> = yield take(appointmentAction.complete.type);
    yield fork(handleCompleteAppointment, action.payload);
}

function* watchFilterChange() {
    while(true){
        console.log('saga filter change');
        const action: PayloadAction<IAppointmentFilter> = yield take(appointmentAction.loadFilter.type);
        yield fork(handleFilterChange, action.payload);
    }
}

// function* watchAppointmentChange() {
//     while(true){
//         const action: PayloadAction<Array<IAppointment>> = yield take(appointmentAction.loadAppointment.type);
//         yield fork(handleLoadAppointment, action.payload);
//     }
// }

export function* appointmentSaga() {
    yield fork(watchFilterChange);
    yield fork(watchCompleteAppointment);
    yield fork(watchCheckInAppointment);
    // yield fork(watchAppointmentChange);
}

