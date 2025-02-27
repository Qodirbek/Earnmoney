import Head from "next/head";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Earnmoney</title>
      </Head>
      <h1>Welcome to Earnmoney</h1>
      <p>Click the button below to pay with crypto:</p>
      <a href="https://nowpayments.io/payment/?iid=5731964294" target="_blank" rel="noreferrer noopener">
        <img src="https://nowpayments.io/images/embeds/payment-button-white.svg" 
             alt="Cryptocurrency & Bitcoin payment button by NOWPayments"
             style={{ width: "200px", cursor: "pointer" }}/>
      </a>
    </div>
  );
}