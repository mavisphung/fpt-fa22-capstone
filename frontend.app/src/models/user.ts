import { IAgoraRTCRemoteUser } from "agora-rtc-sdk-ng";

export interface User {
  firstName: string | undefined;
  lastName: string | undefined;
  address: string | undefined;
  gender: string | undefined;
  phoneNumber: string | undefined;
}

export interface AgoraRoom{
    host: IAgoraRTCRemoteUser, 
    guest: IAgoraRTCRemoteUser,
}