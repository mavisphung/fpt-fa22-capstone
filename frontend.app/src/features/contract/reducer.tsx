import { PayloadAction } from "@reduxjs/toolkit";

export interface ContractFilterState {
    status: string;
    startedAt__gte: Date | string;
    startedAt__lte: Date | string;
    keyword: string;
}