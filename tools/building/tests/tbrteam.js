// Battle royale squads: with Squads chosen, three bots are your team (marked, dropping with you), the rest are in teams
// of four; teammates never count each other as foes and your shots don't target them.  node tbrteam.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,brFoes,bulletTargets'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); const s=document.getElementById('brTeamSel'); s.value='4'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 const r=await pg.evaluate(()=>{ const bots=T.BR.bots, mates=bots.filter(b=>b.team===0), teams=new Map(); bots.forEach(b=>teams.set(b.team,(teams.get(b.team)||0)+1));
   const near=mates.map(m=>Math.round(Math.hypot(m.pos.x-T.P.pos.x,m.pos.z-T.P.pos.z)));
   T.P.sky=null; T.P.bus=false; for(const b of bots) b.bus=false; const foeOk=mates.every(m=>!T.brFoes(m).includes(T.P)&&!T.brFoes(m).some(o=>o.team===0)), other=bots.find(b=>b.team!==0), otherFoes=T.brFoes(other);
   for(const b of bots) b.sky=null; const tg=T.bulletTargets();
   return {opt:!document.getElementById('brTeamOpt').hidden,mates:mates.length,marked:mates.filter(m=>!!m.mark).length,teams:[...teams.values()],near,foeOk,otherSeesYou:otherFoes.includes(T.P),otherTeamFoes:otherFoes.filter(o=>o.team===other.team).length,matesInTargets:tg.filter(t=>t.team===0).length}; });
 console.log(JSON.stringify(r));
 const ok=r.opt&&r.mates===3&&r.marked===3&&r.near.every(d=>d<40)&&r.foeOk&&r.otherSeesYou&&r.otherTeamFoes===0&&r.matesInTargets===0&&r.teams.filter(n=>n===4).length>=3;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();
