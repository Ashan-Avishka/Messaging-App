import React from 'react';
import './PrimaryBtn.css'; 

const Button = ({ text, onClick, type = '', className = '' }) => {
    return (
      <button className={className} type={type} onClick={onClick}>
        {text}
      </button>
    );
  };
  
  export default Button;