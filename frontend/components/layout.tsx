import Head from "next/head";
import MyNavbar from "./navbar";

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
        <link rel="shortcut icon" href="/favicon.ico" />
        <meta
          name="description"
          content="Learn how to build a personal website using Next.js"
        />
      </Head>

      <header>
        <MyNavbar />
      </header>
      <main>{children}</main>
    </>
  );
};

export default Layout;
