import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebookF,
  faTwitter,
  faGoogle,
} from "@fortawesome/free-brands-svg-icons";

import Link from "next/link";

import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";

import styles from "./login.module.css";

const LoginModal = ({ ...props }) => {
  return (
    <Modal
      {...props}
      aria-labelledby="contained-modal-title-vcenter"
      centered
      contentClassName=""
    >
      <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter" className="mx-auto">
          Sign in
        </Modal.Title>
      </Modal.Header>
      <Modal.Body className="mx-4">
        <Form action="/">
          <FloatingLabel label="Email" className="mb-3" controlId="formEmail">
            <Form.Control
              type="email"
              placeholder="Email"
              className={`validate, ${styles.form}`}
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
              className={`validate, ${styles.form}`}
            />
            <Link href="#">
              <a className={styles.forgot_password}>Forgot password?</a>
            </Link>
          </FloatingLabel>

          <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="Remember me" />
          </Form.Group>
          <Form.Group className="mb-3 text-center" controlId="formLoginButton">
            <Button
              type="submit"
              variant="dark"
              className="btn-block "
              onClick={props.onHide}
            >
              Login
            </Button>
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer className="justify-content-center pb-4">
        <Container fluid>
          <Row className="justify-content-md-center">
            <Col className="text-center">
              <p>OR Log in with</p>
            </Col>
          </Row>
          <Row className="justify-content-md-center">
            <Col className="text-center">
              <Link href="/" passHref>
                <Button variant="dark" className={styles.icon_btn}>
                  <FontAwesomeIcon icon={faGoogle} className={styles.icon} />
                </Button>
              </Link>
            </Col>
            <Col className="text-center">
              <Link href="/" passHref>
                <Button variant="dark" className={styles.icon_btn}>
                  <FontAwesomeIcon icon={faFacebookF} className={styles.icon} />
                </Button>
              </Link>
            </Col>
            <Col className="text-center">
              <Link href="/" passHref>
                <Button variant="dark" className={styles.icon_btn}>
                  <FontAwesomeIcon icon={faTwitter} className={styles.icon} />
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
