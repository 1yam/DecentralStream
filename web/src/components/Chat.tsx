import {useAccountState} from "../stores/account";
import {useEffect, useState} from "react";
import {Alert, Button, Sidebar} from "flowbite-react";
import axios from "axios";

interface Props {
  streamer: string
}

const chatApi = axios.create({
  baseURL: process.env.REACT_APP_CHAT_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const Chat = ({ streamer }: Props) => {
  const accountState = useAccountState()
  const [messages, setMessages] = useState<any>([]);
  const [newMessage, setNewMessage] = useState<any>('');

  const fetchMessages = async () => {
    try {
      const response = await chatApi.get(`${process.env.REACT_APP_CHAT_URL}/get_messages/${streamer}`)
      setMessages(response.data)
    } catch (error) {
      setMessages([])
    }
  }

  const sendMessage = async () => {
    try {
      await chatApi.post(`${process.env.REACT_APP_CHAT_URL}/post_message`, {
        channel: streamer,
        message: newMessage,
        username: accountState.getAddress()
      })
      setNewMessage('')
      fetchMessages()
    } catch (error) {
      console.log(error)
    }
  }

  useEffect(() => {
    setInterval(() => {
      fetchMessages()
    }, 5000)
  }, [])

  return (
    <div className="max-w-md mx-auto p-4">
      <Sidebar className={'w-full'}>
        <Sidebar.ItemGroup>
          <h1 className={'text-lg text-center font-medium'}>Chat</h1>
        </Sidebar.ItemGroup>
        <Sidebar.ItemGroup>
          <div className={'overflow-y-auto max-h-96'} ref={(el) => el && el.scrollTo(0, el.scrollHeight)}>
            {messages.map((message: any, idx: number) => (
                <div className="block text-start break-all text-wrap py-2">
                  <div className="text-sm font-medium">{message.username}</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">{message.message}</div>
                </div>
            ))}
          </div>
        </Sidebar.ItemGroup>
        <Sidebar.CTA>
          <div className="mb-3 flex items-center gap-1">
            {accountState.getAddress() ? (
              <>
                <input type="text"
                       value={newMessage}
                       onChange={(e) => setNewMessage(e.target.value)}
                       className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                       placeholder="Your message"/>
                <Button onClick={sendMessage} disabled={!newMessage}>Send</Button>
              </>
            ) : (
              <Alert color={'warning'}>Please connect your wallet to send messages</Alert>
            )}
          </div>
        </Sidebar.CTA>
      </Sidebar>
    </div>
  );


}