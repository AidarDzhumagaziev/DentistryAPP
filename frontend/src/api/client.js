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

export function refreshTokens(){
  return (
    fetch('/api/v1/auth/refresh/', {
      method: 'POST',
      headers: { Authorization: `Bearer ${localStorage.getItem('refresh_token')}` },
    }))
    .then((response) =>{
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
          })
    .then((data) => {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            return data.access_token
        })
    
}


function withToken(options) {
  return { ...options, headers: { ...options.headers, ...authHeaders() } };
}

export function authFetch(url, options = {}) {
  return fetch(url, withToken(options))
  .then((response) => {
    if (response.status !== 401) {
      return response;
    }
    return refreshTokens()
      .then(() => fetch(url, withToken(options)))
      .catch(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        throw new Error('Нужно войти заново');
      });
  });
}