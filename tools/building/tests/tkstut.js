const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,karts,simKart,enterKart,settings,terrainH,TOWNS,WORLD,SPAWN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.karts,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1200);
 const r=await pg.evaluate(()=>{ const out={}; const k=T.karts[0];
   const run=(name,x,z,yaw,n,steer)=>{ Object.assign(k,{x,z,y:T.terrainH(x,z)+0.3,yaw,vx:0,vz:0,vy:0,pitch:0,roll:0,air:false}); let air=0, tog=0, rev=0, maxv=0, pa=false, pv=0, pd=0, jerk=0, hpL=k.hp, pp=k.pitch, dpm=0;
     for(let i=0;i<n;i++){ T.simKart(k,{fw:1,st:steer?Math.sin(i/40)*0.3:0,hb:false},1/60); if(k.air!==pa){ tog++; pa=k.air; } if(k.air) air++; const dv=k.vf-pv; if(i>60&&dv*pd<0&&Math.abs(dv)>0.15) rev++; if(i>60) jerk=Math.max(jerk,Math.abs(dv)); pd=dv; pv=k.vf; maxv=Math.max(maxv,k.vf); dpm=Math.max(dpm,Math.abs(k.pitch-pp)); pp=k.pitch; }
     out[name]={maxKmh:Math.round(maxv*3.6),endKmh:Math.round(k.vf*3.6),airFrames:air,airToggles:tog,speedReversals:rev,maxStepDv:+jerk.toFixed(2),maxPitchStep:+dpm.toFixed(3),dmg:Math.round(hpL-k.hp)}; };
   // along a road out of town 0, across open grass, and down a mountainside
   const rd=T.WORLD.roads[0].pts, a=rd[40], b2=rd[46]; run('road',T.SPAWN[0]+a[0],T.SPAWN[2]+a[1],Math.atan2(-(b2[0]-a[0]),-(b2[1]-a[1])),900,false);
   run('grass',60,60,0.7,900,true);
   // find a steep slope: sample for high ground then point downhill
   let best=null; for(let i=0;i<4000;i++){ const x=(Math.random()*2-1)*700, z=(Math.random()*2-1)*700, h=T.terrainH(x,z); if(h>60&&h<140&&(!best||Math.random()<0.02)) best=[x,z]; }
   if(best){ const [x,z]=best, e=3, gx=T.terrainH(x+e,z)-T.terrainH(x-e,z), gz=T.terrainH(x,z+e)-T.terrainH(x,z-e); run('downhill',x,z,Math.atan2(gx,gz),700,false); }
   return out; });
 console.log(JSON.stringify(r,null,1)); console.log(errs.join('\n')||'no errors'); await b.close(); })();
