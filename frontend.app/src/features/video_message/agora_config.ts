import {
  createClient,
  createMicrophoneAndCameraTracks,
  ClientConfig,
} from "agora-rtc-react";

export const appId = '2379244a079c45098b6d9040bb37aa85';
export const token:string |null = '007eJxTYOCJfP7u84J7KZLzfjhtevKjjK3mQa00Z8MhZb1J+2cJbniowGBkbG5pZGKSaGBumWxiamBpkWSWYmlgYpCUZGyemGhhqhNslSzAx8Dw67M2EyMDBIL47AzJGYl5qTmGDAwA5dofhA==';
export const channelName = 'channel1'
export const config: ClientConfig = {
  mode: 'rtc',
  codec: 'vp8',
}

export const useClient = createClient(config);
export const useMicrophoneAndCameraTracks = createMicrophoneAndCameraTracks();

