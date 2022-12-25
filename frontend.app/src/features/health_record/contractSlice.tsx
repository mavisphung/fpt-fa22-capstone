import { HealthRecord, IPrescription, IMedicalInstruction, IDisease,MedicationHistoryRecord } from "models/health_record";
import { IPatient } from "models/patient";

export interface HealthRecordPayload{
    patient: IPatient,
    diagnose: IDisease,
    historical:MedicationHistoryRecord,
    prescriptions: IPrescription[],
    instructions: IMedicalInstruction[]
}