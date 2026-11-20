import styles from './Footer.module.css';
import { CLINIC } from '../../data/clinic';

function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.contacts}>
        <span>ДентаТайм · {CLINIC.address}</span>
        <span>
          <a href={CLINIC.phoneLink} className={styles.phone}>{CLINIC.phone}</a> · {CLINIC.hours}
        </span>
      </div>
      <span>© 2026 ДентаТайм</span>
    </footer>
  );
}

export default Footer;