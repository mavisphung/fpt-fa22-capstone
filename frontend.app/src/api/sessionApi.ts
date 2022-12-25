import axios, { AxiosRequestConfig } from 'axios'
import { urlApi, localUrl } from "constants/UrlApi";
import { ContractFilterState } from "features/contract/reducer";
import { ITreatmentSession } from "models/contract";

const config: AxiosRequestConfig = {
    baseURL: urlApi,
    headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')!}`,
        'Content-Type': 'application/json',
    },
};

export const listContractSession = async (id: number) => {
    return await axios.get(`${urlApi}contract/doctor/session/readonly/?contract=${id}`, config)
}


export interface ITreatmentSessionRequest {
    contract: number,
    patient: number,
    slot?: any,
    startTime: string|Date,
    endTime: string|Date,
    note: string[],
    assessment: string[],
}


export const createContractSession = async (session: ITreatmentSessionRequest) => {
    return await axios.post(`${urlApi}contract/doctor/session/`, session, config)
}


export const cancelContractSession = async (session: any) => {
    return await axios.put(`${urlApi}contract/doctor/cancel/session/`, {
        'session': session.id,
        'cancelReason': session.cancelReason
    }, config)
}

export const suggestDoctorHour = async (date: string) => {
    return await axios.get(`${urlApi}api/suggest/doctor/${localStorage.getItem('id_data')}/?date=${date}`, config);
}

export const getWorkingShift = async () => {
    return await axios.get(`${urlApi}/doctor/shifts`, config);
}