import React from 'react';
import MessageItem from './MessageItem';
import './MessageItem.css'; // Ensure the CSS file is imported

const MessageList = ({ messages }) => {
  return (
    <div className="message-list-container">
      {messages.map((message, index) => (
        <MessageItem
          key={index}
          message={message}
        />
      ))}
    </div>
  );
};

export default MessageList;