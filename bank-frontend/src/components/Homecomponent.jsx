import React, { useState, useEffect } from 'react'
import '../assets/HomeComponent.css'
import axios from 'axios';

const Homecomponent = (props) => {
    const [transferAmount, setTransferAmount] = useState('');
    const [transferTo, setTransferTo] = useState('');
    const [transferPin, setTransferPin] = useState('');
    const [loanAmount, setLoanAmount] = useState('');
    const [loanPin, setLoanPin] = useState('');
    const [payAmount, setPayAmount] = useState('');
    const [payPin, setPayPin] = useState('');
    const [loanDetails, setLoanDetails] = useState(null);
    const [toggle, setToggle] = useState(false);

    useEffect(() => {
        async function fetchdata() {
      try {
        const response = await axios.get('http://localhost:5000/loan');
        if (response.data.loans == "[]") {
          setLoanDetails(null);
        } else {
            setLoanDetails(JSON.parse(response.data.loans[0]));
        }
      } catch (error) {
        console.error('Error fetching loan details:', error);
      }
    }
        fetchdata();
    }, [toggle])
    

    const handleTransfer = async () => {
        try {
            const data = {
                amount: parseFloat(transferAmount),
                second_acc: transferTo,
                pin: transferPin
            };
            const response = await axios.post('http://localhost:5000/transfer', data);
            props.toggle();
            props.toastapr('Transfer Successful', 'success');
            setTransferAmount('');
            setTransferTo('');
            setTransferPin('');
        } catch (error) {
            console.error('Error occurred during transfer:', error);
            props.toastapr(error.response ? error.response.data : 'Transfer failed', 'error');
        }
    };

    const handleLoan = async () => {
        try {
            const data = {
                amount: parseFloat(loanAmount),
                pin: loanPin
            };
            const response = await axios.post('http://localhost:5000/loan', data);
            props.toggle();
            props.toastapr(response.data.message, 'success');
            setLoanAmount('');
            setLoanPin('');
            setToggle(!toggle);
        } catch (error) {
            console.error('Error occurred during loan application:', error);
            props.toastapr(error.response ? error.response.data.message : 'Loan application failed', 'error');
        }
    };

    const handlePayLoan = async () => {
        try {
            const data = {
                amount: parseFloat(payAmount),
                pin: payPin
            };
            const response = await axios.post('http://localhost:5000/pay_loan', data);
            props.toggle();
            props.toastapr(response.data.message, 'success');
            setPayAmount('');
            setPayPin('');
            setToggle(!toggle);
        } catch (error) {
            console.error('Error occurred during loan payment:', error);
            props.toastapr(error.response ? error.response.data.message : 'Loan payment failed', 'error');
        }
    };

  return (
    <div className='second-container'>
        <div className='side-box first-box'>
            <h3>Transfer</h3>
            <input className='side-input' type="text" placeholder='Transfer To' id='transfer-to' value={transferTo} onChange={(e) => setTransferTo(e.target.value)} />
            <input className='side-input' type="number" placeholder='Amount' id='transfer-amount' value={transferAmount} onChange={(e) => setTransferAmount(e.target.value)} />
            <input className='side-input' type="password" placeholder='PIN' id='transfer-pin' value={transferPin} onChange={(e) => setTransferPin(e.target.value)} />
            <button className='side-button' onClick={handleTransfer}>Transfer Now</button>
        </div>
        <div className='second-box'>
            <div className='side-box sub-box'>
                <h3>Take Loan</h3>
                <input className='side-input' type="text" placeholder='Loan Amount' id='loan-amount' value={loanAmount} onChange={(e) => setLoanAmount(e.target.value)} />
                <input className='side-input' type="password" placeholder='PIN' id='loan-pin' value={loanPin} onChange={(e) => setLoanPin(e.target.value)} />
                <button className='side-button' onClick={handleLoan}>Apply for Loan</button>
            </div>
            <div className='side-box sub-box detail-box'>
                {loanDetails ? (
                    <>
                        <h3>Your Loan</h3>
                        <p>Loan Amount: ${loanDetails.Amount}</p>
                        {/* <p></p> */}
                        <p>Last Updated: {loanDetails.Time}</p>
                    </>
                ) : <p>No Loan Details Available</p>}
            </div>
            <div className='side-box sub-box'>
                <h3>Pay Loan</h3>
                <input className='side-input' type="text" placeholder='Pay Amount' id='pay-amount' value={payAmount} onChange={(e) => setPayAmount(e.target.value)}/>
                <input className='side-input' type="password" placeholder='PIN' id='pay-pin' value={payPin} onChange={(e) => setPayPin(e.target.value)}/>
                <button className='side-button' onClick={handlePayLoan}>Pay Loan</button>
            </div>
        </div>
    </div>
  )
}

export default Homecomponent