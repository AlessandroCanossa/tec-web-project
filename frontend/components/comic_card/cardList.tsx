import ComicCard, { CardProps } from "./comicCard";
import styles from "./cardList.module.css";

const cardList = ({ cards }: { cards: CardProps[] }) => {
  return (
    <section className={styles.card_list}>
      {cards.map((card) => (
        <ComicCard key={card.title} props={card} />
      ))}
    </section>
  );
};

export default cardList;
