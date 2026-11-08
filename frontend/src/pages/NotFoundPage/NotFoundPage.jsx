import { Link } from 'react-router-dom';
import styles from './NotFoundPage.module.css';

function NotFoundPage() {
  return (
    <div className={styles.page}>
      <p className={styles.code}>404</p>
      <h1 className={styles.title}>Страница не найдена</h1>
      <p className={styles.text}>Возможно, ссылка устарела или в адресе опечатка.</p>
      <Link to="/" className={styles.button}>Вернуться на главную</Link>
    </div>
  );
}

export default NotFoundPage;