import React, {useState} from 'react'
export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  async function register(){
    const res = await fetch('http://localhost:8000/api/auth/register', {
      method:'POST', headers:{'content-type':'application/json'},
      body: JSON.stringify({email,password})
    })
    if(res.ok) setMsg('Registered. Now login.')
    else setMsg('Register failed')
  }
  async function login(){
    const form = new FormData()
    form.append('email', email)
    form.append('password', password)
    const res = await fetch('http://localhost:8000/api/auth/token', {method:'POST', body: form})
    const j = await res.json()
    if(j.access_token){
      localStorage.setItem('token', j.access_token)
      localStorage.setItem('me', email)
      window.location.href = '/'
    } else {
      setMsg('Login failed')
    }
  }
  return (<div style={{padding:20}}>
    <h2>Login / Register</h2>
    <input aria-label='email' placeholder='email' value={email} onChange={e=>setEmail(e.target.value)}/><br/>
    <input aria-label='password' placeholder='password' type='password' value={password} onChange={e=>setPassword(e.target.value)}/><br/>
    <button onClick={login}>Login</button>
    <button onClick={register} style={{marginLeft:8}}>Register</button>
    <div role='status'>{msg}</div>
  </div>)
}
