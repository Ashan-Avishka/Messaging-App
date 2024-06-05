import React from 'react';

const MessageItem = ({ message }) => (
  <div>
    <strong>{message.sender}</strong>: {message.text}
  </div>
);

export default MessageItem;
