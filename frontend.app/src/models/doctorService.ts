export interface DoctorService {
  id: number | undefined;
  name: string | undefined;
  description: string | undefined;
  price: number | undefined;
  category: string | undefined;
}

export interface ServicesArray extends Array<DoctorService> {}
