import styles from './LoginPage.module.css';
import { useState } from 'react';

function LoginPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    function handleSubmit(e) {
        e.preventDefault();
        fetch('/api/v1/auth/login/', {
            method: 'POST',
            body: new URLSearchParams({ username: email, password: password }),
        })
        .then((response) =>{
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
        })
        .then((data) => console.log(data))
        .catch(() => console.log('Ошибка входа'))
    }

    return (
        <div className={styles.page}>
            <h1 className={styles.h1}>Вход</h1>
            <form className={styles.form} onSubmit={handleSubmit}>
                <label className={styles.field}>
                    Email 
                    <input type="email" className={styles.input} 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Пароль 
                    <input type="password" className={styles.input}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}/>
                </label>
                <button type="submit" className={styles.button}>Войти</button>
            </form>
        </div>
    )   
}
export default LoginPage;