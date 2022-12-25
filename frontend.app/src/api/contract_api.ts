import axios, { AxiosRequestConfig } from "axios";
import { urlApi, localUrl } from "constants/UrlApi";
import { ContractFilterState } from "features/contract/reducer";
import { ITreamtentContract } from "models/contract";

const config: AxiosRequestConfig = {
    baseURL: urlApi,
    headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')!}`,
        'Content-Type': 'application/json',
    },
};

const generateParams = (map: object) => {
    let param = '';
    for (const [key, value] of Object.entries(map)) {
        console.log(key, value);
        if (value !== undefined && value !== null) {
            param = param.concat(key, '=', value, '&');
        }
    }
    return param.slice(0, param.length - 1);
};

export const listContract = async (filter: ContractFilterState) => {
    return await axios.get(`${urlApi}contract/doctor/list/?${generateParams(filter)}`, config)
}


export const approveRequestBody = (sessions: any[], endedAt: string) => {
return {
        "endedAt": endedAt,
        "numberOfDays": sessions.length,
        "sessions": sessions,
    }
}

export const approveContract = async (contract:number, body: any) => {
    return await axios.put(`${urlApi}contract/doctor/${contract}/approve/`,body,config)
}

export const getContractPatient = async (contract: ITreamtentContract) => {
    return await axios.put(`${urlApi}${contract.id}}/approve/`, config)
}

export const listContractSession = async (contractId: number) => {
    return await axios.get(`${urlApi}contract/doctor/session/readonly/?contract=${contractId}`, config)
}


export const getInstructionCategories = async () => {
    return await axios.get(`${urlApi}instructions-categories/?page=1&limit=10`, config);
}
export const cancelInstruction = async (id: number) => {
    let body = {
        'id': id,
        'action': 'cancel'
    }
    return await axios.put(`${urlApi}doctor/action/instruction/`, body , config)
}

export const reloadContract = (id: number) => {
    return axios.get(`${urlApi}contract/doctor/${id}/`,config);
}

export const cancelContract = async (contract:number, body: string) => {
    return await axios.put(`${urlApi}contract/doctor/${contract}/cancel/`,{'cancelReason': body},config)
}