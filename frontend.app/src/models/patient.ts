export interface IPatient {
    id: number;
    firstName: string;
    lastName: string;
    avatar: string;
    address?: string;
    gender?: string;
    dob?: Date | string;
}

// export interface IPatient{
//     id: number;
//     firstName: string;
//     lastName: string;
//     gender: string;
//     avatar: string;
// }