import { Routes, Route } from 'react-router-dom'
import './App.css'
import LogIn from './components/LogIn'
import About from './components/About'
import Home from './components/Home'
import Navbar from './components/Navbar.jsx'
import { useState } from 'react'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <>
      <Routes>
        <Route path="/" element={isAuthenticated ? <><Navbar onLogOut={() => setIsAuthenticated(false)} /><Home /></> : <LogIn onLogin={() => setIsAuthenticated(true)} />} />
        <Route path="/about" element={isAuthenticated ? <><Navbar onLogOut={() => setIsAuthenticated(false)} /><About /></> : <LogIn onLogin={() => setIsAuthenticated(true)} />} />
        <Route path="/login" element={<LogIn onLogin={() => setIsAuthenticated(true)} />} />
      </Routes>
    </>
  )
}

export default App;
