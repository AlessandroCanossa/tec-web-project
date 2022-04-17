import Link from "next/link";

import { useState } from "react";
import { Disclosure } from "@headlessui/react";
import { MenuIcon, XIcon, SearchIcon } from "@heroicons/react/outline";
import UserMenu from "./userMenu";
// import LoginModal from "./modals/login";

import styles from "./navbar.module.css";

const navigation = [
  { name: "Home", href: "/" },
  { name: "Genres", href: "#genre" },
  { name: "Popular", href: "#popular" },
];

const MyNavbar = () => {
  const [logged, setLoggedState] = useState(true);

  return (
    <Disclosure as="nav" className="bg-gray-900">
      {({ open }) => (
        <>
          <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div className="relative flex items-center justify-between h-16">
              <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                {/* Mobile menu button*/}
                <Disclosure.Button className={styles.menu_btn}>
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <MenuIcon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>

              {/* Navigation */}
              <div className={styles.nav_items}>
                <div className="hidden sm:block sm:ml-6">
                  <div className="flex space-x-4">
                    {navigation.map((item) => (
                      <Link href={item.href} passHref key={item.name}>
                        <a
                          className={
                            item.name === "Home"
                              ? styles.nav_home
                              : styles.nav_item
                          }
                        >
                          {item.name}
                        </a>
                      </Link>
                    ))}
                  </div>
                </div>
              </div>
              {/*search bar*/}
              <div className={styles.search_bar}>
                <input type="search" name="search" placeholder="Search" />
                <button type="submit">
                  <SearchIcon className={"block h-6 w-6"} />
                </button>
              </div>
              <div className={styles.account_zone}>
                {/* Profile dropdown */}
                {logged ? (
                  <UserMenu setLoggedState={setLoggedState} />
                ) : (
                  <>
                    <Link href={"/login"} passHref>
                      <button className={`${styles.btn} ${styles.btn_light}`}>
                        Log in
                      </button>
                    </Link>
                    <Link href={"/"} passHref>
                      <button className={`${styles.btn} ${styles.btn_dark}`}>
                        Sign up
                      </button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>

          <Disclosure.Panel className="sm:hidden">
            <div className={styles.menu}>
              {navigation.map((item) => (
                <Link href={item.href} passHref key={item.name}>
                  <Disclosure.Button as="a" className={styles.menu_item}>
                    {item.name}
                  </Disclosure.Button>
                </Link>
              ))}
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};
export default MyNavbar;
