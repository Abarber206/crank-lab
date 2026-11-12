# patch177: a match starts with nothing: no materials and no shield (farm for builds, find shields). A new Shield
# Potion (epic, +50 shield up to 100) joins the loot. When you're eliminated in a match everything you carried spills
# on the ground (guns with their rounds, ammo, heals, grenades, materials) and it stays there until someone takes it.
# Infinite materials (the Settings switch) only applies outside battle royale.
rep("""             mini:{name:'Small Shield Potion',rarity:'rare',use:2.0,max:6,start:3,amt:25,cap:50,stat:'sh',sound:'shield'}};""",
    """             mini:{name:'Small Shield Potion',rarity:'rare',use:2.0,max:6,start:3,amt:25,cap:50,stat:'sh',sound:'shield'},
             big:{name:'Shield Potion',rarity:'epic',use:5.0,max:3,start:0,amt:50,cap:100,stat:'sh',sound:'shield'}};
function infMats(){ return settings.infMats&&!(typeof BR!=='undefined'&&BR.on); } // (a battle royale is always played for real)""")
rep("""  if((P.items[P.item]|0)<=0){ if(!quiet) toast('Out of '+(P.item==='mini'?'small shields':'bandages')); return; }
  if(P[I.stat]>=I.cap){ if(!quiet) toast(I.stat==='hp'?'Bandages heal up to 75 health':'Small shields go up to 50 shield'); return; }""",
    """  if((P.items[P.item]|0)<=0){ if(!quiet) toast('Out of '+(P.item==='mini'?'small shields':P.item==='big'?'shield potions':'bandages')); return; }
  if(P[I.stat]>=I.cap){ if(!quiet) toast(I.stat==='hp'?'Bandages heal up to 75 health':P.item==='big'?'Your shield is full':'Small shields go up to 50 shield'); return; }""")
rep("""function giveItems(b,m){ P.items.bandage=Math.min(ITEMS.bandage.max,(P.items.bandage|0)+b); P.items.mini=Math.min(ITEMS.mini.max,(P.items.mini|0)+m);
  for(const k of ['bandage','mini']) if""","""function giveItems(b,m){ P.items.bandage=Math.min(ITEMS.bandage.max,(P.items.bandage|0)+b); P.items.mini=Math.min(ITEMS.mini.max,(P.items.mini|0)+m);
  for(const k of ['bandage','mini','big']) if""")
rep("""P.items={bandage:0,mini:0}; P.nades=0; P.res={light:0,medium:0,shells:0,heavy:0,rockets:0}; P.slot=-1;""","""P.items={bandage:0,mini:0,big:0}; P.nades=0; P.res={light:0,medium:0,shells:0,heavy:0,rockets:0}; P.mats={wood:0,brick:0,metal:0}; P.slot=-1; if(typeof syncMats==='function'&&document.getElementById('matStock')) syncMats();""")
rep("""  P.items={bandage:ITEMS.bandage.start,mini:ITEMS.mini.start}; P.nades=0;""","""  P.items={bandage:ITEMS.bandage.start,mini:ITEMS.mini.start,big:0}; P.nades=0;""")
# no shield and no materials when you come back in either
rep("""P.fallTop=null; P.hp=100; P.sh=100; defaultLoadout(); P.reloadT=0; P.useT=0; syncItems(); P.mats={wood:30,brick:0,metal:0};""","""P.fallTop=null; P.hp=100; P.sh=0; defaultLoadout(); P.reloadT=0; P.useT=0; syncItems(); P.mats={wood:0,brick:0,metal:0};""")
for a,b in [("""  if(E===P&&!settings.infMats&&((P.mats&&P.mats[buildMat])|0)<BUILD_COST)""","""  if(E===P&&!infMats()&&((P.mats&&P.mats[buildMat])|0)<BUILD_COST)"""),
            ("""  if(E===P){ if(!settings.infMats){ P.mats[buildMat]-=BUILD_COST; syncMats(); }""","""  if(E===P){ if(!infMats()){ P.mats[buildMat]-=BUILD_COST; syncMats(); }"""),
            ("""function giveMats(mat,n,point){ if(settings.infMats||n<=0) return;""","""function giveMats(mat,n,point){ if(infMats()||n<=0) return;"""),
            ("""  const st=$('matStock'); if(st){ st.hidden=settings.infMats; if(!settings.infMats)""","""  const st=$('matStock'); if(st){ st.hidden=infMats(); if(!infMats())"""),
            ("""<b>${settings.infMats?'∞':(P.mats[m]|0)}</b>""","""<b>${infMats()?'∞':(P.mats[m]|0)}</b>""")]:
    rep(a,b)
