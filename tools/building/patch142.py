# patch142: friends. Every player gets a random account number (on the Profile tab). Type a friend's number on the
# Friends tab to send them a friend request; they accept it (or it's mutual if you both add each other). Friends show
# online or offline; an online friend can be invited to your lobby: they get a pop-up, press Join and they're in your
# party. Each game keeps a small presence connection open (its own PeerJS id from the account number) for this.
s=s.replace("</style>","""
#friendsCard .frow{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;background:rgba(255,255,255,.06);margin-top:6px}
#friendsCard .frow .dot{width:10px;height:10px;border-radius:50%;background:#6b7385;flex:0 0 auto}
#friendsCard .frow .dot.on{background:#3ee07a;box-shadow:0 0 8px #3ee07a}
#friendsCard .frow .fn{flex:1;min-width:0}
#friendsCard .frow .fn b{display:block;color:#fff;font:800 15px/1.2 var(--font-ui,system-ui);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#friendsCard .frow .fn small{color:rgba(225,236,255,.7);letter-spacing:.06em}
#friendsCard .frow .btn{padding:7px 12px}
#friendsCard h3{margin-top:14px}
#friendsCard .addrow{display:flex;gap:8px;flex-wrap:wrap;align-items:end;margin-top:8px}
#friendsCard .addrow input{font:800 18px/1 var(--font-hud);letter-spacing:.12em;width:11em}
#fStatus{min-height:1.2em}
#invitePop{position:fixed;left:50%;top:max(14px,env(safe-area-inset-top,0px));transform:translateX(-50%);z-index:60;display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;background:rgba(6,14,40,.92);border:2px solid #ffd21a;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.45);font:700 15px/1.3 var(--font-ui,system-ui);max-width:94vw}
#invitePop b{color:#ffd21a}
#invitePop .btn{padding:8px 14px}
</style>""",1)
rep("""      <div class="pcard" id="friendsCard"><h2>Friends</h2><p>Add a friend with the account number on their Profile tab.</p></div>""",
"""      <div class="pcard" id="friendsCard"><h2>Friends</h2><p>Add a friend with the account number on their Profile tab.</p>
        <div class="addrow"><label class="field" for="fAdd">Friend's account number<input id="fAdd" inputmode="numeric" maxlength="9" placeholder="1234 5678" autocomplete="off"></label><button class="btn primary" id="fAddBtn" type="button">Add friend</button></div>
        <p id="fStatus" role="status"></p>
        <div id="fReqs"></div><div id="fList"></div><div id="fSent"></div></div>""")
