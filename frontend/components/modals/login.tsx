import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import {
  Button,
  Container,
  FloatingLabel,
  Form,
  Modal,
  Row,
  Col,
} from "react-bootstrap";
import Image from "next/image";

const LoginModal = ({ ...props }) => {
  return (
    <Modal
      {...props}
      backdrop="static"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      contentClassName="bg-dark text-white"
    >
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ marginLeft: "auto" }}
        >
          Sign in
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form action="/">
          <FloatingLabel label="Email" className="mb-3" controlId="formEmail">
            <Form.Control
              type="email"
              placeholder="Email"
              className="validate bg-dark text-white"
              style={{
                border: 0,
                borderBottom: "1px solid",
                borderRadius: 0,
              }}
            />
          </FloatingLabel>
          <FloatingLabel
            label="Password"
            className="mb-3"
            controlId="formPassword"
          >
            <Form.Control
              type="password"
              placeholder="Password"
              className="validate bg-dark text-white"
              style={{ border: 0, borderBottom: "1px solid", borderRadius: 0 }}
            />
            <Link href="#">
              <a style={{ color: "#adb5bd" }}>Forgot password?</a>
            </Link>
          </FloatingLabel>

          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="Remember me" />
          </Form.Group>
          <Form.Group className="mb-3 text-center" controlId="formLoginButton">
            <Button
              type="submit"
              variant="light"
              className="btn-block "
              style={{ marginLeft: "auto" }}
              onClick={props.onHide}
            >
              Login
            </Button>
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer
        className="justify-content-center"
        // style={{ display: "block" }}
      >
        <Container fluid>
          <Row className="justify-content-md-center">
            <Col className="text-center">
              <p>OR Log in with</p>
            </Col>
          </Row>
          <Row className="justify-content-md-center">
            <Col className="text-center">
              <Link href="/">
                <Button
                  variant="light"
                  style={{
                    borderRadius: "100%",
                    height: "3rem",
                    width: "3rem",
                  }}
                >
                  <FontAwesomeIcon
                    icon={"fa-brands fa-google"}
                    style={{ height: "1.5em" }}
                  />
                </Button>
              </Link>
            </Col>
            <Col className="text-center">
              <Link href="/">
                <Button
                  variant="light"
                  style={{
                    borderRadius: "100%",
                    height: "3rem",
                    width: "3rem",
                  }}
                >
                  <FontAwesomeIcon
                    icon={"fa-brands fa-facebook-f"}
                    style={{ height: "1.5em" }}
                  />
                </Button>
              </Link>
            </Col>
            <Col className="text-center">
              <Link href="/">
                <Button
                  variant="light"
                  style={{
                    borderRadius: "100%",
                    height: "3rem",
                    width: "3rem",
                  }}
                >
                  <FontAwesomeIcon
                    icon={"fa-brands fa-twitter"}
                    style={{ height: "1.5em" }}
                  />
                </Button>
              </Link>
            </Col>
          </Row>
        </Container>
      </Modal.Footer>
    </Modal>
  );
};

export default LoginModal;
