import React, { useState } from 'react';
import PrimaryBtn from '../components/PrimaryBtn';

const MessageInput = ({ onSend }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSend(text);
      setText('');
    }
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <input
        className="input"
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your message..."
      />
      <PrimaryBtn text={'Send'} className="primary-btn" type="submit"></PrimaryBtn>
    </form>
  );
};

export default MessageInput;
