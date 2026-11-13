# patch203: the storm forms a while after the bus sets off (about a minute and a half after the last jump), so nobody
# knows where the circle will be when they choose where to land: until then there's no wall, nothing on the map, and
# the HUD counts down to the storm forming
rep("""  // the storm: wait, then close in to the next circle
  S.t-=dt;""","""  // the storm: hidden at first (forms a minute before it first closes), then wait, then close in to the next circle
  if(S.hid&&!(S.ph===0&&S.state==='wait'&&S.t>60)){ S.hid=false; toast('The storm has formed · get inside the circle'); try{ sfx('storm_close'); }catch(e){} }
  S.t-=dt;""")
rep("""const W=BR.wall; W.visible=!lobbyActive();""","""const W=BR.wall; W.visible=!lobbyActive()&&!S.hid;""")
rep("""    el.textContent=S.state==='wait'?'Storm closes in '+mm:""","""    const tf=Math.max(0,Math.ceil(S.t-60)), mf=Math.floor(tf/60)+':'+String(tf%60).padStart(2,'0');
    el.textContent=S.hid?'Storm forms in '+mf:S.state==='wait'?'Storm closes in '+mm:""")
rep("""function brMiniMap(g,tx,tz,sc,dpr){ if(!BR.on) return; const S=BR.storm; g.save();""","""function brMiniMap(g,tx,tz,sc,dpr){ if(!BR.on) return; const S0=BR.storm, S=S0.hid?{cx:SPAWN[0],cz:SPAWN[2],r:1e5,tx:0,tz:0,tr:0,state:'done'}:S0; g.save(); // (no storm on the map before it forms)""")
rep("""      else { const a=Math.random()*Math.PI*2, r=Math.sqrt(Math.random())*Math.max(8,S.tr*0.8); b.dest={pts:[[S.tx+Math.cos(a)*r,S.tz+Math.sin(a)*r,4]],i:0,linger:3}; } }""","""      else { const a=Math.random()*Math.PI*2, hid=S.hid, R0=hid?MAP_R*0.75:S.tr, r=Math.sqrt(Math.random())*Math.max(8,R0*0.8), cx0=hid?SPAWN[0]:S.tx, cz0=hid?SPAWN[2]:S.tz; b.dest={pts:[[cx0+Math.cos(a)*r,cz0+Math.sin(a)*r,4]],i:0,linger:3}; } }""")
rep("""BR.storm={cx:SPAWN[0],cz:SPAWN[2],r:MAP_R*1.08,ph:0,state:'wait',t:BR_SHRINK[0][0]+BRBUS.T};""","""BR.storm={cx:SPAWN[0],cz:SPAWN[2],r:MAP_R*1.08,ph:0,state:'wait',t:BR_SHRINK[0][0]+BRBUS.T,hid:true};""")
