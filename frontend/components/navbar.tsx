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
    <Navbar className={""} variant="dark" bg="dark">
      <Container fluid style={{ margin: " 0 10rem", padding: "0" }}>
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
          <section className={"d-inline-flex"} style={{ flexFlow: "row" }}>
            <Form className="d-flex mx-2">
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
                  <Button variant={"light"} className={"mx-2"}>
                    Log in
                  </Button>
                </Link>
                <Link href={"/registration"} passHref>
                  <Button variant={"outline-light"} className={"mx-2"}>
                    Sign up
                  </Button>
                </Link>
              </>
            )}
          </section>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default MyNavbar;
