export var jsonHeaders = new Headers();
jsonHeaders.append('Content-Type', 'application/json');

export var imageHeader = new Headers();
imageHeader.append('Content-Type', 'image/jpeg');

export var requestOption: RequestInit = {
  method: '',
  headers: undefined,
  body: undefined,
  redirect: 'follow',
};
