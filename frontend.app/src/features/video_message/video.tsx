import {
  faMicrophone,
  faMicrophoneAltSlash,
  faPhoneAlt,
  faVideoCamera,
  faVideoSlash,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  AgoraVideoPlayer,
  IAgoraRTCRemoteUser,
  ICameraVideoTrack,
  IMicrophoneAudioTrack,
} from 'agora-rtc-react';
import { getToken } from 'api/userApi';
import { IPrescription } from 'models/health_record';
import React, { SetStateAction, useContext, useEffect, useState } from 'react';
import { appId, useClient, useMicrophoneAndCameraTracks } from './agora_config';
import './style/video.scss';
export const VideoCall = (props: {
  channelName: string;
  setInCall: React.Dispatch<SetStateAction<boolean>>;
}) => {
  const { channelName, setInCall } = props;
  const [users, setUsers] = useState<IAgoraRTCRemoteUser[]>([]);
  const [start, setStart] = useState<boolean>(false);
  let client = useClient();
  const { ready, tracks } = useMicrophoneAndCameraTracks();
  console.log(
    'users in room',
    users.map((m) => m.uid)
  );
  useEffect(() => {
    let init = async (name: string) => {
      client.on('user-published', async (user, mediaTypes) => {
        await client.subscribe(user, mediaTypes);
        if (mediaTypes === 'video' && user) {
          console.log('new publish user', user.videoTrack);
          setUsers([...users, user]);
        }
        if (mediaTypes === 'audio' && user) {
          user.audioTrack?.play();
        }
        console.log('publish');
      });
      client.on('user-unpublished', async (user, mediaTypes) => {
        console.log('unpub agora', mediaTypes, user);
        if (mediaTypes === 'video') {
          setUsers(users.filter((User) => User.uid !== user.uid));
        }
        if (mediaTypes === 'audio') {
          if (user.audioTrack) user.audioTrack.stop();
        }
      });
      client.on('user-left', (user) => {
        setUsers(users.filter((User) => User.uid !== user.uid));
      });
      let token = await (await getToken()).data.data.token;
      await client.join(appId, props.channelName, token, null);
      if (tracks) await client.publish(tracks);
      setStart(true);
    };
    if (ready && tracks) {
      init(channelName);
      console.log('init agora trigger');
    }
  }, [channelName, client, ready, tracks]);
  return (
    <div className="video_call_section">
      <div className="video_media">
        {start && tracks && <Videos users={users} tracks={tracks} />}
      </div>
      <div className="video_control">
        {ready && tracks && <Controls tracks={tracks} setStart={setStart} setInCall={setInCall} />}
      </div>
    </div>
  );
};

const Videos = (props: {
  users: IAgoraRTCRemoteUser[];
  tracks: [IMicrophoneAudioTrack, ICameraVideoTrack];
}) => {
  const { users, tracks } = props;
  return (
    <>
      <AgoraVideoPlayer
        className={`${users.length > 0 ? 'local_video' : 'remote_video'}`}
        videoTrack={tracks[1]}
      />
      {users.length > 0 && (
        <div className="remote_video">
          {users.length > 0 &&
            users.map((user) => {
              if (user.videoTrack) {
                return (
                  <AgoraVideoPlayer
                    style={{ height: '100%', width: '100%' }}
                    className="vid"
                    videoTrack={user.videoTrack}
                  />
                );
              }
            })}
        </div>
      )}
    </>
  );
};

export const Controls = (props: {
  tracks: [IMicrophoneAudioTrack, ICameraVideoTrack];
  setStart: React.Dispatch<React.SetStateAction<boolean>>;
  setInCall: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const client = useClient();
  const { tracks, setStart, setInCall } = props;
  const [trackState, setTrackState] = useState({ video: true, audio: true });

  useEffect(() => {
    console.log('effect trackes', tracks[1]);
  }, [tracks]);
  const mute = async (type: 'audio' | 'video') => {
    console.log('track info before ', tracks[1], tracks[1].enabled);
    if (type === 'audio') {
      await tracks[0].setEnabled(!trackState.audio);
      setTrackState((ps) => {
        return { ...ps, audio: !ps.audio };
      });
    } else if (type === 'video') {
      await tracks[1]
        .setEnabled(!trackState.video)
        .then(() => {
          console.log('track info after ', tracks[1]);
        })
        .catch((e) => {
          console.log(tracks[1].isPlaying);
          console.error('stop or resume not success', e);
        });
      setTrackState((ps) => {
        return { ...ps, video: !ps.video };
      });
    }
  };

  const leaveCall = async () => {
    await client.leave();
    client.removeAllListeners();
    tracks[0].close();
    tracks[1].close();
    setStart(false);
    setInCall(false);
  };
  return (
    <>
      <div className="btn_control" onClick={() => mute('audio')}>
        <div className="icon_wrapper">
          {trackState.audio ? (
            <FontAwesomeIcon icon={faMicrophone} />
          ) : (
            <FontAwesomeIcon icon={faMicrophoneAltSlash} />
          )}
        </div>
      </div>
      <div className="btn_control" onClick={() => mute('video')}>
        <div className="icon_wrapper">
          {trackState.video ? (
            <FontAwesomeIcon icon={faVideoCamera} />
          ) : (
            <FontAwesomeIcon icon={faVideoSlash} />
          )}
        </div>
      </div>
      {
        <div className="btn_control" onClick={() => leaveCall()}>
          <div className="icon_wrapper">
            <FontAwesomeIcon icon={faPhoneAlt}></FontAwesomeIcon>
          </div>
        </div>
      }
    </>
  );
};

export const PrescriptionModal = (props: IPrescription) => {
  return (
    <>
      <div className="video_table">
        <div className="video_table__header"></div>
        <div className="video_table__body">
          <div className="prescription">
            <div className="prescription__title"></div>
            <div className="prescirption__usage"></div>
            <div className=""></div>
          </div>
        </div>
      </div>
    </>
  );
};

export const VideoPage = () => {
  const [inCall, setInCall] = useState(true);
  const [channelName, setChanelName] = useState('aaa');
  return (
    <div className="page">
      <VideoCall setInCall={setInCall} channelName="aaa"></VideoCall>
      {/* <div className="shortcut_section">
                <div role='button'>Thêm Y Lệnh</div>
                <div role='button'>Thêm Đơn Thuốc</div>
                <div role='button'>Thêm Chuẩn Đoán</div>
            </div> */}
    </div>
  );
};
