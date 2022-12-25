import { createSlice, PayloadAction} from "@reduxjs/toolkit";
import { RootState } from './../../app/store';
import { AppointmentStatus, IAppointment, IAppointmentFilter } from "models/appointment";

export interface AppointmentSliceState {
    filter: IAppointmentFilter,
    displayAppointment: Array<IAppointment>
    page: number,
    limit: number,
    viewAppointment: IAppointment|null
}

const initialState: AppointmentSliceState = {
    filter: {
        bookedAt__gte: new Date('2022-01-01').toISOString(),
        bookedAt__lte: new Date().toISOString(),
        status: AppointmentStatus.PENDING,
        patient__pk: null,
        page: 1,
        limit: 10,
    },
    displayAppointment: [],
    page: 1,
    limit: 10,
    viewAppointment: null
}

export interface AppointmentPayload {
    id: number,
    bookedAt: Date | string,
    checkInCode: string | undefined,
}

export const appointmentSlice = createSlice({
    name: 'appointment',
    initialState, 
    reducers:{
        loadAppointment(state, action: PayloadAction<Array<IAppointment>>){
            state.displayAppointment = action.payload
        },
        loadFilter(state, action:PayloadAction<IAppointmentFilter>) {
            console.log('appointment filter change', action.payload)
            state.filter = action.payload
        },
        checkIn(state,action: PayloadAction<number>){
            let target = state.displayAppointment.find((appointment:IAppointment) => {return appointment.id === action.payload});
            target!.status = AppointmentStatus.CHECKIN
        },
        complete(state, action: PayloadAction<number>){
            let target= state.displayAppointment.find((appointment:IAppointment) => {return appointment.id === action.payload});
            target!.status = AppointmentStatus.CHECKIN
        },
        viewAppointment(state,action:PayloadAction<number>){
            let target= state.displayAppointment.find((appointment:IAppointment) => {return appointment.id === action.payload});
            console.log('detail' , target)
            state.viewAppointment = target!; 
        }
    }
})

export const appointmentAction = appointmentSlice.actions;
export const appointmentReducer = appointmentSlice.reducer;
export const appointmentDetailSelector = (state:RootState) => {return state.appointment.viewAppointment!}
export const AppointmentFilterSelector = (state: RootState) => {return state.appointment.filter}
export const AppointmenDisplayListSelector = (state: RootState) => {return state.appointment.displayAppointment};