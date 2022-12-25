import axios, { AxiosResponse } from "axios"
import { HealthRecord, IPrescription } from "models/health_record"
import {localUrl, urlApi} from "../constants/UrlApi"
const headers = {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
    'Content-Type': 'application/json'
}


const generateParams = (map: object) =>{
    let param = '?'
    for (const [key,value] of Object.entries(map)){
        console.log(key , value)
        if (value === undefined || value === null){
            param = param.concat(param,key,'=',value,'&')
        }
    }
    return param.slice(0,param.length-1)
}

export const loadHealthRecordByContract = async (contract:number) => {
    let response = await axios.get(`${localUrl}/doctor/health-records/${contract}/`, {headers: headers})
    return response

}

export const addPrecription = async (prescription:IPrescription) => {
    return await axios.post(localUrl, prescription, {
        headers: headers
    })
}

export const cancelPrescription = async (prescription:IPrescription) => {
    if(prescription.healthRecord === undefined || prescription.healthRecord === null) {
        return;
    }
    let response = await axios.get(`${localUrl}/doctor/health-records/${prescription.healthRecord}/`, {headers: headers})
    return response
}
