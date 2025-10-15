import React, {useEffect, useState} from 'react'
export default function Inbox(){
  const [me, setMe] = useState(localStorage.getItem('me')||'')
  const [msgs, setMsgs] = useState([])
  useEffect(()=>{ if(!me) window.location.href='/login' },[me])
  useEffect(()=>{
    async function load(){
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:8000/api/messages/', {headers:{Authorization:'Bearer '+token}})
      if(res.ok){
        const j = await res.json()
        setMsgs(j)
      }
    }
    load()
  },[])
  return (<div style={{display:'flex',padding:20}}>
    <div style={{width:300}}>
      <h3>Chats</h3>
      <ul>
        {Array.from(new Set(msgs.map(m=>m.sender===me?m.recipient:m.sender))).map(u=>(
          <li key={u}><a href={'/chat/'+u}>{u}</a></li>
        ))}
      </ul>
    </div>
    <div style={{flex:1, paddingLeft:20}}>
      <p>Select chat to open</p>
    </div>
  </div>)
}
