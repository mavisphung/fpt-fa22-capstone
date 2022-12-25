export interface Instruction {
  id: number | undefined;
  name: string | undefined;
}

export interface InstructionArray extends Array<Instruction> {}
