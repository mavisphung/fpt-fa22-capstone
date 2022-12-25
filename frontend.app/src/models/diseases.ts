export interface Diseases {
  id: number | undefined;
  code: string | undefined;
  generalName: string | undefined;
  diseaseName: string | undefined;
  otherCode: string | undefined;
}

export interface DiseasesArray extends Array<Diseases> {}
