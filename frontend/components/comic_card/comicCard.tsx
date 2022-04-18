import Image from "next/image";
import Link from "next/link";
import styles from "./comicCard.module.css";

import { StarIcon } from "@heroicons/react/solid";

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
  return (
    <div className={styles.card}>
      <div className={"col-start-1 hover:brightness-50"}>
        <Link href={"/series/" + props.link} passHref>
          <Image
            src={props.cover}
            width={240}
            height={320}
            layout={"responsive"}
            alt={props.title}
            className="rounded-md"
          />
        </Link>
      </div>
      <div className="col-start-2 mr-2">
        <div className="mb-8 flex flex-col">
          <Link href={"/series/" + props.link} passHref>
            <a className="text-gray-900 font-bold text-xl mb-2 hover:text-gray-500">
              {props.title}
            </a>
          </Link>
          {/* status */}
          <div className="flex flex-row justify-between">
            <div className="flex gap-1 items-center p-0.5">
              <p className="text-gray-700 text-xs ">{props.rating}</p>
              <StarIcon className="w-4 h-4 text-amber-500" />
            </div>
            <div className="flex gap-1 items-center p-0.5">
              <span
                className={`${styles.status_dot} ${styles.completed}`}
              ></span>
              <p className="text-gray-700 text-xs">{props.status}</p>
            </div>
          </div>
          {/* chapters */}
          <div className="flex flex-col">
            {props.latest_chapters
              .map((ch) => (
                <Link href={`/${props.link}-chapter-${ch}`} passHref key={ch}>
                  <a>Chapter {ch}</a>
                </Link>
              ))
              .reverse()}
            <Link href={`/series/${props.link}`} passHref>
              <a>All chapters</a>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComicCard;
