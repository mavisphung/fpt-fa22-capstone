import {
  MainContainer,
  ChatContainer,
  ConversationHeader,
  Avatar,
  VideoCallButton,
  InfoButton,
  MessageList,
  MessageGroup,
  Message,
  MessageInput,
  AttachmentButton,
} from '@chatscope/chat-ui-kit-react';
import { getChatMemberInfo } from 'api/userApi';
import { getMessages, sendMessage, sendToAppointment } from 'config/firebase';
import { useConversation } from 'hooks/useConversation';
import React, { ChangeEvent, useEffect, useReducer, useRef, useState } from 'react';
import { ConverationMetadata, MessageItem } from './chat_section';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import 'features/communication/conversation.scss';
import { faClose } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { ComponentPropsWithoutRef, ElementType, ReactNode } from 'react';
import { groupByVer2, MessgageGroup } from 'utils/utils';
import { documentId } from 'firebase/firestore';
import { uploadImage } from 'api/uploader_api';
import { AppointmentStatus, AppointmentType, IAppointment } from 'models/appointment';
import { IPatient } from 'models/patient';
import { MyDiv } from './chat_layout';
import { fetchAppointment } from 'api/appointmentApi';
import { init } from 'i18next';
import { InfoUser } from 'models/infoUser';
import '../communication/conversation.scss';
import { useParams } from 'react-router-dom';

interface StyleReduceState {
  center: boolean;
  hasImage: boolean;
}

interface StyleActionState {
  type: string;
  payload: StyleReduceState;
}

const defaultStyle: StyleReduceState = {
  center: true,
  hasImage: false,
};


let initApp: IAppointment = {
  id: 187,
  bookedAt: '2022-11-29 18:00:00',
  beginAt: '2022-11-28 10:08:51',
  endAt: '2022-11-28 10:09:53',
  category: 'AT_DOCTOR_HOME',
  checkInCode: '257394-13-2-5',
  status: AppointmentStatus.COMPLETED,
  type: AppointmentType.ONLINE,
  cancelReason: '',
  diseaseDescription: 'fhdhdvv',
  patient: {
    id: 2,
    firstName: 'Phong',
    lastName: 'Hoàng',
    dob: '1995-05-09',
    avatar: 'https://cuu-be.s3.amazonaws.com/cuu-be/2022/11/10/KUKCDV.jpg',
    address: '218/25 Hồng Bàng, Phưởng 12, Quận 5, Thành phố Hồ Chí Minh, Việt Nam',
  },
  doctor: {
    id: 5,
    firstName: 'Lê Thành',
    lastName: 'Đạt',
    age: 39,
    experienceYears: 12.0,
    gender: 'MALE',
    address: '215 Hồng Bàng, Phường 11, Quận 5, Thành phố Hồ Chí Minh, Việt Nam',
    avatar: 'https://cuu-be.s3.amazonaws.com/cuu-be/2022/11/14/UZ944B.jpg',
    rate: 0,
    email: 'doctor@gmail.com',
  },
  booker: {
    id: 13,
    firstName: 'Huy',
    lastName: 'Phùng Chí',
    phoneNumber: '0349797318',
    email: 'nguoibimatthegioi@gmail.com',
  },
  package: {
    id: 6,
    name: 'Khám tổng quát cơ bản',
    price: 3500000.0,
    description:
      'Giúp Bạn Phát Hiện Sớm Bệnh Tình, Điều Trị Kịp Thời. Giúp Bạn An Tâm Về Sức Khỏe. Dịch Vụ Khám Nhanh Chóng, Chu Đáo',
  },
  historical: {
    id: 187,
    bookedAt: '2022-11-29 18:00:00',
    beginAt: '2022-11-28 10:08:51',
    endAt: '2022-11-28 10:09:53',
    estEndAt: null,
    checkInCode: '257394-13-2-5',
    status: 'COMPLETED',
    cancelReason: null,
    diseaseDescription: 'fhdhdvv',
    patient: {
      id: 2,
      firstName: 'Phong',
      lastName: 'Hoàng',
      dob: '1995-05-09',
      avatar: 'https://cuu-be.s3.amazonaws.com/cuu-be/2022/11/10/KUKCDV.jpg',
      address: '218/25 Hồng Bàng, Phưởng 12, Quận 5, Thành phố Hồ Chí Minh, Việt Nam',
    },
    doctor: {
      id: 5,
      firstName: 'Lê Thành',
      lastName: 'Đạt',
      age: 39,
      experienceYears: 12.0,
      gender: 'MALE',
      address: '215 Hồng Bàng, Phường 11, Quận 5, Thành phố Hồ Chí Minh, Việt Nam',
      avatar: 'https://cuu-be.s3.amazonaws.com/cuu-be/2022/11/14/UZ944B.jpg',
      rate: 0,
      email: 'doctor@gmail.com',
    },
    booker: {
      id: 13,
      firstName: 'Huy',
      lastName: 'Phùng Chí',
      phoneNumber: '0349797318',
      email: 'nguoibimatthegioi@gmail.com',
    },
    package: {
      id: 6,
      name: 'Khám tổng quát cơ bản',
      price: 3500000.0,
      description:
        'Giúp Bạn Phát Hiện Sớm Bệnh Tình, Điều Trị Kịp Thời. Giúp Bạn An Tâm Về Sức Khỏe. Dịch Vụ Khám Nhanh Chóng, Chu Đáo',
      category: 'AT_DOCTOR_HOME',
    },
    historical: null,
  },
};


