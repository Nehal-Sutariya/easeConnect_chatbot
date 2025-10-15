import React, {useEffect, useState, useRef} from 'react'
import {useParams} from 'react-router-dom'
export default function Chat({bot=false}){
  const params = useParams()
  const me = localStorage.getItem('me')
  const other = bot ? 'bot@whasease.local' : (params.email || '')
  const [ws, setWs] = useState(null)
  const [messages, setMessages] = useState([])
  const inputRef = useRef()
  useEffect(()=>{
    if(!me) { window.location.href='/login'; return }
    const w = new WebSocket('ws://localhost:8000/api/ws/ws/'+me)
    w.onopen = ()=> console.log('ws open')
    w.onmessage = (evt)=> {
      const data = JSON.parse(evt.data)
      if(data.type==='message'){
        setMessages(m=>[...m, data.message])
      }
    }
    setWs(w)
    return ()=> w.close()
  },[me])
  async function send(){
    const text = inputRef.current.value.trim()
    if(!text) return
    const msg = {
      message_id: Date.now().toString(),
      sender: me,
      recipient: other,
      content: text,
      timestamp: new Date().toISOString(),
      status: 'Sent',
      is_bot_response: false
    }
    // persist via API
    const token = localStorage.getItem('token')
    await fetch('http://localhost:8000/api/messages/', {method:'POST', headers:{'content-type':'application/json','authorization':'Bearer '+token}, body: JSON.stringify(msg)})
    // send via websocket
    ws.send(JSON.stringify({type:'send', message: msg}))
    setMessages(m=>[...m, msg])
    inputRef.current.value=''
  }
  return (<div style={{padding:20}}>
    <h3>Chat with {other}</h3>
    <div style={{border:'1px solid #ccc', height:300, overflow:'auto', padding:10'}}>
      {messages.map((m,i)=>(<div key={i} style={{textAlign: m.sender===me ? 'right':'left'}} aria-live='polite'>
        <div><strong>{m.sender}</strong></div>
        <div>{m.content}</div>
        <div style={{fontSize:12}}>{new Date(m.timestamp).toLocaleString()} - {m.status}</div>
      </div>))}
    </div>
    <div style={{marginTop:8}}>
      <input aria-label='message' ref={inputRef} onKeyDown={(e)=> e.key==='Enter' && send()} placeholder='Type message'/>
      <button onClick={send}>Send</button>
    </div>
  </div>)
}
