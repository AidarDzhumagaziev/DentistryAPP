import styles from './RegisterPage.module.css';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

function RegisterPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [phone, setPhone] = useState('');
    const [full_name, setFullName] = useState('');
    const [error, setError] = useState(null);
    const { login } = useAuth();
    const navigate = useNavigate();

    function handleSubmit(e) {
        e.preventDefault();
        fetch('/api/v1/auth/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: full_name, email: email, phone: phone, password: password }),
        })
        .then((response) =>{
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
        })
        .then(() =>{
            return (fetch('/api/v1/auth/login/', {
            method: 'POST',
            body: new URLSearchParams({ username: email, password: password }),
            }))
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
        .catch(() => setError('Не удалось зарегистрироваться'))
    }

    return (
        <div className={styles.page}>
            <h1 className={styles.h1}>Регистрация</h1>
            <form className={styles.form} onSubmit={handleSubmit}>
                <label className={styles.field}>
                    ФИО 
                    <input type="text" className={styles.input} 
                    value={full_name}
                    onChange={(e) => setFullName(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Email 
                    <input type="email" className={styles.input} 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Телефон 
                    <input type="tel" placeholder="+79001234567" className={styles.input} 
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Пароль 
                    <input type="password" className={styles.input}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}/>
                </label>
                {error && <p className={styles.error}>{error}</p>}
                <button type="submit" className={styles.button}>Зарегистрироваться</button>
                <Link to="/login">Войти</Link>
            </form>
        </div>
    )   
}
export default RegisterPage;