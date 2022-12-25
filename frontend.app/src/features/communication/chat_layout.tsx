import {
  MainContainer,
  Sidebar,
  Search,
  ConversationList,
  Conversation,
  Avatar,
  ConversationHeader,
  MessageList,
  Message,
  MessageInput,
  ExpansionPanel,
  ChatContainer,
  MessageGroup,
  AttachmentButton,
} from '@chatscope/chat-ui-kit-react';
import { getChatMemberInfo } from 'api/userApi';
import { getMessages, sendMessage } from 'config/firebase';
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
import { init } from 'i18next';

type MyDivProps<T extends ElementType> = {
  as?: T;
  children: ReactNode;
};

export const MyDiv = <T extends ElementType = 'div'>({
  as,
  children,
  ...props
}: MyDivProps<T> & ComponentPropsWithoutRef<T>) => {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
};

export interface GuestMetaData {
  fullName: string;
  avatar: string;
}

export interface ICustomConversationProps {
  meta: ConverationMetadata;
  setSelectedConversation: (conversation: ConverationMetadata) => void;
  setSelectedGuest: (conversation: GuestMetaData) => void;
}

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

export const CustomConversation = (props: ICustomConversationProps) => {
  let conversation = props.meta;
  const [guest, setGuest] = useState<GuestMetaData>({
    fullName: '',
    avatar: '',
  });
  useEffect(() => {
    const init = async () => {
      let response = await (await getChatMemberInfo(conversation.supervisorId)).data;
      console.log('chat member info', response);
      setGuest(response);
    };
    init();
  }, []);
  return (
    <Conversation
      name=""
      lastSenderName={guest.fullName}
      info={conversation.lastMessage}
      onClick={(e) => {
        props.setSelectedConversation(conversation);
      }}
    >
      <Avatar src={guest.avatar} name={guest.fullName} status="away" />
    </Conversation>
  );
};

