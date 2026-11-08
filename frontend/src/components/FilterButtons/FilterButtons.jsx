import styles from './FilterButtons.module.css';

function FilterButtons({items, selectedId, onSelect}){
     function getFilterClass(id) {
          if (id === selectedId) {
          return `${styles.filter} ${styles.active}`;
          }
          return styles.filter
        }
    return( 
            <div className={styles.filters}>
            <button className={getFilterClass(null)}  onClick={() => onSelect(null)}>Все</button>
            {items.map((item) => (
            <button className={getFilterClass(item.id)} key={item.id}  onClick={() => onSelect(item.id)} >{item.name}</button>
        ))}
        </div>
        )
    }
export default FilterButtons;