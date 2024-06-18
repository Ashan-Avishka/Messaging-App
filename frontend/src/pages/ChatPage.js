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

  const fetchMessages = async (chatId, username) => {
    try {
      var msgList = [];
      var sender = '';
      var message = '';
      var msgType = '';
      var timestamp = '';
      const messageResponse = await getMessages(chatId);

      if(messageResponse.data.message == "No message found for this user"){
        console.error('No message found for this user');
      }
      else if(messageResponse.data.message == "Private key not found"){
        console.error('Private key not found');
      }
      else{

        for (let i = 0; i < messageResponse.data.messages.length; i++) {

          if(messageResponse.data.msg_types[i] == 'sent') {
            sender = 'You';
            message = messageResponse.data.messages[i];
            msgType = messageResponse.data.msg_types[i];
            timestamp = messageResponse.data.timestamps[i];
            console.log(msgType);
          }
          else if(messageResponse.data.msg_types[i] == 'received') {
            sender = username;
            message = messageResponse.data.messages[i];
            msgType = messageResponse.data.msg_types[i];
            timestamp = messageResponse.data.timestamps[i];
            console.log(msgType);
          }
  
          var newMessage = {
            sender: sender,
            text:message,
            msgType:msgType,
            timestamp: timestamp 
          };
          msgList.push(newMessage);
        }
        setMessages(msgList);

      }

    } catch (error) {
      console.error('Error fetching messages', error);
      setError('Error fetching messages');
    }
  };

  const handleChatClick = (chatId, username) => {
    console.log('handleChatClick', username);
    setSelectedChatId(chatId);
    fetchMessages(chatId, username);
  };

  const handleSend = async (text) => {
    const newMessage = {
      sender: "You",
      reciever: selectedChatId,
      text,
      msgType:'sent',
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
            <li key={user.id} className="user-item" onClick={() => handleChatClick(user.uid, user.username)}>
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
