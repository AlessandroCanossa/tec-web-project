import { Dispatch, Fragment, SetStateAction } from "react";
import { Menu, Transition } from "@headlessui/react";
import { UserCircleIcon } from "@heroicons/react/outline";
import Link from "next/link";

import styles from "./userMenu.module.css";

const UserMenu = (props: {
  setLoggedState: Dispatch<SetStateAction<boolean>>;
}) => {
  return (
    <Menu as="div" className="ml-3 relative">
      <div>
        <Menu.Button className={styles.menu_btn}>
          <span className="sr-only">Open user menu</span>
          <UserCircleIcon className={styles.user_icon} />
        </Menu.Button>
      </div>
      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className={styles.menu_items}>
          <Menu.Item>
            <Link href={"/user/me"}>
              <a href="#" className={styles.menu_item}>
                Your Profile
              </a>
            </Link>
          </Menu.Item>
          <Menu.Item>
            <Link href={"#"} passHref>
              <a href="#" className={styles.menu_item}>
                Settings
              </a>
            </Link>
          </Menu.Item>
          <Menu.Item>
            <Link href={"/"} passHref>
              <a
                className={styles.menu_item}
                onClick={() => props.setLoggedState(false)}
              >
                Sign out
              </a>
            </Link>
          </Menu.Item>
        </Menu.Items>
      </Transition>
    </Menu>
  );
};
export default UserMenu;
