import Head from "next/head";
import Layout from "../components/layout";

import { Formik } from "formik";
import * as Yup from "yup";
import styles from "../components/registration.module.css";

import { Form, Button } from "react-bootstrap";

const schema = Yup.object().shape({
  email: Yup.string().email().required(),
  password: Yup.string().required(),
  remember_me: Yup.bool(),
});

const Login = () => {
  return (
    <Layout>
      <Head>
        <title>Log In</title>
      </Head>

      <section className={`${styles.form_signin} w-100 m-auto`}>
        <Formik
          validationSchema={schema}
          initialValues={{
            email: "",
            password: "",
            remember_me: false,
          }}
          onSubmit={(values, actions) => {
            console.log({ values, actions });
            alert(JSON.stringify(values, null, 2));
            actions.setSubmitting(false);
          }}
        >
          {({
            handleSubmit,
            handleChange,
            values,
            errors,
          }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

              <Form.Group
                className="mb-3 position-relative"
                controlId="validationFormik01"
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
                controlId="validationFormik02"
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

              <Form.Group className="mb-3" controlId="formCheckbox">
                <Form.Check
                  type="checkbox"
                  label="Remember me"
                  name="remember_me"
                  onChange={handleChange}
                />
              </Form.Group>
              <Button className="ml-0 w-100" size="lg" variant="dark" type="submit">
                Sign in
              </Button>
            </Form>
          )}
        </Formik>
      </section>
    </Layout>
  );
};

export default Login;
