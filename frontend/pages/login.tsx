import Head from "next/head";
import Layout from "../components/layout";
import FormInput from "../components/formInput";

const Login = () => {
  return (
    <Layout>
      <Head>
        <title>Log In</title>
      </Head>

      <div className="container flex flex-wrap mt-5 mx-auto p-5 bg-white max-w-xl ">
        <div className=" w-full items-center mb-4">
          <h2 className="text-2xl">Log into your account</h2>
        </div>
        <div className=" w-full mb-4 ">
          <form action="/" method="GET">
            <div>
              <FormInput
                inputType={"text"}
                inputName={"username"}
                inputLabel={"Username"}
                errorMsg={""}
              />
              <FormInput
                inputType={"password"}
                inputName={"password"}
                inputLabel={"Password"}
                errorMsg={""}
                // errorMsg={passwordError}
                // changeHandler={handleChangePassword}
              />
            </div>
            <label>
              <input type="checkbox" name="rememberMe" className="mr-2"/>
              Remember Me
            </label>
            <div className="text-center">
              <button type={"submit"} className="btn btn_dark">
                Log in
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
};

export default Login;
