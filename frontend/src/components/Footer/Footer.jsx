import styles from './Footer.module.css';

function Footer() {
  return (
    <footer className={styles.footer}>
      <span>© 2026 ДентаТайм</span>
      <span>Онлайн-запись к стоматологу</span>
    </footer>
  );
}

export default Footer;