export function getJson(url){
    return fetch(url).then((response)=> {
        if (!response.ok) {
      throw new Error('Сервер ответил ошибкой');
    }
    return response.json();
    });
}