import Link from "next/link";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";

const MyNavbar = () => {
  return (
    <Navbar bg="dark" variant="dark">
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
            className="me-2 bg-dark"
          />
          <Button type="submit" variant="outline-success" className="me-2">
            Search
          </Button>
        </Form>

        <Link href="/account">
          <Button variant="outline-light">
            <FontAwesomeIcon icon={faUser} className="me-2"></FontAwesomeIcon>
            Username
          </Button>
        </Link>
      </Container>
    </Navbar>
  );
};

export default MyNavbar;