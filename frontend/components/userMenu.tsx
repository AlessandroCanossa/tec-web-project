import { Dispatch, Fragment, SetStateAction } from "react";
import { Dropdown, Button } from "react-bootstrap";
import Link from "next/link";
import { faUserCircle } from "@fortawesome/free-regular-svg-icons";

import styles from "./userMenu.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const UserMenu = (props: {
  setLoggedState: Dispatch<SetStateAction<boolean>>;
}) => {
  return (
    <Dropdown>
      <Dropdown.Toggle variant={"dark"}>
        {/*@ts-ignore*/}
        <FontAwesomeIcon icon={faUserCircle} size={"xl"}></FontAwesomeIcon>
      </Dropdown.Toggle>
      <Dropdown.Menu>
        <Dropdown.Item href="/user/me">Your profile</Dropdown.Item>
        <Dropdown.Item href="/settings">Settings</Dropdown.Item>
        <Dropdown.Divider></Dropdown.Divider>
        <Dropdown.Item>
          <Link href={"/"} passHref>
            <a
              className={"text-black text-decoration-none"}
              onClick={() => props.setLoggedState(false)}
            >
              Sign out
            </a>
          </Link>
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
    //
    //   <Menu as="div" className="ml-3 relative">
    // <div>
    // <Menu.Button className={ styles.menu_btn }>
    // <span className="sr-only">Open user menu</span>
    // <UserCircleIcon className={ styles.user_icon }/>
    // </Menu.Button>
    // </div>
    // <Transition
    //     as={ Fragment }
    //     enter="transition ease-out duration-100"
    //     enterFrom="transform opacity-0 scale-95"
    //     enterTo="transform opacity-100 scale-100"
    //     leave="transition ease-in duration-75"
    //     leaveFrom="transform opacity-100 scale-100"
    //     leaveTo="transform opacity-0 scale-95"
    //   >
    //     <Menu.Items className={ styles.menu_items }>
    //       <Menu.Item>
    //         <Link href={ "/user/me" }>
    //           <a href="#" className={ styles.menu_item }>
    //             Your Profile
    //           </a>
    //         </Link>
    //       </Menu.Item>
    //       <Menu.Item>
    //         <Link href={ "#" } passHref>
    //           <a href="#" className={ styles.menu_item }>
    //             Settings
    //           </a>
    //         </Link>
    //       </Menu.Item>
    //       <Menu.Item>
    //         <Link href={ "/" } passHref>
    //           <a
    //             className={ styles.menu_item }
    //             onClick={ () => props.setLoggedState(false) }
    //           >
    //             Sign out
    //           </a>
    //         </Link>
    //       </Menu.Item>
    //     </Menu.Items>
    //   </Transition>
    // </Menu>
  );
};
export default UserMenu;
