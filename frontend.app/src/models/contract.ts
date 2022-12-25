import { ContractStatus } from "./enum";
import { HealthRecord } from "./health_record";
import { InfoUser } from "./infoUser";
import { IPatient } from "./patient";

export interface SupervisorInfo{
    id: number;
    firstName: string;
    lastName: string;
}

export interface ITreamtentContract{    
        id: number,
        startedAt: Date|string,
        endedAt: Date|string,
        price: number,
        status: string | ContractStatus,
        doctor: InfoUser| undefined,
        patient: IPatient,
        supervisor: SupervisorInfo,
        healthRecord: HealthRecord[],
        detail: string | object | undefined ;
        service: object | any | undefined;
}

export interface ITreatmentSession{
    'id': number,
    'start': string,
    'end': string,
    'status': string,
    'date': string,
    'note': [],
    'assessment': [],
    'checkInCode': string,
    'cancelReason': string | null | any,
    'patient'?: object | any,
    'contract'?: object | any,
    'doctor'?: object | any,
    'supervisor'?: object | any,
    'isDoctorCancelled'?: boolean,
    'isSupervisorCancelled'?: boolean,
    'isSystemCancelled'?: boolean,
}