import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "app/store";
import { IPatient } from "models/patient";
import { HealthRecord, IMedicalInstruction, IPrescription} from "models/health_record";
import { ContractDetailPayload, ETreatmentContractStatus, UpdateStatusTreatmentContractPayload } from "./payload";

export interface TreatmentContract {
    id: number;
    beginAt: string;
    endAt: string;
    status: ETreatmentContractStatus | null;
    patient: IPatient
    healthrecord: HealthRecord;
}

export interface TreatmentContractFilter {
    fromDate: string | Date;
    toDate: string | Date;
    status: Array<ETreatmentContractStatus> | null;
    patientName: string | null;
}

export interface TreatmentContractSliceState {
    contracts: Array<TreatmentContract>;
    current: TreatmentContract | null;
    filter: TreatmentContractFilter;
}

const initialState: TreatmentContractSliceState = {
    contracts: [],
    current: null,
    filter: {
        fromDate: new Date('2021-12-12'),
        toDate: new Date(),
        status: [],
        patientName: null,
    }
}

export const treamtmentContractSlice = createSlice({
    name: 'treatment_contract',
    initialState,
    reducers: {
        loadContractFilter(state,action: PayloadAction<TreatmentContractFilter>){
            state.filter = action.payload
        },
        loadContractThroughFilter(state,action: PayloadAction<Array<TreatmentContract>>){
            state.contracts = action.payload
        },
        addPrescription(state,action: PayloadAction<IPrescription>){
            let contract = state.contracts.find(contract => contract.healthrecord.recordId === action.payload.healthRecord)
            contract?.healthrecord.prescriptions.push(action.payload)
            return state;
        },
        addInstruction(state,action:PayloadAction<IMedicalInstruction>){
            let contract = state.contracts.find(contract => contract.healthrecord.recordId === action.payload.healthRecord)
            contract?.healthrecord.instructions.push(action.payload)
            return state;
        },
        addNewContract(state, action:PayloadAction<TreatmentContract>){
            state.contracts.push(action.payload)
        },
        updateContractStatus(state, action:PayloadAction<UpdateStatusTreatmentContractPayload>){
            let contract = state.contracts.find(contract => contract.id === action.payload.contract)
            contract!.status = action.payload.status
        },
        updateContractHealthRecord(state, action:PayloadAction<ContractDetailPayload>){
            let contract = state.contracts.find(contract => contract.id === action.payload.contract);
            contract!.healthrecord = action.payload.healthRecord; 
        }
    }
})


export const contractReducer = treamtmentContractSlice.reducer
export const ContractAction  = treamtmentContractSlice.actions
// export const ContractListSelector = (state: RootState) => {return state.treatmentContract.contracts}
// export const ContractFilterSelector = (state: RootState) => {return state.treatmentContract.filter}
