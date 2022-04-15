import Image from "next/image";
import Link from "next/link";
import Card from "react-bootstrap/Card"

export enum Status {
  OnGoing,
  Hiatus,
  Finished,
}

export interface CardProps {
  title: string;
  rating: number;
  status: Status;
  cover: string;
  link: string;
  latest_chapters: string[];
}

const ComicCard = ({ props }: { props: CardProps }) => {
  return (
    <div>
      <Link href={props.link} passHref>
        <h2>{props.title}</h2>
      </Link>

      <Link href={props.link} passHref>
        <Image src={props.cover} width={230} height={350} alt={props.title} />
      </Link>

      <p>{props.rating}</p>
    </div>
  );
};

export default ComicCard;
