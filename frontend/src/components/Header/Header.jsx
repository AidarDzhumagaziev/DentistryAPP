import { Link, NavLink } from 'react-router-dom';
import styles from './Header.module.css';
import {useAuth} from '../../context/AuthContext';


function getLinkClass({ isActive }) {
  if (isActive) {
    return `${styles.link} ${styles.active}`;
  }
  return styles.link;
}

function Header() {
  const { token, logout } = useAuth();
  
  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>ДентаТайм</Link>
      <nav className={styles.nav}>
        <NavLink to="/services" className={getLinkClass}>Услуги</NavLink>
        <NavLink to="/doctors" className={getLinkClass}>Наши врачи</NavLink>
        {token && <NavLink to="/account" className={getLinkClass}>Личный кабинет</NavLink>}
        {token ? 
        <Link to="/login" className={styles.loginButton} onClick={logout}>Выйти</Link>:
        <Link to="/login" className={styles.loginButton}>Войти</Link>
        }
      </nav>
    </header>
  );
}

export default Header;