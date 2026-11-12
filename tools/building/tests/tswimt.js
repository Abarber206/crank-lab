// swimming transitions: walk from the shore into deep water and back out, recording the arms and body every frame.
// Passes when going in and coming out each switch the swim pose once (no flicker at the water's edge) and the limbs
// and body never jump between two frames.  node tswimt.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,terrainH,waterAt,waterDepth,localHero,SPAWN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.localHero,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const spot=await pg.evaluate(()=>{ const S=T.SPAWN; let best=null; for(let k=0;k<400000&&!best;k++){ const a=k*2.399, d=600+(k%4000)*0.055, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d;
   if(T.waterDepth(x,z)>3.2&&T.waterDepth(x+6,z)>3&&T.waterDepth(x-6,z)>3&&T.waterDepth(x,z+6)>3&&T.waterDepth(x,z-6)>3){
     for(let q=0;q<16&&!best;q++){ const aa=q*Math.PI/8; for(let r=8;r<70;r+=2){ const sx=x+Math.cos(aa)*r, sz=z+Math.sin(aa)*r; if(T.waterDepth(sx,sz)<0.05&&T.waterAt(sx,sz)<-999){ const ex=sx+Math.cos(aa)*3, ez=sz+Math.sin(aa)*3, w=T.waterAt(x,z), g=T.terrainH(ex,ez); if(g>w+0.1&&T.waterAt(ex,ez)<-999) best={x,z,sx:ex,sz:ez,ya:Math.atan2(-(sx-x),-(sz-z)),r}; break; } } } } }
   return best; });
 console.log('spot',JSON.stringify(spot));
 await pg.evaluate(sp=>{ T.P.pos.set(sp.sx,T.terrainH(sp.sx,sp.sz)+0.05,sp.sz); T.P.vel.set(0,0,0); T.P.yaw=sp.ya+Math.PI; T.P.pitch=0; window.__rec=[];
   const R=T.localHero.rig, A=T.localHero.anim, G=T.localHero.group; const f=()=>{ const v=new THREE.Vector3(); let hy=-9; if(T.P.swim){ for(const a of [R.armL,R.armR]){ (a.fing||a.wr).getWorldPosition(v); hy=Math.max(hy,v.y-T.waterAt(T.P.pos.x,T.P.pos.z)); } } window.__rec.push([R.armL.sh.rotation.x,R.armL.sh.rotation.z,R.armL.el.rotation.x,G.rotation.x,G.position.y-T.P.pos.y,A.swimT||0,!!T.P.swim,hy,Math.hypot(T.P.vel.x,T.P.vel.z),A.swC||0,A.swimMv||0]); requestAnimationFrame(f); }; requestAnimationFrame(f); },spot);
 console.log(JSON.stringify(await pg.evaluate(sp=>({p:[T.P.pos.x,T.P.pos.y,T.P.pos.z].map(v=>+v.toFixed(1)),wd:T.waterDepth(T.P.pos.x,T.P.pos.z),wa:T.waterAt(T.P.pos.x,T.P.pos.z),sw:!!T.P.swim,st:T.localHero.anim.swimT,gr:T.terrainH(T.P.pos.x,T.P.pos.z)}),spot))); await sleep(800); await pg.keyboard.down('KeyW'); let inT=-1; for(let i=0;i<80;i++){ await sleep(400); if(await pg.evaluate(()=>T.localHero.anim.swimT>=1)){ inT=i; break; } } await sleep(1500); await pg.keyboard.up('KeyW');
 await sleep(1200); await pg.evaluate(sp=>{ T.P.yaw=sp.ya; },spot); await pg.keyboard.down('KeyW'); let outT=-1; for(let i=0;i<70;i++){ await sleep(400); if(await pg.evaluate(()=>!T.P.swim&&(T.localHero.anim.swimT||0)===0)){ outT=i; break; } } await sleep(1200); await pg.keyboard.up('KeyW');
 const rec=await pg.evaluate(()=>window.__rec);
 let flips=0, dir=0, mx=[0,0,0,0,0]; for(let i=1;i<rec.length;i++){ const d=rec[i][5]-rec[i-1][5]; const s=d>1e-6?1:d<-1e-6?-1:0; if(s&&s!==dir){ flips++; dir=s; } for(let c=0;c<5;c++) mx[c]=Math.max(mx[c],Math.abs(rec[i][c]-rec[i-1][c])); }
 let handUp=-9; for(const q of rec) if(q[5]>=1&&q[8]>1) handUp=Math.max(handUp,q[7]); if(process.env.V){ const B=new Array(10).fill(-9); for(const q of rec) if(q[5]>=1&&q[8]>1){ const i=Math.floor(q[9]*10)%10; B[i]=Math.max(B[i],q[7]); } console.log('by phase',B.map(v=>v.toFixed(2)).join(' '), 'mv', rec.filter(q=>q[5]>=1&&q[8]>1).map(q=>q[10]).reduce((a,b)=>Math.max(a,b),0)); }
 const r={handUp:+handUp.toFixed(2),frames:rec.length,inT,outT,swimDirChanges:flips,maxJump:{shX:+mx[0].toFixed(3),shZ:+mx[1].toFixed(3),elX:+mx[2].toFixed(3),bodyTilt:+mx[3].toFixed(3),bodyY:+mx[4].toFixed(3)}};
 { const J=[]; for(let i=1;i<rec.length;i++){ const j=Math.max(...[0,1,2].map(c=>Math.abs(rec[i][c]-rec[i-1][c]))); if(j>0.25) J.push(i+":"+j.toFixed(2)+" st="+rec[i-1][5].toFixed(2)+">"+rec[i][5].toFixed(2)+" sw="+rec[i][6]+" sh="+rec[i-1].slice(0,3).map(v=>v.toFixed(2))+">"+rec[i].slice(0,3).map(v=>v.toFixed(2))); } if(process.env.V) console.log(J.slice(0,12).join("\n")); }
 console.log(JSON.stringify(r)); const ok=handUp<0.05&&inT>=0&&outT>=0&&flips<=2&&mx[0]<0.35&&mx[1]<0.35&&mx[3]<0.2&&mx[4]<0.25;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
