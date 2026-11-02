import styles from './Header.module.css';

function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>ДентаПлан</div>
      <nav className={styles.nav}>
        <a href="#">Услуги</a>
        <a href="#">Врачи</a>
        <a href="#">Войти</a>
      </nav>
    </header>
  );
}

export default Header;