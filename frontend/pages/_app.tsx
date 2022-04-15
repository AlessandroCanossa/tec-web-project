import "../styles/globals.css";
import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";

config.autoAddCss = false;
import type { AppProps } from "next/app";
import Head from "next/head";
import Script from "next/script";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title></title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