export const DoctorChatContainer = (props: { doctorId: number }) => {
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
  const [messageInputValue, setMessageInputValue] = useState('');
  const conversations = useConversation(props.doctorId);
  const [messages, setMessages] = useState<MessageItem[]>();
  const [selectedConversation, setSelectedConversation] = useState<ConverationMetadata>();
  const [selectedGuest, setSelectedGuest] = useState<GuestMetaData>({
    fullName: '',
    avatar: '',
  });
  const [groupedMessages, setGroupedMessages] = useState<Array<MessgageGroup>>();
  const [guests, setGuests] = useState<GuestMetaData[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let conversation = conversations[0] as ConverationMetadata;
    if (conversation !== undefined && conversations !== undefined) {
      getMessages(conversation.supervisorId + '-' + conversation.doctorId, setMessages);
      setSelectedConversation(conversation);
    }
    let promise = conversations.map((c: ConverationMetadata) => {
      return getChatMemberInfo(c.supervisorId);
    });
    Promise.all(promise).then((reps) => {
      reps.forEach((res) => {
        return guests.push(res.data);
      });
      setGuests([...guests]);
    });
  }, [conversations]);

  useEffect(() => {
    async function init() {
      if (selectedConversation) {
        let res = await getChatMemberInfo(selectedConversation.supervisorId);
        setSelectedGuest(res.data);
      }
    }
    init();
    if (selectedConversation !== undefined) {
      getMessages(
        selectedConversation.supervisorId + '-' + selectedConversation.doctorId,
        setMessages
      );
      if (selectedConversation.files === undefined) {
        selectedConversation.files = [];
        dispatch({ type: 'REMOVE_MEDIA', payload: { hasImage: false, center: true } });
      }
      if (selectedConversation.files.length > 0) {
        dispatch({ type: 'ADD_MORE_MEDIA', payload: { hasImage: false, center: true } });
      }
      if (selectedConversation.proposalText) {
        console.log('init proposal text');
        setMessageInputValue(selectedConversation!.proposalText);
      } else {
        setMessageInputValue('');
      }
    }
  }, [selectedConversation]);

  useEffect(() => {
    if (messages !== undefined) {
      let groupedMess = groupByVer2(messages);
      setGroupedMessages(groupedMess);
    }
  }, [messages]);

  const removeImage = (selectedIndex: number) => {
    console.log('on remove image');
    if (selectedConversation) {
      selectedConversation.files = selectedConversation?.files?.filter((value, index) => {
        return index !== selectedIndex;
      });
      selectedConversation.proposalFile = selectedConversation?.proposalFile?.filter(
        (value, index) => {
          return index !== selectedIndex;
        }
      );
      let updatedConversation = Object.assign({}, selectedConversation);
      if (selectedConversation.proposalFile?.length == 0) {
        dispatch({ type: 'REMOVE_MEDIA', payload: { center: true, hasImage: false } });
      }
      setSelectedConversation(updatedConversation);
    }
  };

  const handleOnImageChange = (index: ConverationMetadata, e: ChangeEvent<HTMLInputElement>) => {
    if (e.currentTarget.files) {
      let files = e.currentTarget.files as FileList;
      // let span_input = getComputedStyle(document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input').item(0) as Element)
      let imgCacheUrls = selectedConversation?.proposalFile;
      let conversationFile = selectedConversation?.files;
      if (conversationFile === undefined) {
        conversationFile = [];
      }
      if (imgCacheUrls === undefined) {
        imgCacheUrls = [];
      }
      for (let i = 0; i < files.length; i++) {
        let file = files.item(i) as File;
        imgCacheUrls.push(URL.createObjectURL(file));
        conversationFile.push(file);
      }
      selectedConversation!.proposalFile = imgCacheUrls;
      selectedConversation!.files = conversationFile;
      console.log('selectedConversation files', selectedConversation?.proposalFile);
      let updatedConversation = Object.assign({}, selectedConversation);
      setSelectedConversation(updatedConversation);
      dispatch({ type: 'ADD_MORE_MEDIA', payload: { hasImage: true, center: true } });
    }
    console.log('trigger input event');
  };

  const handleSendMultiTypeMessage = async (selectedConversation: ConverationMetadata) => {
    let textMessage = selectedConversation.proposalText?.replaceAll('(<)([a-zA-Z0-9]+)(>)', '');
    let mediaFile = selectedConversation.files as File[];
    console.log('textMessage', textMessage, mediaFile);
    if (mediaFile && mediaFile.length > 0) {
      let urls = await uploadImage(mediaFile);
      let urlMessages = urls.map((url) => url.slice(0, url.lastIndexOf('?')));
      let imgPromise = urlMessages.map((imgUrl) => {
        return sendMessage(
          selectedConversation.supervisorId,
          selectedConversation.doctorId,
          imgUrl,
          1
        );
      });
      Promise.all(
        imgPromise.concat(
          textMessage
            ? sendMessage(
                selectedConversation.supervisorId,
                selectedConversation.doctorId,
                textMessage,
                0
              )
            : []
        )
      );
    } else {
      if (textMessage) {
        sendMessage(
          selectedConversation.supervisorId,
          selectedConversation.doctorId,
          textMessage,
          0
        );
      }
    }
    selectedConversation.files = [];
    selectedConversation.proposalFile = [];
    selectedConversation.proposalText = undefined;
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
        height: '600px',
        position: 'relative',
      }}
    >
      <MainContainer responsive>
        <Sidebar position="left" scrollable={false}>
          <Search placeholder="Tìm kiếm cuộc trò chuyện..." />
          <ConversationList>
            {conversations !== undefined && guests.length > 0 ? (
              conversations.map((conversation: ConverationMetadata, index) => {
                let guest = guests[index];
                return (
                  <Conversation
                    active={
                      selectedConversation?.supervisorId === conversation.supervisorId
                        ? true
                        : false
                    }
                    lastSenderName={guest.fullName}
                    info={conversation.lastMessage}
                    onClick={(e) => {
                      setSelectedConversation(conversation);
                      setSelectedGuest(guest);
                    }}
                  >
                    <Avatar src={guest.avatar} name={guest.fullName} status="away" />
                  </Conversation>
                );
              })
            ) : (
              <></>
            )}
          </ConversationList>
        </Sidebar>

        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Back />
            <Avatar src={selectedGuest.avatar} name={selectedGuest.avatar} />
            <ConversationHeader.Content userName={selectedGuest.fullName} />
          </ConversationHeader>
          <MessageList>
            {groupedMessages !== undefined ? (
              groupedMessages.map((msg: MessgageGroup) => {
                let isHost = props.doctorId === msg.message[0].senderId;
                if (msg.type === 0)
                  return (
                    <MessageGroup
                      direction={msg.senderId !== props.doctorId ? 'incoming' : 'outgoing'}
                      sender={msg.senderId !== props.doctorId ? selectedGuest.avatar : ''}
                      avatarPosition="bl"
                    >
                      {isHost ? (
                        <></>
                      ) : (
                        <Avatar src={selectedGuest.avatar} name={selectedGuest.avatar} />
                      )}
                      <MessageGroup.Messages>
                        {msg.message.map((m) => (
                          <Message
                            model={{
                              direction: !isHost ? 'incoming' : 'outgoing',
                              type: 'text',
                              position: 'normal',
                              sender: !isHost ? '' : selectedGuest.fullName,
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
                      direction={msg.senderId !== props.doctorId ? 'incoming' : 'outgoing'}
                      sender={msg.senderId !== props.doctorId ? selectedGuest.avatar : ''}
                      className="image_group"
                      avatarPosition="bl"
                    >
                      {isHost ? (
                        <></>
                      ) : (
                        <Avatar src={selectedGuest.avatar} name={selectedGuest.avatar} />
                      )}
                      <MessageGroup.Messages
                        className={`cs-message-group__messages ${
                          isHost
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
                              sender: !isHost ? '' : selectedGuest.fullName,
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
                                sender: !isHost ? '' : selectedGuest.fullName,
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
                        sender: !isHost ? '' : selectedGuest.fullName,
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
              className={`conversation__detail__form__textAndPreview__preview ${
                state.hasImage ? 'conversation__detail__form__textAndPreview__preview--show' : ''
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
              {selectedConversation !== undefined &&
              selectedConversation!.proposalFile !== undefined ? (
                selectedConversation!.proposalFile!.map((src, index) => (
                  <div className="conversation__detail__form__textAndPreview__preview__item">
                    <span className="icon">
                      <FontAwesomeIcon
                        icon={faClose}
                        size="1x"
                        fixedWidth
                        onClick={(e) => {
                          removeImage(index);
                        }}
                        color={'#000000'}
                      />
                    </span>
                    <img
                      src={src}
                      className="conversation__detail__form__textAndPreview__preview__item"
                    />
                  </div>
                ))
              ) : (
                <></>
              )}
            </div>
            <input
              type={'file'}
              id="attactments"
              ref={inputRef}
              onChange={(e) => {
                handleOnImageChange(selectedConversation as ConverationMetadata, e);
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
                value={messageInputValue}
                onChange={(val) => {
                  selectedConversation!.proposalText = val;
                  setMessageInputValue(val);
                }}
                sendDisabled={false}
                onSend={(
                  innerHtml: string,
                  textContent: string,
                  innerText: string,
                  nodes: NodeList
                ) => {
                  handleSendMultiTypeMessage(selectedConversation as ConverationMetadata);
                }}
              />
            </div>
          </MyDiv>
        </ChatContainer>
      </MainContainer>
    </div>
  );
};
