import Image from "next/image";
import Link from "next/link";
import styles from "./comicCard.module.css";
import { Card } from "react-bootstrap";

import { faStar, faCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export enum Status {
  ongoing = "Ongoing",
  hiatus = "Hiatus",
  completed = "Completed",
  cancelled = "Cancelled",
}

export interface CardProps {
  title: string;
  rating: number;
  status: Status;
  cover: string;
  link: string;
  latest_chapters: number[];
}

const ComicCard = ({ props }: { props: CardProps }) => {
  let dot_status;

  switch (props.status) {
    case Status.cancelled:
      dot_status = styles.cancelled;
      break;
    case Status.completed:
      dot_status = styles.completed;
      break;
    case Status.hiatus:
      dot_status = styles.hiatus;
      break;
    case Status.ongoing:
      dot_status = styles.ongoing;
      break;
  }

  return (
    <Card className={styles.card}>
      <Link href={props.link} passHref>
        <Card.Img as={"a"}>
          <Image
            width={"240px"}
            height={"320px"}
            alt={props.title}
            src={props.cover}
            className={styles.image}
          />
        </Card.Img>
      </Link>
      <div style={{ padding: "0 4px", width: "100%" }}>
        <Link href={props.link} passHref>
          <Card.Title as={"a"} className={styles.title}>
            {props.title}
          </Card.Title>
        </Link>
        <div className={styles.info_box}>
          <div className={styles.rating_box}>
            <span className={styles.rating}>{props.rating}</span>
            <FontAwesomeIcon icon={faStar} className={styles.star_icon} />
          </div>
          <div className={styles.status_box}>
            <FontAwesomeIcon
              icon={faCircle}
              className={`${styles.status_icon} ${dot_status}`}
            />
            <span className={styles.status}>{props.status}</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ComicCard;
