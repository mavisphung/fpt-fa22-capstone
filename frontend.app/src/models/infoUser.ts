export interface InfoUser {
  email: string | undefined;
  firstName: string | undefined;
  lastName: string | undefined;
  dob: string | undefined;
  avatar: string | undefined;
  phoneNumber: string | undefined;
  address: string | undefined;
  gender: string | undefined;
  experienceYears: number | undefined;
  specialists: Array<number | undefined>;
}

export interface specsUrl {
  url: string | undefined;
  ext: string | undefined;
}
