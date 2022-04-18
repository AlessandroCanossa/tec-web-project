import Link from "next/link";
import styles from "./loginSocial.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebookF,
  faGoogle,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons";

const LoginSocial = () => {
  return (
    <>
      <div className=" w-full justify-content-md-center mb-4">
        <div className=" text-center">
          <p>OR Log in with</p>
        </div>
      </div>
      <div className=" flex flex-wrap mb-4 w-full">
        <div className="w-full md:w-1/3 md:text-right text-center">
          <Link href="/google-signin" passHref>
            <button className={styles.icon_btn}>
              <FontAwesomeIcon icon={faGoogle} className={styles.icon} />
            </button>
          </Link>
        </div>
        <div className="w-full md:w-1/3 text-center">
          <Link href="/facebook-signin" passHref>
            <button className={styles.icon_btn}>
              <FontAwesomeIcon icon={faFacebookF} className={styles.icon} />
            </button>
          </Link>
        </div>
        <div className="w-full md:w-1/3 md:text-left text-center">
          <Link href="/twitter-signin" passHref>
            <button className={styles.icon_btn}>
              <FontAwesomeIcon icon={faTwitter} className={styles.icon} />
            </button>
          </Link>
        </div>
      </div>
    </>
  );
};

export default LoginSocial;
