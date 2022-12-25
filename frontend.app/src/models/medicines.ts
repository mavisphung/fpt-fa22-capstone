export interface Medicines {
  id: number | undefined;
  name: string | undefined;
}

export interface InstructionArray extends Array<Medicines> {}

