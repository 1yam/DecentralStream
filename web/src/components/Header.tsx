import {Button, Navbar, Spinner, Dropdown} from 'flowbite-react';
import {useState} from "react";
import {GenerateStreamKeyModal} from "./GenerateStreamKeyModal";

interface Props {
  address: string;
  loading: boolean;
  login: () => void;
  logout: () => void;
}

export const Header = ({logout, login, address, loading}: Props) => {
  const [generateStreamKeyModalOpened, setGenerateStreamKeyModalOpened] = useState(false);

  return (
    <>
      <Navbar rounded>
        <Navbar.Brand href="https://flowbite-react.com">
          <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">DecentralStream</span>
        </Navbar.Brand>
        <div className="flex md:order-2">
          {address ? (
            <Dropdown label="My profile">
              <Dropdown.Item>
                <div className={'block text-start'}>
                  <p className={'font-bold'}>Account</p>
                  <p className={'text-xs'}>{address}</p>
                </div>
              </Dropdown.Item>
              <Dropdown.Divider/>
              <Dropdown.Item onClick={() => setGenerateStreamKeyModalOpened(true)}>Generate stream key</Dropdown.Item>
              <Dropdown.Divider/>
              <Dropdown.Item onClick={logout}>Sign out</Dropdown.Item>
            </Dropdown>
          ) : (
            <Button onClick={login}>
              {loading ? <Spinner/> : "Connect Wallet"}
            </Button>
          )}
          <Navbar.Toggle/>
        </div>
      </Navbar>

      {generateStreamKeyModalOpened && (
        <GenerateStreamKeyModal
          opened={generateStreamKeyModalOpened}
          onClose={() => setGenerateStreamKeyModalOpened(false)}
          address={address}
        />
      )}
    </>
  );
}