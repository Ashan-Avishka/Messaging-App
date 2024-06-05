import React from 'react';
import MessageItem from './MessageItem';

const MessageList = ({ messages }) => (
  <div>
    {messages.map((message, index) => (
      <MessageItem key={index} message={message} />
    ))}
  </div>
);

export default MessageList;
