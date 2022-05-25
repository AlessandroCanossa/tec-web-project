import {
  Navbar,
  Nav,
  Container,
  Form,
  FormControl,
  Button,
} from "react-bootstrap";
import Link from "next/link";
import { useState } from "react";
import UserMenu from "./userMenu";

const MyNavbar = () => {
  const [logged, setLoggedState] = useState(true);

  return (
    <Navbar className="navbar-expand-lg" variant="dark" bg="dark">
      <Container>
        <Link href="/" passHref>
          <Navbar.Brand>Home</Navbar.Brand>
        </Link>
        <Navbar.Collapse
          className="me-auto my-2 my-lg-0"
          style={{ maxHeight: "100px" }}
        >
          <Nav className="me-auto my-2 my-lg-0">
            <Nav.Item className="">
              <Link href="/series" passHref>
                <Nav.Link>Genres</Nav.Link>
              </Link>
            </Nav.Item>
            <Nav.Item className="">
              <Link href="/series" passHref>
                <Nav.Link>Popular</Nav.Link>
              </Link>
            </Nav.Item>
          </Nav>
          <Form className="d-flex">
            <FormControl
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
            />
            <Button variant="outline-light">Search</Button>
          </Form>

          {logged ? (
            <UserMenu setLoggedState={setLoggedState} />
          ) : (
            <>
              <Link href={"/login"} passHref>
                <Button variant={"light"}>Log in</Button>
              </Link>
              <Link href={"/registration"} passHref>
                <Button variant={"outline-light"}>Sign up</Button>
              </Link>
            </>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default MyNavbar;
