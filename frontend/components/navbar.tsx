import Link from "next/link";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faSearch } from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";

import LoginModal from "./modals/login";

import styles from "./navbar.module.css";

let logged = false;

const MyNavbar = () => {
  const [loginModalShow, setLoginModalShow] = useState(false);

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Link href="/">
          <a className="navbar-brand">Home</a>
        </Link>
        <Nav className="me-auto">
          <Link href="#genre">
            <a className="nav-link">Genres</a>
          </Link>
          <Link href="#popular">
            <a className="nav-link">Popular</a>
          </Link>
        </Nav>
        <Form className="d-flex me-5" method="get" action="">
          {/* TODO: set action to get the search */}
          <FormControl
            type="search"
            placeholder="Search"
            className={`me-2 bg-dark text-white ${styles.search_bar}`}
          />
          <Button
            type="submit"
            variant="outline-light"
            className={`me-2 ${styles.search_btn}`}
          >
            <FontAwesomeIcon icon={faSearch} />
          </Button>
        </Form>

        {logged ? (
          <Link href="/account" passHref>
            <Button variant="outline-light">
              <FontAwesomeIcon icon={faUser} className="me-2"></FontAwesomeIcon>
              <span>Username</span>
            </Button>
          </Link>
        ) : (
          <>
            <Button
              variant="outline-light"
              className="me-2"
              onClick={() => setLoginModalShow(true)}
            >
              Log in
            </Button>
            <Link href="/registration" passHref>
              <Button variant="light">Sign up</Button>
            </Link>
            <LoginModal
              show={loginModalShow}
              onHide={() => setLoginModalShow(false)}
            />
          </>
        )}
      </Container>
    </Navbar>
  );
};

export default MyNavbar;
