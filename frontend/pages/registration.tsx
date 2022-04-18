import Head from "next/head";
import { NextPage } from "next/types";

import { FocusEvent, useState } from "react";

import Layout from "../components/layout";
import LoginSocial from "../components/loginSocial";
import FormInput from "../components/formInput";
import styles from "../components/registration.module.css";

const Registration: NextPage = () => {
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPswError, setConfirmPswError] = useState("");
  const [password, setPassword] = useState("");

  const handleChangeEmail = (e: FocusEvent<HTMLInputElement>) => {
    const regex =
      /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i;
    const target = e.target;
    const value = target.value;

    if (!value || !regex.test(value)) {
      setEmailError("Insert a valid email!");
    } else {
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
      setPasswordError(
        "Error: Password must contain at least one number, one uppercase or lowercase letter, one special character, and at least 8 and no more than 32."
      );
      return;
    }
    setPasswordError("");
  };

  const handleChangeConfirmPsw = (e: FocusEvent<HTMLInputElement>) => {
    const target = e.target;
    const value = target.value;

    if (value !== password) {
      setConfirmPswError("Error: Passwords must match");
      return;
    }
    setConfirmPswError("");
  };

  return (
    <Layout>
      <Head>
        <title>Sign Up</title>
        <meta name="description" content="Generated by create next app" />
        {/* <link rel="icon" href="/favicon.ico" /> */}
      </Head>

      <div className="container flex flex-wrap mt-5 mx-auto p-5 bg-white max-w-xl ">
        <div className=" w-full items-center mb-4">
          <h2 className="text-2xl">Create account</h2>
        </div>
        <div className=" w-full mb-4 ">
          <form action="/" method="POST">
            <span className="text-sm text-gray-500">
              Your username must be unique and will be visible to other users.
            </span>
            <div>
              <FormInput
                inputType={"text"}
                inputName={"username"}
                inputLabel={"Username"}
                errorMsg={""}
              />
              <FormInput
                inputType={"email"}
                inputName={"email"}
                inputLabel={"Email"}
                errorMsg={emailError}
                changeHandler={handleChangeEmail}
              />
              <FormInput
                inputType={"password"}
                inputName={"password"}
                inputLabel={"Password"}
                errorMsg={passwordError}
                changeHandler={handleChangePassword}
              />
              <FormInput
                inputType={"password"}
                inputName={"confirmPassword"}
                inputLabel={"Confirm Password"}
                errorMsg={confirmPswError}
                changeHandler={handleChangeConfirmPsw}
              />
            </div>
            <div className="text-center">
              <button type={"submit"} className="btn btn_dark">
                Sign up
              </button>
            </div>
          </form>
        </div>
        <LoginSocial />
      </div>
    </Layout>
  );
};

export default Registration;
