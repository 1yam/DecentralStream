import React, {useState} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from "./pages/Home";
import {Header} from "./components/Header";
import Web3 from "web3";
import {useAccountState} from "./stores/account";

function App() {
  const Layout = ({children}: { children: React.ReactNode }) => {
    const accountState = useAccountState();
    const [authLoading, setAuthLoading] = useState(false);
    const [address, setAddress] = useState("");

    const login = async () => {
      setAuthLoading(true);

      try {
        if (window?.ethereum?.isMetaMask) {
          // Desktop browser
          const accounts = await window.ethereum.request({
            method: "eth_requestAccounts",
          });

          const account = Web3.utils.toChecksumAddress(accounts[0]);
          setAddress(account);
          accountState.setAddress(account);
        }
      } catch (error) {
        console.log(error);
      }

      setAuthLoading(false);
    };

    const logout = () => {
      setAddress("");
      accountState.setAddress("");
    }

    return (
      <div className="flex flex-col h-screen">
        <Header login={login} logout={logout} loading={authLoading} address={address}/>
        <main className="flex-1">
          {children}
        </main>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <Layout>
            <Home/>
          </Layout>
        }/>
      </Routes>
    </Router>
  );
}

export default App;
