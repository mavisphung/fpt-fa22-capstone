import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "app/store";
import { ContractStatus } from "models/enum";
import { ContractFilterState } from "./reducer";


export interface ContractPagingAndFilterState{
    page: number;
    size: number;
    filter: ContractFilterState
}
const initialState:  ContractPagingAndFilterState = {
    page: 1,
    size: 10,
    filter: {
        startedAt__gte: new Date().toISOString(),
        startedAt__lte: new Date().toISOString(),
        keyword: '',
        status: ContractStatus.PENDING
    }
}

export const contractFilterSlice = createSlice({
    name: "contract",
    initialState,
    reducers:{
        changeFilter(state, action: PayloadAction<ContractFilterState>){
            state.filter = action.payload
        },
        changePage(state, action: PayloadAction<number>){
            state.page = action.payload
        },
    }
})

export const contractAction = contractFilterSlice.actions;
export const contractFilterReducer = contractFilterSlice.reducer;
export const contractFilterSelector = (state:RootState) =>  {return state.contract.filter};
export const contractPagingSelector = (state:RootState) => {return state.contract.page};