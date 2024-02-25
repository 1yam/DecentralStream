export const ConnectWallet = ({
  logout,
  login,
  loading,
  address,
}: any) => {
  return (
    <div>
      {address && !loading ? (
        <button onClick={logout}>
          Disconnect
        </button>
      ) : loading ? (
        <button
          disabled
        >
          <div>Loading...</div>
        </button>
      ) : (
        <button onClick={login}>
          Connect Wallet
        </button>
      )}
    </div>
  );
}