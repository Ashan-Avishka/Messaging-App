import React from 'react';
import { formatTimestamp } from '../utils/utils';
import './MessageItem.css'; 

const MessageItem = ({ message}) => (
  <div className={`message-container ${message.msgType}`}>
    <div className="message-header">
      <div className="sender-name">{message.sender}</div>
    </div>
    <div className="message-text">{message.text}</div>
    <div className="timestamp">{formatTimestamp(message.timestamp)}</div>
  </div>
);


export default MessageItem;


