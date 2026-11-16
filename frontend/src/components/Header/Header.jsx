import { Link, NavLink } from 'react-router-dom';
import styles from './Header.module.css';
import { useAuth } from '../../context/AuthContext';
import { useState } from 'react';


function getLinkClass({ isActive }) {
  if (isActive) {
    return `${styles.link} ${styles.active}`;
  }
  return styles.link;
}

function getCabinetPath(role) {
  if (role === 'doctor') {
    return '/doctor-cabinet'
  }
  if (role === 'admin') {
    return '/admin'
  }
  return '/account'
}

function Header() {
  const { token, logout, role } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo} onClick={() => setIsOpen(false)}>ДентаТайм</Link>
      <button
        type="button"
        className={styles.burger}
        aria-label={isOpen ? 'Закрыть меню' : 'Открыть меню'}
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '✕' : '☰'}
      </button>
      <nav
        className={isOpen ? `${styles.nav} ${styles.navOpen}` : styles.nav}
        onClick={() => setIsOpen(false)}
      >
        <NavLink to="/services" className={getLinkClass}>Услуги</NavLink>
        <NavLink to="/doctors" className={getLinkClass}>Наши врачи</NavLink>
        {token && <NavLink to={getCabinetPath(role)} className={getLinkClass}>Личный кабинет</NavLink>}
        {token ?
          <Link to="/login" className={styles.loginButton} onClick={logout}>Выйти</Link> :
          <Link to="/login" className={styles.loginButton}>Войти</Link>
        }
      </nav>
    </header>
  );
}

export default Header;
