import React, { useState, useEffect } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import '../assets/Home.css'
import axios from 'axios';
import Homecomponent from './Homecomponent';

const Home = () => {
  const [deposit, setDeposit] = useState('');
  const [withdraw, setWithdraw] = useState('');
  const [pin1, setPin1] = useState('');
  const [pin2, setPin2] = useState('');
  const [accountNo, setAccountNo] = useState(''); 
  const [currentBalance, setCurrentBalance] = useState('');
  const [toggle, setToggle] = useState(false);
  const [transactions, setTransactions] = useState([]);
  const [totalTransactions, setTotalTransactions] = useState(0);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get('http://localhost:5000/check_balance');
        console.log(response.data);
        const { account_no, balance } = response.data;
        setAccountNo(account_no);
        setCurrentBalance(balance);
        const transactionsResponse = await axios.get('http://localhost:5000/transactions');
        let { transactions, total_transactions } = transactionsResponse.data;
        console.log(transactions);
        console.log(typeof transactions);
        console.log();
        console.log(total_transactions);
        if (transactions == "[]") {
          transactions = [];
        } else {
          console.log(transactions[0]);
          console.log(typeof transactions[0]);
          transactions = transactions.reverse();
          transactions = transactions.map(transaction => (
            transaction = JSON.parse(transaction)
          ));
          console.log(transactions);
        }
        setTransactions(transactions);
        setTotalTransactions(total_transactions);
      } catch (error) {
        console.error('Error fetching account details:', error);
      }
    }
    fetchData();
  }, [toggle])

  const handleTransaction = async (type) => {
    const data = {
      amount: type === 'deposit' ? parseFloat(deposit) : parseFloat(withdraw),
      pin: type === 'deposit' ? pin1 : pin2
    };
    try {
      const response = await axios.post(`http://localhost:5000/${type}`, data);
      ChangeToggle();
      if (type === 'deposit') {
        setDeposit('');
        setPin1('');
      }
      if (type === 'withdraw') {
        setWithdraw('');
        setPin2('');
      }
      ToastMeassage(`${type.charAt(0).toUpperCase() + type.slice(1)} Successful`, 'success');
    } catch (error) {
      console.error(`Error occurred during ${type}:`, error);
      ToastMeassage(error.response ? error.response.data : `${type.charAt(0).toUpperCase() + type.slice(1)} failed`, 'error');
    }
  };

  const ChangeToggle = () => {
    setToggle(!toggle);
  };

  const ToastMeassage = (message, type) => {
    if (type === 'success') {
      toast.success(message, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    } else if (type === 'error') {
      toast.error(message, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    }
  }

  return (
    <>
      <div className='main-container'>
        <div className='main-box'>
          <div className='main-div'>
            <h2>Account No: {accountNo}</h2>
            <h2>Current Balance: {currentBalance}</h2>
          </div>
          <hr className='divider'/>
          <div>
            <h3>Your Transactions - {totalTransactions} Total</h3>
            <div className='transaction-box'>
              {transactions.length > 0 ? (
                transactions.map((transaction, index) => (
                  <div key={index} className='transaction-item'>
                    <p>{transaction.Method} {transaction.Reciever ? `to ${transaction.Reciever}` : ''} - ${transaction.Amount}</p>
                    <p>Date: {new Date(transaction.Time).toLocaleString()}</p>
                    <hr />
                  </div>
                ))
              ) : (
                <p>No transactions found.</p>
              )}
          </div>
          </div>
        </div>
        <div className='side-box side-box1'>
          <h3>Deposit</h3>
          <input className='side-input' type="number" id='deposit' name='deposit' placeholder='Amount' value={deposit} onChange={(e) => setDeposit(e.target.value)} />
          <input className='side-input' type="password" id='pin1' name='pin1' placeholder='Pin' value={pin1} onChange={(e) => setPin1(e.target.value)} />
          <button className='side-button' onClick={() => handleTransaction('deposit')}>Deposit</button>
        </div>
        <div className='side-box side-box2'>
          <h3>Withdraw</h3>
          <input className='side-input' type="number" id='withdraw' name='withdraw' placeholder='Amount' value={withdraw} onChange={(e) => setWithdraw(e.target.value)} />
          <input className='side-input' type="password" id='pin2' name='pin2' placeholder='Pin' value={pin2} onChange={(e) => setPin2(e.target.value)} />
          <button className='side-button' onClick={() => handleTransaction('withdraw')}>Withdraw</button>
        </div>
      </div>
      {/* <div className='side-box side-box3'></div> */}
      <Homecomponent toggle={ChangeToggle} toastapr={ToastMeassage} />
      <ToastContainer />
    </>
  )
}

export default Home