import React from 'react';
import { formatTimestamp } from '../utils/utils';
import './MessageItem.css'; 

const MessageItem = ({ message, isSender }) => (
  <div className={`message-container ${isSender ? 'sender' : 'receiver'}`}>
    <div className="message-header">
      <div className="sender-name">{message.sender}</div>
    </div>
    <div className="message-text">{message.text}</div>
    <div className="timestamp">{formatTimestamp(message.timestamp)}</div>
  </div>
);


export default MessageItem;


