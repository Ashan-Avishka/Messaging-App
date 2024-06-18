import React, { useEffect, useState } from 'react';
import './styles/ChatPage.css';  
import MessageList from '../components/MessageList';
import MessageInput from '../components/MessageInput';
import { getMessages, sendMessage, getUsers } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGear, faSearch, faUserCircle } from '@fortawesome/free-solid-svg-icons';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);  
  const [selectedChatId, setSelectedChatId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const userResponse = await getUsers();
        setUsers(userResponse.data);  
      } catch (error) {
        console.error('Error fetching users', error);
        setError('Error fetching users');
      }
    };
    fetchUsers();
  }, []);  

  const fetchMessages = async (chatId) => {
    try {
      var msgList = [];
      const messageResponse = await getMessages(chatId);

      for (let i = 0; i < messageResponse.data.messages.length; i++) {
        
        const sender = messageResponse.data.messages[i];
        const message = messageResponse.data.messages[i];
        const timestamp = messageResponse.data.timestamps[i];
        
        var newMessage = {
          sender: "you",
          text:message,
          timestamp: timestamp 
        };
        msgList.push(newMessage);
      }

      setMessages(msgList);

      
      // setMessages(messageResponse.data);
    } catch (error) {
      console.error('Error fetching messages', error);
      setError('Error fetching messages');
    }
  };

  const handleChatClick = (chatId) => {
    console.log('handleChatClick', chatId);
    setSelectedChatId(chatId);
    fetchMessages(chatId);
  };

  const handleSend = async (text) => {
    const newMessage = {
      sender: "You",
      reciever: selectedChatId,
      text,
      timestamp: new Date().toISOString()  
    };
    setMessages([...messages, newMessage]);  

    try {
      await sendMessage(newMessage);
    } catch (error) {
      console.error('Error sending message', error);
      setError('Failed to send message');
      setMessages(messages); 
    }
  };

  return (
    <div className="container1">
      <div className="sidebar">
        <div className="row sr">
          <div className="col-12">
            <div className="input-group">
              <input className="form-control border-secondary py-1" type="search" placeholder="search chat"/>
              <div className="input-group-append">
                <button className="btn btn-outline-light btn-search" type="button">
                  <FontAwesomeIcon icon={faSearch} />
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <ul className="user-list">
          {users.map(user => (
            <li key={user.id} className="user-item" onClick={() => handleChatClick(user.uid)}>
              <FontAwesomeIcon icon={faUserCircle} className='user-icon' />
              <span className="user-name">{user.username}</span>
            </li>
          ))}
        </ul>
        <div className="row br">
          <div className='d-flex' type="button">
            <FontAwesomeIcon icon={faGear} className='settings-icon' />
            <span>Settings</span>
          </div>
        </div>
      </div>
      <div className="chat-area">
        {error && <div className="error">{error}</div>}
        <MessageList messages={messages} />
        <MessageInput onSend={handleSend} />
      </div>
    </div>
  );
};

export default ChatPage;