rep("""<div id="menu" class="lobby">""","""<div id="invitePop" hidden><span id="invText"></span><button class="btn primary" id="invJoin" type="button">Join</button><button class="btn" id="invNo" type="button">No thanks</button></div>
<div id="menu" class="lobby">""")
rep("""/* ---------- the 3D lobby: out on the water off the coastal town, looking at the lighthouse ---------- */""",
r"""/* ---------- friends ----------
   Your account number is made up once and kept. Your game listens for friends on a PeerJS id built from it; friends'
   games connect to that to see you're online, send friend requests and invites. The list is kept on this device. */
const FR={names:new Map(),acct:'',list:[],peer:null,conns:new Map(),online:new Set(),pollT:0,inv:null,retryT:0};
(function(){ try{ FR.acct=localStorage.getItem('cranklab.acct')||''; }catch(e){}
  if(!/^\d{8}$/.test(FR.acct)){ FR.acct=String(10000000+Math.floor(Math.random()*90000000)); try{ localStorage.setItem('cranklab.acct',FR.acct); }catch(e){} }
  try{ FR.list=JSON.parse(localStorage.getItem('cranklab.friends')||'[]').filter(f=>f&&/^\d{8}$/.test(f.id)); }catch(e){ FR.list=[]; } })();
const fmtAcct=a=>String(a).replace(/^(\d{4})(\d{4})$/,'$1 $2'), FR_ID=a=>PREFIX+'u-'+a;
function frSave(){ try{ localStorage.setItem('cranklab.friends',JSON.stringify(FR.list.map(f=>({id:f.id,name:f.name||'',st:f.st})))); }catch(e){} }
function frGet(id){ return FR.list.find(f=>f.id===id); }
function frName(){ return ($('pname').value.trim()||net.name||'Player').slice(0,16); }
function frStatus(t){ $('fStatus').textContent=t||''; }
function frHello(c){ try{ c.send({t:'hi',id:FR.acct,name:frName(),o:outfitIdx(settings.outfit)}); }catch(e){} }
function frSend(id,m){ const c=FR.conns.get(id); if(c&&c.open){ try{ c.send(m); return true; }catch(e){} } return false; }
function frWire(c,id0){ let id=id0;
  c.on('open',()=>{ frHello(c); });
  c.on('data',m=>{ if(!m||typeof m!=='object') return;
    if(m.t==='hi'&&/^\d{8}$/.test(m.id)){ id=String(m.id); FR.conns.set(id,c); FR.online.add(id); if(m.name) FR.names.set(id,String(m.name).slice(0,16)); const f=frGet(id); if(f){ if(m.name) f.name=String(m.name).slice(0,16); if(f.st==='sent') c.send({t:'req'}); frSave(); } frRender(); return; }
    if(!id) return; const f=frGet(id);
    if(m.t==='req'){ if(f&&(f.st==='sent'||f.st==='friend')){ f.st='friend'; frSave(); c.send({t:'acc'}); toast((f.name||fmtAcct(id))+' is now your friend'); } else if(!f){ FR.list.push({id,name:FR.names.get(id)||'',st:'in'}); frSave(); sfx('confirm'); toast('Friend request from '+(FR.names.get(id)||fmtAcct(id))); } frRender(); }
    else if(m.t==='acc'){ if(f&&f.st!=='friend'){ f.st='friend'; frSave(); toast((f.name||fmtAcct(id))+' accepted your friend request'); frRender(); } }
    else if(m.t==='bye'){ if(f){ FR.list=FR.list.filter(x=>x!==f); frSave(); frRender(); } }
    else if(m.t==='inv'&&f&&f.st==='friend'&&typeof m.code==='string'&&/^[A-Z0-9]{4,6}$/.test(m.code)){ frInvited(f,m.code); } });
  const gone=()=>{ if(id&&FR.conns.get(id)===c){ FR.conns.delete(id); FR.online.delete(id); frRender(); } };
  c.on('close',gone); c.on('error',gone); }
function frStart(){ if(typeof Peer==='undefined'||FR.peer||window.CRANK_NO_MP) return;
  const p=new Peer(FR_ID(FR.acct),PEER_OPTS); FR.peer=p;
  p.on('open',()=>{ FR.pollT=0; });
  p.on('connection',c=>frWire(c,null));
  p.on('error',err=>{ if(err.type==='peer-unavailable'){ const m=/u-(\d{8})/.exec(err.message||''); if(m){ FR.online.delete(m[1]); FR.conns.delete(m[1]); frRender(); } return; }
    if(err.type==='unavailable-id'){ try{ p.destroy(); }catch(e){} FR.peer=null; FR.retryT=30; return; } }); // this account is open in another tab: try again later
  p.on('disconnected',()=>{ try{ p.reconnect(); }catch(e){} }); }
// every so often, look in on each friend (and anyone you've sent a request to) who isn't connected
function frPoll(dt){ if(!FR.peer){ if(FR.retryT>0&&(FR.retryT-=dt)<=0) frStart(); return; } if(!FR.peer.open) return; FR.pollT-=dt; if(FR.pollT>0) return; FR.pollT=20;
  for(const f of FR.list){ if(f.st==='in'||FR.conns.has(f.id)) continue; try{ const c=FR.peer.connect(FR_ID(f.id),{reliable:true}); frWire(c,f.id); c.on('open',()=>{ FR.conns.set(f.id,c); FR.online.add(f.id); frRender(); }); }catch(e){} } }
function frAdd(){ const id=$('fAdd').value.replace(/\D/g,''); if(!/^\d{8}$/.test(id)){ frStatus('An account number is 8 digits.'); return; } if(id===FR.acct){ frStatus("That's your own number."); return; }
  let f=frGet(id); if(f&&f.st==='friend'){ frStatus('Already friends.'); return; }
  if(f&&f.st==='in'){ frAccept(id); return; }
  if(!f){ f={id,name:'',st:'sent'}; FR.list.push(f); frSave(); } $('fAdd').value=''; frStatus('Friend request sent to '+fmtAcct(id)+'. It arrives when they are online.');
  if(!frSend(id,{t:'req'})){ FR.pollT=0; } frRender(); }
function frAccept(id){ const f=frGet(id); if(!f) return; f.st='friend'; frSave(); frSend(id,{t:'acc'}); FR.pollT=0; frRender(); }
function frRemove(id){ frSend(id,{t:'bye'}); FR.list=FR.list.filter(f=>f.id!==id); frSave(); const c=FR.conns.get(id); if(c){ try{ c.close(); }catch(e){} } FR.conns.delete(id); FR.online.delete(id); frRender(); }
// invite: into the party you're in, or a new one you lead
function frInvite(id){ const f=frGet(id); if(!f||!FR.online.has(id)) return;
  const go=()=>{ if(frSend(id,{t:'inv',code:net.code,name:frName()})) toast('Invite sent to '+(f.name||fmtAcct(id))); else toast((f.name||fmtAcct(id))+' just went offline'); };
  if(net.role&&net.code){ go(); return; }
  readName(); hostGame(); let n=0; const w=setInterval(()=>{ if(net.role==='host'&&net.code){ clearInterval(w); go(); renderParty(); } else if(++n>60){ clearInterval(w); toast("Couldn't start a party. Try again."); } },250); }
function frInvited(f,code){ if(net.code===code) return; FR.inv={code,from:f}; $('invText').innerHTML='<b></b> invited you to their lobby'; $('invText').querySelector('b').textContent=f.name||fmtAcct(f.id); $('invitePop').hidden=false; sfx('confirm');
  clearTimeout(frInvited.t); frInvited.t=setTimeout(()=>{ $('invitePop').hidden=true; FR.inv=null; },30000); }
$('invJoin').addEventListener('click',()=>{ const v=FR.inv; $('invitePop').hidden=true; FR.inv=null; if(!v) return; if(playing) openMenu(); P.everPlayed=false; $('jcode').value=v.code; joinGame(); showTab('play'); });
$('invNo').addEventListener('click',()=>{ $('invitePop').hidden=true; FR.inv=null; });
function frRender(){ const box=(el,html)=>{ $(el).innerHTML=html; }, esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const reqs=FR.list.filter(f=>f.st==='in'), fr=FR.list.filter(f=>f.st==='friend').sort((a,b)=>FR.online.has(b.id)-FR.online.has(a.id)), sent=FR.list.filter(f=>f.st==='sent');
  box('fReqs',reqs.length?'<h3>Friend requests</h3>'+reqs.map(f=>`<div class="frow"><span class="dot${FR.online.has(f.id)?' on':''}"></span><span class="fn"><b>${esc(f.name||'Player')}</b><small>${fmtAcct(f.id)}</small></span><button class="btn primary" data-acc="${f.id}">Accept</button><button class="btn" data-rm="${f.id}">Decline</button></div>`).join(''):'');
  box('fList','<h3>Friends</h3>'+(fr.length?fr.map(f=>{ const on=FR.online.has(f.id); return `<div class="frow"><span class="dot${on?' on':''}"></span><span class="fn"><b>${esc(f.name||'Player')}</b><small>${fmtAcct(f.id)} · ${on?'Online':'Offline'}</small></span><button class="btn${on?' primary':''}" data-inv="${f.id}" ${on?'':'disabled'}>Invite to lobby</button><button class="btn" data-rm="${f.id}" aria-label="Remove friend">✕</button></div>`; }).join(''):'<p>No friends yet.</p>'));
  box('fSent',sent.length?'<h3>Sent</h3>'+sent.map(f=>`<div class="frow"><span class="dot"></span><span class="fn"><b>${fmtAcct(f.id)}</b><small>Waiting for them to accept</small></span><button class="btn" data-rm="${f.id}">Cancel</button></div>`).join(''):'');
  const n=reqs.length, tb=document.querySelector('.mtabs button[data-tab=friends]'); if(tb) tb.textContent=n?'Friends ('+n+')':'Friends'; }
$('friendsCard').addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; if(b.dataset.acc) frAccept(b.dataset.acc); else if(b.dataset.rm) frRemove(b.dataset.rm); else if(b.dataset.inv) frInvite(b.dataset.inv); });
$('fAddBtn').addEventListener('click',frAdd); $('fAdd').addEventListener('keydown',e=>{ if(e.key==='Enter') frAdd(); });
$('acctNum').textContent=fmtAcct(FR.acct);
$('acctCopy').addEventListener('click',()=>{ const t=FR.acct, done=()=>toast('Account number copied'); if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done,()=>toast('Your number: '+fmtAcct(t))); else toast('Your number: '+fmtAcct(t)); });
frRender(); setTimeout(frStart,1500);

/* ---------- the 3D lobby: out on the water off the coastal town, looking at the lighthouse ---------- */""")
rep("""  fitView(); updateCamera(); lobbyView(dt);""","""  frPoll(dt); fitView(); updateCamera(); lobbyView(dt);""")
# the party box on the Friends tab: the code is the way in for anyone who isn't your friend yet
rep("""        <h2>Party</h2>""","""        <h2>Party code</h2><p class="sub" style="margin:0 0 8px">Or play with anyone using a party code.</p>""")
