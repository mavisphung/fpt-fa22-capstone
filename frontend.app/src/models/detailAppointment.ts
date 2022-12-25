import { UserStorage } from './userStorage';

export interface DetailAppointmentData {
  id: number | undefined;
  beginAt: string | undefined;
  bookedAt: string | undefined;
  booker: Booker | undefined;
  cancelReason: string | undefined;
  checkInCode: string | undefined;
  endAt: string | undefined;
  package: Package | undefined;
  patient: Patient | undefined;
  status: string | undefined;
  type: string | undefined;
}

export interface Booker {
  email: string | undefined;
  firstName: string | undefined;
  lastName: string | undefined;
  id: number | undefined;
  phoneNumber: string | undefined;
}
export interface Package {
  id: number | undefined;
  description: string | undefined;
  name: string | undefined;
  price: number | undefined;
}

export interface Patient extends UserStorage {
  dob: string | undefined;
  address: string | undefined;
}
