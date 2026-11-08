import styles from './LoginPage.module.css';

function LoginPage(){
    return (
        <div className={styles.page}>
            <h1 className={styles.h1}>Вход</h1>
            <form className={styles.form}>
                <label className={styles.field}>
                    Email 
                    <input type="email" className={styles.input}/>
                </label>
                <label className={styles.field}>
                    Пароль 
                    <input type="password" className={styles.input}/>
                </label>
                <button type="submit" className={styles.button}>Войти</button>
            </form>
        </div>
    )   
}
export default LoginPage;