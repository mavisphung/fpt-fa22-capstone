import { HealthRecord, IMedicalInstruction, IPrescription } from "models/health_record";
import { IPatient } from "models/patient";

export enum ETreatmentContractStatus {
    APPROVED = 'APPROVED',
    REJECTED = 'REJECTED',
    CANCELLED = 'CANCELLED',
    IN_PROGRESS = 'IN_PROGRESS',
    COMPLETED = 'COMPLETED',
}

export interface TreatmentContractPayload{
    instructions: Array<IMedicalInstruction>,
    prescriptions: Array<IPrescription>,
    patient: IPatient,
}

export interface UpdateStatusTreatmentContractPayload{
    status: ETreatmentContractStatus,
    contract: number,
}

export interface ContractDetailPayload{
    healthRecord:HealthRecord,
    contract: number,
}