# patch179: cars and players don't pass through each other.
#  - A parked car is solid along its real length and angle (a row of small boxes down its middle, lower over the bonnet
#    and boot), not one square box snapped to the nearest right angle (which let you walk into a car parked at an angle
#    and stopped you on thin air beside it).
#  - A buggy or boat being driven stops against people (you, other players, the bot, battle-royale bots) the way it
#    stops against a wall; and if one rolls into you while you stand still, you're nudged out of its way.
rep("""  // car: long side follows its yaw, rounded to the nearest 90 degrees for a simple box
  const along=Math.abs(Math.cos(p.g.rotation.y))>.7; return [along?[x-2,0,z-.95,x+2,1.8,z+.95]:[x-.95,0,z-2,x+.95,1.8,z+2]];""",
    """  // car: a row of small boxes down its middle along its real angle (lower at the bonnet and the boot)
  const yw=p.g.rotation.y, ux=Math.cos(yw), uz=-Math.sin(yw), out=[]; for(const a of [-1.55,-0.93,-0.31,0.31,0.93,1.55]){ const cx=x+ux*a, cz=z+uz*a, r=0.72, h=Math.abs(a)>1.2?1.15:1.75; out.push([cx-r,0,cz-r,cx+r,h,cz+r]); }
  return out;""")
rep("""  for(const o of karts) if(o!==k&&!o.dead&&Math.abs(o.x-x)<4&&Math.abs(o.z-z)<4) ps.add(o.solid);
  const hit=(cx,cz)=>{""","""  for(const o of karts) if(o!==k&&!o.dead&&Math.abs(o.x-x)<4&&Math.abs(o.z-z)<4) ps.add(o.solid);
  { const ppl=peopleNear(k,x,z); if(ppl.length) ps.add({boxes:ppl}); } // people are in the way too
  const hit=(cx,cz)=>{""")
rep("""function stepKarts(dt){ if(!karts) return; const me=ME();""","""// the people a vehicle could run into: a box round each (not anyone riding in it)
function peopleNear(k,x,z){ const out=[], add=(p,id)=>{ if(!p||Math.abs(p.x-x)>4.5||Math.abs(p.z-z)>4.5) return; if(id!=null&&k.seats&&k.seats.includes(id)) return; out.push([p.x-0.42,p.y,p.z-0.42,p.x+0.42,p.y+1.8,p.z+0.42]); };
  if(!(P.kart&&P.kart.k===k)&&!isDead()&&!P.sky) add(P.pos,net.role?net.id:'me');
  if(net.players) net.players.forEach(pl=>{ if(pl.alive&&pl.pos) add(pl.pos,pl.id); });
  if(typeof B!=='undefined'&&B&&B.active&&!B.down) add(B.pos,'bot'); if(typeof AB!=='undefined'&&AB&&AB.active&&!AB.dead) add(AB.pos,'ally');
  if(typeof BR!=='undefined'&&BR.on) for(const b of BR.bots) if(b.alive&&!b.sky&&!b.bus) add(b.pos,null);
  return out; }
function stepKarts(dt){ if(!karts) return; const me=ME();
  if(!P.kart&&!isDead()) for(const k of karts){ if(k.dead||Math.abs(k.x-P.pos.x)>4||Math.abs(k.z-P.pos.z)>4) continue; if(k.solid.boxes.some(b=>P.pos.y+1.6>b[1]&&P.pos.y<b[4]&&circBox(b,P.pos.x,P.pos.z,0.38))) depen(new Set([k.solid]),P); } // rolled into you: step aside""")
