import React, { useEffect, useState } from 'react';
import MessageList from '../components/MessageList';
import MessageInput from '../components/MessageInput';
import { getMessages, sendMessage } from '../services/api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await getMessages();
        setMessages(response.data);
      } catch (error) {
        console.error('Error fetching messages', error);
      }
    };
    fetchMessages();
  }, []);

  const handleSend = async (text) => {
    const newMessage = { sender: 'User', text };
    try {
      await sendMessage(newMessage);
      setMessages([...messages, newMessage]);
    } catch (error) {
      console.error('Error sending message', error);
    }
  };

  return (
    <div>
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} />
    </div>
  );
};

export default ChatPage;