# the shield potion's model: a tall bottle of blue shield with a big cork, and its flat stand-in icon
rep("""  g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; } });
  return g;
}
let _lootTex=null;""","""  else if(item==='big'){ // a tall bottle of shield, a darker blue, with a broad shoulder and a big cork
    const body=new THREE.Mesh(new THREE.CylinderGeometry(.1,.12,.24,18),toon(0x2a8cff)); body.position.y=.13; g.add(body);
    const sh=new THREE.Mesh(new THREE.SphereGeometry(.1,18,10,0,Math.PI*2,0,Math.PI/2),toon(0x2a8cff)); sh.position.y=.25; g.add(sh);
    const glass=new THREE.Mesh(new THREE.CylinderGeometry(.122,.122,.05,18),toon(0xcdeeff)); glass.position.y=.03; g.add(glass);
    const label=new THREE.Mesh(new THREE.CylinderGeometry(.104,.114,.08,18,1,true),toon(0xf2f2ee)); label.position.y=.13; g.add(label);
    const shine=new THREE.Mesh(new THREE.BoxGeometry(.02,.16,.01),toon(0xffffff)); shine.position.set(-.06,.15,.085); g.add(shine);
    const neck=new THREE.Mesh(new THREE.CylinderGeometry(.04,.05,.07,12),toon(0xcdeeff)); neck.position.y=.37; g.add(neck);
    const cork=new THREE.Mesh(new THREE.CylinderGeometry(.05,.044,.07,10),toon(0x9a6a3a)); cork.position.y=.43; g.add(cork); }
  g.traverse(o=>{ if(o.isMesh){ o.castShadow=true; } });
  return g;
}
let _lootTex=null;""")
rep("""  if(WEAPONS[item]||item==='mini'){ g.add(beam); g.add(ring); }""","""  if(WEAPONS[item]||item==='mini'||item==='big'){ g.add(beam); g.add(ring); }""")
rep("""const ICONS={""","""const ICONS={
  big:'<path d="M18 7h12v6l5 4v22a4 4 0 0 1-4 4H17a4 4 0 0 1-4-4V17l5-4z" fill="#d9f1ff" stroke="#1d232c" stroke-width="2" stroke-linejoin="round"/><path d="M14 22h20v17a3 3 0 0 1-3 3H17a3 3 0 0 1-3-3z" fill="#2a8cff"/><rect x="19" y="3" width="10" height="5" rx="1.5" fill="#9a6a3a" stroke="#1d232c" stroke-width="1.5"/>',""")
# in chests: the shield potion is one of the extras, weighted by its rarity like the rest
rep("""const pool=[['bandage',3],['ammo',0],['nade',2],['mini',2]],""","""const pool=[['bandage',3],['ammo',0],['nade',2],['mini',2],['big',1]],""")
# ---- eliminated in a match: spill everything; dropped loot stays until it's picked up
rep("""function netDrop(item,n,pos,vel,keep){
  if(net.role==='client'){ netSend({type:'dd',item,n,p:pos.toArray().map(v=>+v.toFixed(2)),v:vel.toArray().map(v=>+v.toFixed(2))}); return; }""",
    """function netDrop(item,n,pos,vel,keep){
  if(net.role==='client'){ netSend({type:'dd',item,n,k:keep?1:0,p:pos.toArray().map(v=>+v.toFixed(2)),v:vel.toArray().map(v=>+v.toFixed(2))}); return; }""")
rep("""  else if(m.type==='dd'){ netDrop(m.item,m.n,new THREE.Vector3(...m.p),new THREE.Vector3(...m.v)); }""","""  else if(m.type==='dd'){ netDrop(m.item,m.n,new THREE.Vector3(...m.p),new THREE.Vector3(...m.v),!!m.k); }""")
rep("""function brPlayerOut(by){ if(BR.out) return; BR.out=true;""","""// everything you carry, on the ground in a ring where you fell (kept until someone picks it up)
function spillLoot(){ if(P.spilled) return; const list=[];
  (P.inv||[]).forEach(id=>{ if(!id) return; if(WEAPONS[id]&&id!=='nade') list.push([id,P.ammo&&P.ammo[id]!=null?P.ammo[id]:WEAPONS[id].mag]); else if(ITEMS[id]&&(P.items[id]|0)>0) list.push([id,P.items[id]|0]); });
  if((P.nades|0)>0) list.push(['nade',P.nades|0]);
  for(const k in (P.res||{})) if((P.res[k]|0)>0) list.push([k,P.res[k]|0]);
  if(!list.length) return; P.spilled=true; const n=list.length, c=P.pos;
  list.forEach(([item,cnt],q)=>{ const a=q/n*Math.PI*2, r=0.9+0.25*(q%2); netDrop(item,cnt,new THREE.Vector3(c.x+Math.cos(a)*r*0.3,c.y+1.0,c.z+Math.sin(a)*r*0.3),new THREE.Vector3(Math.cos(a)*1.8,3.2,Math.sin(a)*1.8),true); });
  P.inv=[null,null,null,null,null]; P.items={bandage:0,mini:0,big:0}; P.nades=0; P.res={light:0,medium:0,shells:0,heavy:0,rockets:0}; syncItems(); }
function inMatch(){ return (typeof BR!=='undefined'&&BR.on)||(typeof skyDropAllowed==='function'&&skyDropAllowed()); }
function brPlayerOut(by){ if(BR.out) return; spillLoot(); BR.out=true;""")
rep("""  if(hurt(P,m.dmg)){ if(rbCanKnock()){ rbKnock(m.id,m.w); return; } net.dead=true;""","""  if(hurt(P,m.dmg)){ if(rbCanKnock()){ rbKnock(m.id,m.w); return; } if(inMatch()) spillLoot(); net.dead=true;""")
rep("""function rbBleedOut(){ if(!P.down) return; const d=P.down; P.down=null; P.hp=0;""","""function rbBleedOut(){ if(!P.down) return; const d=P.down; P.down=null; if(inMatch()) spillLoot(); P.hp=0;""")
rep("""  if(net.role){ net.dead=true; net.deaths++; const e={type:'elim',id:net.id,by:net.id,w:'fall'};""","""  if(net.role){ if(inMatch()) spillLoot(); net.dead=true; net.deaths++; const e={type:'elim',id:net.id,by:net.id,w:'fall'};""")
# a new life (or a new match) can spill again
rep("""function respawn(){ P.down=null;""","""function respawn(){ P.spilled=false; P.down=null;""")
rep("""function emptyLoadout(){ defaultLoadout();""","""function emptyLoadout(){ P.spilled=false; defaultLoadout();""")
