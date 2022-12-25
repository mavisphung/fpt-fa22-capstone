export interface Prescription {
  id: number | undefined;
  name: string | undefined;
  quantity: string | undefined;
  unit: string | undefined;
  guide: string | undefined;
}

export interface PrescriptionArray extends Array<Prescription> {}
