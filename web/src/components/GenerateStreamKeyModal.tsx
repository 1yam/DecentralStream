import {Button, Modal, Alert, Spinner} from 'flowbite-react';
import axios from "axios";
import {useState} from "react";

interface Props {
  opened: boolean;
  onClose: () => void;
  address: string;
}

export const GenerateStreamKeyModal = ({opened, onClose, address}: Props) => {
  const [streamKeyLoading, setStreamKeyLoading] = useState(false);
  const [streamKey, setStreamKey] = useState("");

  const generateStreamKey = async () => {
    setStreamKeyLoading(true);

    try {
      const response = await axios.post(`/accounts/${address}/generate-stream-key`);
      setStreamKey(response.data);
    } catch (error) {
      console.log(error);
    }

    setStreamKeyLoading(false);
  }

  return (
    <>
      <Modal show={opened} onClose={onClose}>
        <Modal.Header>Generate stream key</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
              Your stream key is a unique key that allows you to stream to your account. Do not share it with anyone.
            </p>
            <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
              If you think your stream key has been compromised or you loose it, you can regenerate it.
            </p>
            <Button onClick={generateStreamKey}>
              {streamKeyLoading ? <Spinner/> : "Generate stream key"}
            </Button>
            {streamKey && (
              <Alert color="gray">
                <div className={'block text-start'}>
                  <p> Your stream key:</p>
                  <p className={'font-bold break-all'}>{streamKey}</p>
                </div>
              </Alert>
            )}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <div className={'flex justify-end w-full'}>
            <Button color={'gray'} onClick={onClose}>Close</Button>
          </div>
        </Modal.Footer>
      </Modal>
    </>
  );
}