import axios, { AxiosRequestConfig } from "axios";
import { urlApi, localUrl } from "constants/UrlApi";
import { ContractFilterState } from "features/contract/reducer";
import { ITreamtentContract } from "models/contract";
import { Diseases } from "models/diseases";
import { IPrescription, IPrescription2, IPrescriptionDetails2 } from "models/health_record";
import moment from "moment";

const config: AxiosRequestConfig = {
    baseURL: urlApi,
    headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')!}`,
        'Content-Type': 'application/json',
    },
};

export const getMedicine = async (keyword: string) => {
    return await axios.get(`${urlApi}medicines/?keyword=${keyword}`, config)
}


export const getDisease = async (keyword: string) => {
    return await axios.get(`${urlApi}diseases/?keyword=${keyword}`, config)
}


const formatCreatePrescription = (prescription: IPrescription,
    record: number,
    patient: number) => {
    let detail = prescription.details.map((d) => { return {
        medicine: d.medicine.id,
        guide: d.guide,
        quantity: d.quantity,
        unit: d.unit,
    }})
    let fromDate = moment(prescription.fromDate).format('YYYY-MM-DD')
    let toDate = moment(prescription.toDate).format('YYYY-MM-DD')

    return {
        "healthRecord": record,
        "patient": patient,
        "fromDate":fromDate,
        "toDate": toDate,
        "diagnose": prescription.diagnose,
        "detail": detail,
        "note": prescription.note,
    }
}

export const makePrescription = async (prescprion: IPrescription, record: number, patient: number) => {
    let body = formatCreatePrescription(prescprion, record, patient)
    return await axios.post(`${urlApi}prescription/`, body , config)
}

export const listPrescription = async (record: number) => {
    return await axios.get(`${urlApi}prescription/doctor/${record}/`, config)
}


export const getPrescription = async (record: number) => {
    return await axios.get(`${urlApi}prescription-detail/doctor/${record}/`, config)
}
