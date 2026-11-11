export function getJson(url){
    return fetch(url).then((response)=> {
        if (!response.ok) {
      throw new Error('Сервер ответил ошибкой');
    }
    return response.json();
    });
}

export function authHeaders() {
  return { Authorization: `Bearer ${localStorage.getItem('access_token')}` };
}