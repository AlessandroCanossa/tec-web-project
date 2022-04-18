import Head from "next/head";
import Link from "next/link";
import { NextPage } from "next/types";

import { FocusEvent, useState } from "react";

import Layout from "../components/layout";
import LoginSocial from "../components/loginSocial";
import styles from "../components/registration.module.css";

const Registration: NextPage = () => {
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPswError, setConfirmPswError] = useState("");

  const [password, setPassword] = useState("");

  const validateEmail = (e: FocusEvent<HTMLInputElement>) => {
    const regex =
      /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i;
    const target = e.target;
    const value = target.value;

    if (!value || !regex.test(value)) {
      e.target.classList.add("is-invalid");
      setEmailError("Insert a valid email!");
    } else {
      target.classList.remove("is-invalid");
      setEmailError("");
    }
  };

  const handleChangePassword = (e: FocusEvent<HTMLInputElement>) => {
    const target = e.target;
    const regex =
      /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[!@#$%^&(){}[\]:;<>,.?\/~_+\-=|\\]).{8,32}$/i;
    const value = target.value;
    setPassword(value);

    if (!value || !regex.test(value)) {
      target.classList.add("is-invalid");
      setPasswordError(
        "Error: Password must contain at least one number, one uppercase or lowercase letter, one special character, and at least 8 and no more than 32."
      );
      return;
    }
    target.classList.remove("is-invalid");
    setPasswordError("");
  };

  const handleChangeConfirmPsw = (e: FocusEvent<HTMLInputElement>) => {
    const target = e.target;
    const value = target.value;

    if (value !== password) {
      target.classList.add("is-invalid");
      setConfirmPswError("Error: Passwords must match");
      return;
    }
    target.classList.remove("is-invalid");
    setConfirmPswError("");
  };

  return (
    <Layout>
      <Head>
        <title>Sign Up</title>
        <meta name="description" content="Generated by create next app" />
        {/* <link rel="icon" href="/favicon.ico" /> */}
      </Head>

      <div className="container flex flex-wrap mt-5 mx-auto p-5 bg-white ">
        <div className=" w-full items-center mb-4">
          <h2 className="font-header">Create account</h2>
        </div>
        <div className=" w-full mb-4">
          <form action="/">
            <span className="mb-0">
              Your username must be unique and will be visible to other users.
            </span>
          </form>
        </div>
        <hr className="" />
        <LoginSocial />
      </div>
    </Layout>
  );
};

export default Registration;
