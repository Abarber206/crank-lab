# ---------- 41. drop-ins: everyone in a party drops together from high up, and every drop-in starts with just the pickaxe ----------
rep("function defaultLoadout(){","""function emptyLoadout(){ defaultLoadout(); P.inv=[null,null,null,null,null]; P.items={bandage:0,mini:0}; P.nades=0; P.res={light:0,medium:0,shells:0,heavy:0,rockets:0}; P.slot=-1; if(typeof selectPick==='function') selectPick(); syncItems(); }
// where a party match drops everyone: one spot (from the match number, the same on every screen), each player a few metres apart
function matchDrop(){ const r=seeded(1000+party.seq), a=r()*6.283, cx=SPAWN[0]+Math.cos(a)*30, cz=SPAWN[2]+Math.sin(a)*30;
  let h=0; for(const c of String(net.id||'me')) h=(h*31+c.charCodeAt(0))>>>0; const b=(h%360)*Math.PI/180, d=4+(h>>9)%6;
  emptyLoadout(); skyDrop(cx+Math.cos(b)*d,cz+Math.sin(b)*d,SKY_MATCH); }
function defaultLoadout(){""")
s=s.replace("respawn(); round.you=0; round.bot=0; if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*30,SPAWN[2]+Math.sin(a)*30,SKY_MATCH); }","respawn(); round.you=0; round.bot=0; if(skyDropAllowed()) matchDrop();")
s=s.replace("respawn(); sfx('win'); if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*30,SPAWN[2]+Math.sin(a)*30,SKY_MATCH); }","respawn(); sfx('win'); if(skyDropAllowed()) matchDrop();")
rep("if((!net.role||!party.live)&&skyDropAllowed()) skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); }","if((!net.role||!party.live)&&skyDropAllowed()){ emptyLoadout(); skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); } }")
rep("$('respawn').addEventListener('click',()=>{ respawn(); if(skyDropAllowed()){","$('respawn').addEventListener('click',()=>{ respawn(); if(skyDropAllowed()){ emptyLoadout();")
rep("function onPartyStart(m){\n  party.live=true;","function onPartyStart(m){\n  if(m.seq!=null) party.seq=m.seq; party.live=true;")
