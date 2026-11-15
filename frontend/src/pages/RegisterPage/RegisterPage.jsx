import styles from './RegisterPage.module.css';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

function formatPhone(d) {
  let result = '+7';
  if (d.length > 0) result += ' ' + d.slice(0, 3);
  if (d.length > 3) result += ' ' + d.slice(3, 6);
  if (d.length > 6) result += '-' + d.slice(6, 8);
  if (d.length > 8) result += '-' + d.slice(8, 10);
  return result;
}

const serverErrors = {
  'Email already registered': 'Этот email уже зарегистрирован',
  'Phone already registered': 'Этот телефон уже зарегистрирован',
};

function RegisterPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [phoneDigits, setPhoneDigits] = useState('');
    const [full_name, setFullName] = useState('');
    const [error, setError] = useState(null);
    const { login } = useAuth();
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);

    function handleSubmit(e) {
        e.preventDefault();
        if (phoneDigits.length !== 10) {
            setError('Не правильный формат нелефона');
            return;
        }
        if (password.length < 8) {
            setError('Пароль должен быть не короче 8 символов');
            return;
        }
        setError(null);
        fetch('/api/v1/auth/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: full_name, email: email, phone: '+7' + phoneDigits, password: password }),
        })
        .then((response) => {
        if (!response.ok) {
            return response.json().then((body) => {
            throw new Error(body.detail);
            });
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
        .catch((err) => setError(serverErrors[err.message] || 'Не удалось зарегистрироваться'))
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
                    <input type="tel" className={styles.input}
                    value={formatPhone(phoneDigits)}
                    onChange={(e) => {
                        const digits = e.target.value.replace(/\D/g, '');
                        setPhoneDigits(digits.slice(1, 11));
                    }} />
                </label>
                <label className={styles.field}>
                    Пароль 
                    <div className={styles.passwordBox}>
                        <input
                            type={showPassword ? 'text' : 'password'}
                            className={styles.input}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <button type="button" className={styles.showButton} onClick={() => setShowPassword(!showPassword)}>
                            {showPassword ? 'Скрыть' : 'Показать'}
                        </button>
                    </div>
                </label>
                {error && <p className={styles.error}>{error}</p>}
                <button type="submit" className={styles.button}>Зарегистрироваться</button>
                <Link className={styles.login} to="/login">Войти</Link>
            </form>
        </div>
    )   
}
export default RegisterPage;