export const AppointmentChatRoom: React.FC<any> = (props) => {
  console.log('props', props.appointment);
  const layoutReducer = (state: StyleReduceState, action: StyleActionState) => {
    switch (action.type) {
      case 'ADD_MORE_MEDIA': {
        return {
          center: true,
          hasImage: true,
        };
      }
      case 'REMOVE_MEDIA': {
        return {
          center: true,
          hasImage: false,
        };
      }
      case 'TEXT_NEED_CENTER': {
        return {
          center: true,
          hasImage: false,
        };
      }
      default: {
        return state;
      }
    }
  };
  const [state, dispatch] = useReducer(layoutReducer, defaultStyle);
  const [appointment, setAppointment] = useState<IAppointment>(initApp)
  //   let appointment: IAppointment = props.appointment;
  let selectedGuest: IPatient = appointment.patient;
  let fullName = selectedGuest.lastName.concat(' ', selectedGuest.firstName);
  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [groupedMessages, setGroupedMessages] = useState<Array<MessgageGroup>>();
  const [media, setMedia] = useState<Array<string>>([]);
  const [files, setFile] = useState<File[]>([]);
  const [proposalText, setProposalText] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (messages !== undefined && messages.length > 0) {
      let groupedMess = groupByVer2(messages);
      setGroupedMessages(groupedMess);
    } else {
      setGroupedMessages([])
    }
  }, [messages]);

  useEffect(() => {
    if (props.appointment === undefined) {
    } else {
      setAppointment(props.appointment)
      console.log('room: ', props.appointment.booker.id.toString().concat('-', props.appointment.doctor.accountId));
      getMessages(props.appointment.booker.id.toString().concat('-', props.appointment.doctor.accountId), setMessages);
    }
  }, [props, props.appointment]);

  const removeImage = (selectedIndex: string) => {
    console.log('on remove image');
    let index = media.findIndex((s) => s === selectedIndex);
    let left = files.slice(0, index);
    let result = left.concat(files.slice(index + 1));
    let newMedia = media.filter((s) => s !== selectedIndex);
    setFile(result);
    setMedia(newMedia);
  };

  const handleOnImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.currentTarget.files) {
      let currentFiles = e.currentTarget.files as FileList;
      // let span_input = getComputedStyle(document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input').item(0) as Element)
      let imgCacheUrls = media;
      let newFiles = files;
      if (imgCacheUrls === undefined) {
        imgCacheUrls = [];
      }
      if (newFiles === undefined) {
        newFiles = [];
      }
      for (let i = 0; i < e.currentTarget.files.length; i++) {
        let file = currentFiles.item(i) as File;
        imgCacheUrls.push(URL.createObjectURL(file));
        newFiles.push(file);
      }
      setFile(newFiles);
      setMedia(imgCacheUrls);
    }
    dispatch({ type: 'ADD_MORE_MEDIA', payload: { hasImage: true, center: true } });
    console.log('trigger input event');
  };

  const handleSendMultiTypeMessage = async () => {
    console.log(props.appointment)
    let sup: any = props.appointment.booker;
    let doc: any = props.appointment.doctor;
    let textMessage = proposalText.replaceAll('<br>','');
    if (files && files.length > 0) {
      console.log('files', textMessage);
      let urls = await uploadImage(files).then(res => {
        let urlMessages = res.map((url) => url.slice(0, url.lastIndexOf('?')));
        let imgPromise = urlMessages.map((imgUrl) => {
          return sendMessage(sup.id, doc.accountId, imgUrl, 1);
        });
        Promise.all(
          imgPromise
        );
      });
    }
    if (textMessage.length > 0) {
      console.log('send room', sup.id, doc.accountId)
      sendMessage(sup.id, doc.accountId, textMessage, 0);
    }
    setTimeout(() => {
      dispatch({ type: 'REMOVE_MEDIA', payload: { hasImage: true, center: true } });
      setMedia([]);
      setFile([]);
      setProposalText('');
    }, 1000)

  };

  const handleMediaClick = (src: string) => {
    popupCenter(src, 'media content', 800, 800);
  };

  const popupCenter = (url: string, title: string, w: number, h: number) => {
    // Fixes dual-screen position                             Most browsers      Firefox
    const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
    const dualScreenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;

    const width = window.innerWidth
      ? window.innerWidth
      : document.documentElement.clientWidth
        ? document.documentElement.clientWidth
        : w;
    const height = window.innerHeight
      ? window.innerHeight
      : document.documentElement.clientHeight
        ? document.documentElement.clientHeight
        : h;

    const systemZoom = width / window.screen.availWidth;
    const left = (width - w) / 2 / systemZoom + dualScreenLeft;
    const top = (height - h) / 2 / systemZoom + dualScreenTop;
    const newWindow = window.open(
      url,
      title,
      `
          scrollbars=yes,
          width=${w / systemZoom}, 
          height=${h / systemZoom}, 
          top=${top}, 
          left=${left}
          `
    );
  };

  return (
    <div
      style={{
        width: '100%',
        height: '600px',
        position: 'relative',
      }}
    >
      <MainContainer responsive>
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Back />
            <Avatar src={selectedGuest.avatar} name={fullName} />
            <ConversationHeader.Content userName={props.a} />
            <ConversationHeader.Actions>
              <VideoCallButton onClick={props.openVideoCallWindow} />
              {/* <InfoButton /> */}
            </ConversationHeader.Actions>
          </ConversationHeader>
          <MessageList>
            {groupedMessages !== undefined && groupedMessages.length > 0 ? (
              groupedMessages.map((msg: MessgageGroup) => {
                let doctorId = Number.parseInt(props.appointment.doctor.accountId as string);
                let isHost = doctorId === msg.message[0].senderId;
                if (msg.type === 0)
                  return (
                    <MessageGroup
                      direction={msg.senderId !== doctorId ? 'incoming' : 'outgoing'}
                      sender={msg.senderId !== doctorId ? selectedGuest.avatar : ''}
                      avatarPosition="bl"
                    >
                      {isHost ? (
                        <></>
                      ) : (
                        <Avatar src={props.appointment.patient.avatar} name={selectedGuest.avatar} />
                      )}
                      <MessageGroup.Messages>
                        {msg.message.map((m) => (
                          <Message
                            model={{
                              direction: !isHost ? 'incoming' : 'outgoing',
                              type: 'text',
                              position: 'normal',
                              sender: !isHost ? '' : fullName,
                              sentTime: m.createdAt.toString(),
                            }}
                          >
                            <Message.TextContent>{m.content}</Message.TextContent>
                          </Message>
                        ))}
                      </MessageGroup.Messages>
                    </MessageGroup>
                  );
                if (msg.type === 1) {
                  let firstTwoDiv: MessageItem[] = [];
                  let secondThirdDiv: MessageItem[] = [];
                  if (msg.message.length > 3) {
                    firstTwoDiv = msg.message.slice(0, 2);
                    secondThirdDiv = msg.message.slice(2);
                  } else {
                    firstTwoDiv = msg.message;
                  }
                  return (
                    <MessageGroup
                      direction={msg.senderId !== doctorId ? 'incoming' : 'outgoing'}
                      sender={msg.senderId !== doctorId ? selectedGuest.avatar : ''}
                      className="image_group"
                      avatarPosition="bl"
                    >
                      {isHost ? (
                        <></>
                      ) : (
                        <Avatar src={selectedGuest.avatar} name={selectedGuest.avatar} />
                      )}
                      <MessageGroup.Messages
                        className={`cs-message-group__messages ${isHost
                          ? 'cs-message-group__messages--flex_outgoing'
                          : 'cs-message-group__messages--flex_incoming'
                          }`}
                      >
                        {firstTwoDiv.map((m) => (
                          <Message
                            model={{
                              direction: !isHost ? 'incoming' : 'outgoing',
                              type: 'image',
                              position: 'normal',
                              sender: !isHost ? '' : fullName,
                              sentTime: m.createdAt.toString(),
                            }}
                            onClick={(e) => {
                              e.preventDefault();
                              handleMediaClick(m.content);
                            }}
                          >
                            <Message.ImageContent
                              src={m.content}
                              width={384 / (firstTwoDiv.length > 2 ? 3 : 2)}
                              height={384 / (firstTwoDiv.length > 2 ? 3 : 2)}
                            />
                          </Message>
                        ))}
                        {secondThirdDiv.length > 0 ? (
                          secondThirdDiv.map((m) => (
                            <Message
                              model={{
                                direction: !isHost ? 'incoming' : 'outgoing',
                                type: 'image',
                                position: 'normal',
                                sender: !isHost ? '' : fullName,
                                sentTime: m.createdAt.toString(),
                              }}
                              onClick={(e) => {
                                console.log('img click with new window');
                                window.open(m.content);
                              }}
                            >
                              <Message.ImageContent
                                src={m.content}
                                width={384 / 3}
                                height={384 / 3}
                              />
                            </Message>
                          ))
                        ) : (
                          <></>
                        )}
                      </MessageGroup.Messages>
                    </MessageGroup>
                  );
                }
                if (msg.type === 2)
                  return (
                    <Message
                      model={{
                        direction: !isHost ? 'incoming' : 'outgoing',
                        type: 'text',
                        position: 'normal',
                        sender: !isHost ? '' : fullName,
                      }}
                    >
                      {isHost ? (
                        <></>
                      ) : (
                        <Avatar src={selectedGuest.avatar} name={selectedGuest.avatar} />
                      )}
                      {msg.message.map((m) => (
                        <Message.HtmlContent html=""></Message.HtmlContent>
                      ))}
                    </Message>
                  );
                return <></>;
              })
            ) : (
              <div></div>
            )}
            <div></div>
          </MessageList>
          <MyDiv as={MessageInput} className={'cs-message-input__content-editor-wrapper'}>
            <div
              className={`conversation__detail__form__textAndPreview__preview ${state.hasImage ? 'conversation__detail__form__textAndPreview__preview--show' : ''
                }`}
            >
              <AttachmentButton
                onClick={(e) => {
                  console.log('on attachButton');
                  if (inputRef !== undefined && inputRef !== null) {
                    document.getElementById('attactments')?.click();
                  }
                }}
              ></AttachmentButton>
              {media.map((src, index) => (
                <div className="conversation__detail__form__textAndPreview__preview__item">
                  <span className="icon">
                    <FontAwesomeIcon
                      icon={faClose}
                      size="1x"
                      fixedWidth
                      onClick={(e) => {
                        removeImage(src);
                      }}
                      color={'#000000'}
                    />
                  </span>
                  <img
                    src={src}
                    className="conversation__detail__form__textAndPreview__preview__item"
                  />
                </div>
              ))}
            </div>
            <input
              type={'file'}
              id="attactments"
              ref={inputRef}
              onChange={(e) => {
                handleOnImageChange(e);
              }}
            ></input>
            <div>
              <MessageInput
                ref={inputRef}
                attachButton={state.hasImage ? false : true}
                onAttachClick={(e) => {
                  console.log('on attachButton');
                  if (inputRef !== undefined && inputRef !== null) {
                    document.getElementById('attactments')?.click();
                  }
                }}
                placeholder="Type message here"
                sendButton={true}
                value={proposalText}
                onChange={(val) => {
                  setProposalText(val);
                }}
                sendDisabled={false}
                onSend={(
                  innerHtml: string,
                  textContent: string,
                  innerText: string,
                  nodes: NodeList
                ) => {
                  handleSendMultiTypeMessage();
                }}
              />
            </div>
          </MyDiv>
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export const InitChatBox: React.FC<any> = (props) => {
  const [app, setApp] = useState<IAppointment>();
  const { id } = useParams<{ id: string }>()
  useEffect(() => {
    const init = async () => {
      let res = await fetchAppointment(Number.parseInt(props.id));
      setApp(res.data.data);
      console.log('response', res.data.data);
    };
    init();
    console.log('useEffect trigger')
  }, [props.id]);

  useEffect(() => {
    const init = async () => {
      let res = await fetchAppointment(Number.parseInt(props.id));
      setApp(res.data.data);
      console.log('response', res.data.data);
    };
    init();
  }, []);
  return (
    <div className="chat_container">
      <div className="button_section">
        <button onClick={props.navigateNewHealthRecord}>Chuẩn đoán và kê đơn</button>
        {/* <button>Thêm y lệnh</button> */}
      </div>
      <div className="chat_section">
        <AppointmentChatRoom appointment={app} openVideoCallWindow={props.openVideoCallWindow} />
      </div>
    </div>
  );
};
