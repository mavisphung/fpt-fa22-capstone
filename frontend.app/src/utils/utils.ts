import { MessageItem } from '../features/communication/chat_section';

export interface MessgageGroup {
  senderId?: number;
  message: Array<MessageItem>;
  type: number;
}

export const groupBy = (messages: MessageItem[]) => {
  let currentSender = messages[0].senderId;
  let currentIndex = 0;
  let result: Array<MessageItem[]> = [];
  messages.forEach((message) => {
    let newGroup: MessageItem[];
    if (message.senderId === currentSender && message.type === 0) {
      newGroup =
        result[currentIndex] === undefined || result[currentIndex] === null
          ? []
          : result[currentIndex];
      newGroup.push(message);
      result[currentIndex] = newGroup;
    } else if (message.senderId !== currentSender && message.type === 0) {
      currentIndex = currentIndex + 1;
      currentSender = message.senderId;
      newGroup =
        result[currentIndex] === undefined || result[currentIndex] === null
          ? []
          : result[currentIndex];
      newGroup.push(message);
      result[currentIndex] = newGroup;
    } else if (message.senderId === currentSender && message.type !== 0) {
      currentIndex = currentIndex + 1;
      currentSender = message.senderId;
      newGroup =
        result[currentIndex] === undefined || result[currentIndex] === null
          ? []
          : result[currentIndex];
      newGroup.push(message);
      result[currentIndex] = newGroup;
    } else if (message.senderId !== currentSender && message.type !== 0) {
      currentIndex = currentIndex + 1;
      currentSender = message.senderId;
      newGroup =
        result[currentIndex] === undefined || result[currentIndex] === null
          ? []
          : result[currentIndex];
      newGroup.push(message);
      result[currentIndex] = newGroup;
    }
  });
  return result;
};

export const groupByVer2 = (messages: MessageItem[]) => {
  let currentSender = messages[0].senderId;
  let currentIndex = 0;
  let result: Array<MessgageGroup> = [];
  let hasImageBefore = false;
  // console.log(messages.map(m => {return {'message': m.content, 'type': m.type}}))
  messages.forEach((message, index) => {
    let newGroup: MessgageGroup;
    if (message.type !== 0 && message.senderId === currentSender) {
      currentIndex = hasImageBefore ? currentIndex : currentIndex + 1;
      newGroup =
        result[currentIndex] !== undefined
          ? result[currentIndex]
          : { message: [], type: 1, senderId: currentSender };
      // console.log('type media', 'actual type:', newGroup.type, 'message:', message.content, result[currentIndex] !== undefined, 'index', currentIndex)
      newGroup.message.push(message);
      result[currentIndex] = newGroup;
      hasImageBefore = true;
    }
    if (message.type === 0 && message.senderId === currentSender) {
      console.log(currentIndex,'befofore', 'has image before')
      currentIndex = !hasImageBefore ? currentIndex : currentIndex + 1;
      newGroup =
        result[currentIndex] !== undefined
          ? result[currentIndex]
          : { message: [], type: 0, senderId: currentSender };
      newGroup.message.push(message);
      console.log('type text', 'actual type:', newGroup.type, 'message:', message.content, ',has Image then text', !hasImageBefore, ',index', currentIndex, ',new group', result[currentIndex] !== undefined);
      result[currentIndex] = newGroup;
      hasImageBefore = false;
    }
    if (message.type !== 0 && message.senderId !== currentSender) {
      currentSender = message.senderId;
      currentIndex = currentIndex + 1;
      newGroup =
        result[currentIndex] !== undefined
          ? result[currentIndex]
          : { message: [], type: 1, senderId: currentSender };
      newGroup.message.push(message);
      result[currentIndex] = newGroup;
      // console.log('type media - change user', 'actual type:', newGroup.type, 'message:', message.content, result[currentIndex] !== undefined,'index', currentIndex)
      hasImageBefore = true;
    }
    if (message.type === 0 && message.senderId !== currentSender) {
      currentSender = message.senderId;
      currentIndex = currentIndex + 1;
      newGroup =
        result[currentIndex] !== undefined
          ? result[currentIndex]
          : { message: [], type: 0, senderId: currentSender };
      newGroup.message.push(message);
      result[currentIndex] = newGroup;
      // console.log('type text user change', 'actual type:', newGroup.type, 'message:', message.content, result[currentIndex] !== undefined,'index', currentIndex)
      hasImageBefore = false;
    }
  });
  // console.log('result of groupByVer2', result.map(g => {return {'length': g.message.length, 'message': g.message.map(m => m.content)}}))
  return result;
};

export const options: Intl.DateTimeFormatOptions = {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
};
export const optionsTime: Intl.DateTimeFormatOptions = { hour: '2-digit', minute: '2-digit' };
