import { useEffect, useState } from "react";
import Head from "next/head";

export default function Home() {
  const [balance, setBalance] = useState(null);
  const backendUrl = "https://earnmoney-l1tz.onrender.com"; // Backend URL

  useEffect(() => {
    // Foydalanuvchi balansini backenddan olish
    fetch(`${backendUrl}/balance`)
      .then((res) => res.json())
      .then((data) => setBalance(data.balance))
      .catch((err) => console.error("Error fetching balance:", err));
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <Head>
        <title>Earnmoney</title>
      </Head>
      <h1>Welcome to Earnmoney</h1>
      <p>Your Balance: {balance !== null ? balance + " USD" : "Loading..."}</p>
      
      <h3>Click the button below to pay with crypto:</h3>
      <a href="https://nowpayments.io/payment/?iid=5731964294" target="_blank" rel="noreferrer noopener">
        <img 
          src="https://nowpayments.io/images/embeds/payment-button-white.svg" 
          alt="Cryptocurrency & Bitcoin payment button by NOWPayments"
          style={{ width: "200px", cursor: "pointer" }}
        />
      </a>
    </div>
  );
}