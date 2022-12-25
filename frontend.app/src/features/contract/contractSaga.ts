import { PayloadAction } from "@reduxjs/toolkit";
import axios from "axios";
import { contractAction } from "features/contract/contractSlice";
import { take, call } from "redux-saga/effects";
import { ContractFilterState } from "./reducer";
import {listContract} from '../../api/contract_api'

function* handleFilterChange(action: PayloadAction<ContractFilterState>) {
    yield call(listContract,action.payload);
}

function* watchContractFilterChange(){
    let action: PayloadAction<ContractFilterState> = yield take(contractAction.changeFilter.type);
}
