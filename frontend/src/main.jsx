import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Login from './pages/Login'
import Inbox from './pages/Inbox'
import Chat from './pages/Chat'

function App(){
  return (
    <BrowserRouter>
      <nav style={{padding:10, borderBottom:'1px solid #ccc'}}>
        <Link to='/' style={{marginRight:10}}>Inbox</Link>
        <Link to='/bot'>Bot Chat</Link>
      </nav>
      <Routes>
        <Route path='/' element={<Inbox/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/chat/:email' element={<Chat/>}/>
        <Route path='/bot' element={<Chat bot={true}/>}/>
      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App/>)
