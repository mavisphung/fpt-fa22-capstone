import { Medicines } from "./medicines";
import { IPatient } from "./patient";
import {Diseases} from './diseases'
export interface MedicationHistoryRecord {
    medicine: string;
    usage?: string;
    status?: string;
}

export interface HistoryOfPresentIllness {
    illness: string;
    recordDate: Date | string | null;
    severity: string;
}

export interface PatientMedicalHistory {
    chiefComplaint: string;
    allergies: string[];
    socialHistory: string[];
    historyOfPresentIllness: HistoryOfPresentIllness[],
    medicationHistory: MedicationHistoryRecord[];
}

export interface IDisease {
    code: string;
    otherCode: string;
    generalName: string;
    vGeneralName: string;
    diseaseName: string;
    vDiseaseName: string;
}


export interface IPrescriptionDetails {
    medicine: string;
    guide: string;
}

export interface IPrescriptionDetails3 {
    name: string;
    guide: string;
}

export interface IPrescriptionDetails2{
    medicine: Medicines | any;
    guide: string;
    quantity: number;
    unit: string;
}


// "id": 89,
// "createdAt": "2022-10-05T16:31:35.759857Z",
// "fromDate": "2022-10-05",
// "toDate": "2022-10-15",
// "cancelReason": null,
// "details"

export interface IPrescription {
    id: number;
    createdAt: Date|string;
    fromDate: Date|string;
    toDate: Date|string;
    cancelReason: string;
    details: IPrescriptionDetails2[],
    healthRecord: number;
    diagnose: Diseases[],
    note: string[]
}

export interface IPrescription2{
    id: number;
    createdAt: Date|string;
    fromDate: Date|string;
    toDate: Date|string;
    cancelReason: string;
    details: {
        medicine: string,
        guide: number,
        quantity: number,
        unit: string
    }[],
    healthRecord: number;
    diagnose: any,
    note: string[]
}


// export interface IMedicalInstruction {
//     id: number;
//     name: string;
//     detail: string;
//     diagnose: IDisease[],
//     result: string;
//     healthRecord: number;
// }

export interface IMedicalInstruction {
    "id": number,
    'createdAt': string,
    'category': string,
    'requirments': string,
    'submissions': string,
    'status': string,
    "patient"?: any|object,
    'doctor'?: any|object,
    healthRecord?: number;
}

export interface HealthRecord {
    patient: IPatient;
    recordId: number;
    name: string;
    description: string;
    medicalHistory: PatientMedicalHistory;
    instructions: IMedicalInstruction[];
    prescriptions: IPrescription[];
    detail?: object|any;
}