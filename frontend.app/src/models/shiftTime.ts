export interface ShiftTime {
  id: number | undefined;
  weekday: number | undefined;
  startTime: string | undefined;
  endTime: string | undefined;
  isActive: boolean;
}

export interface ShiftTimes extends Array<ShiftTime> {}

export type Shifts = Map<string, ShiftTimes>;
