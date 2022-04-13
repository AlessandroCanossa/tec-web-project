import Head from "next/head";
import MyNavbar from "./navbar";
import React from "react";

const Layout = ({
  children,
  home,
}: {
  children: React.ReactNode;
  home?: boolean;
}) => {
  return (
    <>
      <Head>
        {/*<link rel="shortcut icon" href="/favicon.ico" />*/}
        <meta
          name="description"
          content="Learn how to build a personal website using Next.js"
        />
        <title></title>
      </Head>

      <header>
        <MyNavbar />
      </header>
      <main>{children}</main>
      <footer></footer>
    </>
  );
};

export default Layout;
