import { Link, NavLink } from 'react-router-dom';
import styles from './Header.module.css';

function getLinkClass({ isActive }) {
  if (isActive) {
    return `${styles.link} ${styles.active}`;
  }
  return styles.link;
}

function Header() {
  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>ДентаТайм</Link>
      <nav className={styles.nav}>
        <NavLink to="/services" className={getLinkClass}>Услуги</NavLink>
        <NavLink to="/doctors" className={getLinkClass}>Наши врачи</NavLink>
        <Link to="/login" className={styles.loginButton}>
          Войти
        </Link>
      </nav>
    </header>
  );
}

export default Header;