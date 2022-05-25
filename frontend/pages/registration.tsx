import Head from "next/head";
import { NextPage } from "next/types";

import Layout from "../components/layout";
import styles from "../components/registration.module.css";

import * as Yup from "yup";
import { Formik } from "formik";
import { Button, Form } from "react-bootstrap";

const schema = Yup.object().shape({
  email: Yup.string()
    .email("Enter a valid email")
    .required("Enter a valid email")
    .min(5)
    .max(255),
  username: Yup.string().required().min(3).max(255),
  first_name: Yup.string().required().min(3).max(255),
  last_name: Yup.string().required().min(3).max(255),
  password: Yup.string().required().min(5).max(255),
});

const Registration: NextPage = () => {
  return (
    <Layout>
      <Head>
        <title>Register</title>
      </Head>

      <section className={`${styles.form_signin} w-100 m-auto`}>
        <Formik
          validationSchema={schema}
          initialValues={{
            email: "",
            username: "",
            first_name: "",
            last_name: "",
            password: "",
          }}
          onSubmit={(values, actions) => {
            console.log({ values, actions });
            alert(JSON.stringify(values, null, 2));
            actions.setSubmitting(false);
          }}
        >
          {({ handleSubmit, handleChange, values, errors }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <h1 className="h3 mb-3 fw-normal">Sign on</h1>

              <Form.Group
                className="mb-3 position-relative"
                controlId="validation_email"
              >
                <Form.FloatingLabel label="Email address" className="mb-3">
                  <Form.Control
                    type="email"
                    name="email"
                    placeholder="name@example.com"
                    isInvalid={!!errors.email}
                    // isValid={touched.email && !errors.email}
                    value={values.email}
                    onChange={handleChange}
                  />
                  <Form.Control.Feedback type="invalid" tooltip>
                    {errors.email}
                  </Form.Control.Feedback>
                </Form.FloatingLabel>
              </Form.Group>
              <Form.Group
                className="mb-3 position-relative"
                controlId="validation_username"
              >
                <Form.FloatingLabel label="Username" className="mb-3">
                  <Form.Control
                    type="text"
                    name="username"
                    placeholder="username"
                    isInvalid={!!errors.username}
                    // isValid={touched.email && !errors.email}
                    value={values.username}
                    onChange={handleChange}
                  />
                  <Form.Control.Feedback type="invalid" tooltip>
                    {errors.username}
                  </Form.Control.Feedback>
                </Form.FloatingLabel>
              </Form.Group>
              <Form.Group
                className="mb-3 position-relative"
                controlId="validation_first_name"
              >
                <Form.FloatingLabel label="First Name" className="mb-3">
                  <Form.Control
                    type="text"
                    name="first_name"
                    placeholder="First name"
                    isInvalid={!!errors.first_name}
                    // isValid={touched.email && !errors.email}
                    value={values.first_name}
                    onChange={handleChange}
                  />
                  <Form.Control.Feedback type="invalid" tooltip>
                    {errors.first_name}
                  </Form.Control.Feedback>
                </Form.FloatingLabel>
              </Form.Group>
              <Form.Group
                className="mb-3 position-relative"
                controlId="validation_last_name"
              >
                <Form.FloatingLabel label="Last Name" className="mb-3">
                  <Form.Control
                    type="text"
                    name="last_name"
                    placeholder="Last name"
                    isInvalid={!!errors.last_name}
                    // isValid={touched.email && !errors.email}
                    value={values.last_name}
                    onChange={handleChange}
                  />
                  <Form.Control.Feedback type="invalid" tooltip>
                    {errors.last_name}
                  </Form.Control.Feedback>
                </Form.FloatingLabel>
              </Form.Group>
              <Form.Group
                className="mb-3 position-relative"
                controlId="validation_password"
              >
                <Form.FloatingLabel label="Password">
                  <Form.Control
                    type="password"
                    name="password"
                    placeholder="Password"
                    isInvalid={!!errors.password}
                    // isValid={touched.password && !errors.password}
                    value={values.password}
                    onChange={handleChange}
                  />
                  <Form.Control.Feedback type="invalid" tooltip>
                    {errors.password}
                  </Form.Control.Feedback>
                </Form.FloatingLabel>
              </Form.Group>

              <Button
                className="ms-0 w-100"
                size="lg"
                variant="dark"
                type="submit"
              >
                Sign in
              </Button>
            </Form>
          )}
        </Formik>
      </section>
    </Layout>
  );
};

export default Registration;
