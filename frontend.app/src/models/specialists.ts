export interface DoctorSpecialist {
  id: number | undefined;
  name: string | undefined;
  description: string | undefined;
}

export interface SpecialistArray extends Array<DoctorSpecialist> {}
