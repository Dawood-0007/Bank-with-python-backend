import React from 'react'
import '../assets/Navbar.css'
import { NavLink} from 'react-router-dom'
import axios from 'axios'

const Navbar = () => {
  const handleClick = async () => {
    await axios.get('http://localhost:5000/logout');
  }
  return (
    <nav className='navbar'>
        <h1>Bank</h1>
        <ul className='nav-ul'>
            <li><NavLink to="/">Home</NavLink></li>
            <li><NavLink to="/about">About</NavLink></li>
            <li><NavLink className='logout-button' onClick={handleClick} to={"/login"}>Logout</NavLink></li>
        </ul>
    </nav>
  )
}

export default Navbar