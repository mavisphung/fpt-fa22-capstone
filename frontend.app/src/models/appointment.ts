import { IPatient } from "./patient";

export enum AppointmentStatus {
    PENDING = 'PENDING',
    CHECKIN = 'CHECKIN',
    COMPLETED = 'COMPLETED',
    CANCELLED = 'CANCELLED',
}

export enum AppointmentType{
    ONLINE = 'ONLINE',
    OFFLINE = 'OFFLINE',
}

export interface IAppointment{
    id: number;
    bookedAt: Date|string;
    beginAt? : Date|string;
    endAt? : Date|string;
    estimatedAt? : Date|string;
    cancelReason?: string,
    category?: string,
    diseaseDescription?: string,
    checkInCode: string;
    type: AppointmentType;
    historical: object;
    patient: IPatient;
    doctor: object;
    booker: object;
    status: AppointmentStatus;
    package: object;
}
export interface IAppointmentFilter{
    bookedAt__gte: Date|string;
    bookedAt__lte: Date|string;
    patient__pk: number|null;
    status?: AppointmentStatus;
    page: number;
    limit: number;
}


