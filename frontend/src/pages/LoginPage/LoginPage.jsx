import styles from './LoginPage.module.css';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function LoginPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const [error, setError] = useState(null);
    const navigate = useNavigate();

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
        .then((data) => {
            login(data.access_token, data.refresh_token)
            navigate('/');
        })
        .catch(() => setError('Неверный email или пароль'))
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
                {error && <p className={styles.error}>{error}</p>}
                <button type="submit" className={styles.button}>Войти</button>
                <Link to="/register">Нет аккаунта? Зарегистрироваться</Link>
            </form>
        </div>
    )   
}
export default LoginPage;