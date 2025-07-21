import React, { useState } from 'react'
import axios from 'axios';
import { NavLink, redirect } from 'react-router-dom';
import "../assets/LogIn.css"

const LogIn = (props) => {
    const [accno, setaccno] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleClick = async () => {
        const data = {
            account_no: accno,
            pin: password
        };
        try {
            const response = await axios.post('http://localhost:5000/login', data);
            const result = response.data;
            setMessage(result);
            props.onLogin();
            redirect('/');
        } catch (error) {
            setMessage(error.response.data);
        }
    }
    return (
        <div className="login-page">
      <div className="login-box">
        <h1 className="app-title">Bank</h1>
        <h2 className="login-title">Login</h2>

        <label>Account Number</label>
        <input className="input-login" type="text" placeholder="Enter account number" value={accno} onChange={(e) => setaccno(e.target.value)} />

        <label>PIN</label>
        <input className="input-login" type="password" placeholder="Enter PIN" value={password} onChange={(e) => setPassword(e.target.value)} />

        <NavLink className="login-btn" onClick={handleClick} to={"/"}>Log in</NavLink>
        <p>{message}</p>
      </div>
      <div className="sample-users">
        <h1>Sample Users</h1>
        <p>Account No: 506-932, PIN: 1111</p>
        <p>Account No: 131-323, PIN: 1234</p>
        <p>Account No: 305-900, PIN: 1122</p>
        <p>Account No: 633-374, PIN: 2222</p>
      </div>
    </div>
    )
}

export default LogIn