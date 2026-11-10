# ---------- 57. gunshots rendered as recorded-style samples: a hard muzzle crack, a body of air that darkens as it dies,
# a low thump, the gun's action clacking, and the shot bouncing back off the world. A few takes per gun so repeats differ. ----------
rep("function sfx(k){\n  if(!AC) return;", r"""const GUN_SND={ // len s; crack/blast/boom/sub/mech weights; times in s; f0->f1 the body's darkening sweep; slap = echo strength
  shot:       {len:0.75,crack:0.8,crackT:0.0012,blast:1,blastT:0.028,f0:6500,f1:750,sweepT:0.012,boom:0.75,boomF:230,boomT:0.07,sub:0.4,subF:72,mech:[[0.028,0.16]],slap:0.34,drive:2.2,vol:0.9},
  shot_smg:   {len:0.5,crack:0.75,crackT:0.001,blast:1,blastT:0.019,f0:7200,f1:950,sweepT:0.009,boom:0.6,boomF:270,boomT:0.045,sub:0.25,subF:92,mech:[[0.02,0.2]],slap:0.24,drive:2,vol:0.78},
  shot_mg:    {len:0.85,crack:0.8,crackT:0.0013,blast:1,blastT:0.034,f0:6000,f1:620,sweepT:0.014,boom:0.85,boomF:205,boomT:0.09,sub:0.5,subF:62,mech:[[0.03,0.14]],slap:0.38,drive:2.3,vol:0.9},
  shot_mini:  {len:0.38,crack:0.7,crackT:0.0009,blast:1,blastT:0.015,f0:7000,f1:1000,sweepT:0.008,boom:0.55,boomF:260,boomT:0.035,sub:0.2,subF:95,mech:[],slap:0.18,drive:2,vol:0.62},
  shot_pistol:{len:0.55,crack:1,crackT:0.0011,blast:0.95,blastT:0.018,f0:7500,f1:1100,sweepT:0.009,boom:0.6,boomF:290,boomT:0.05,sub:0.3,subF:96,mech:[[0.024,0.22]],slap:0.3,drive:2.1,vol:0.82},
  shot_rev:   {len:1,crack:0.9,crackT:0.0014,blast:1,blastT:0.04,f0:6000,f1:600,sweepT:0.015,boom:0.9,boomF:180,boomT:0.1,sub:0.6,subF:60,mech:[],slap:0.5,drive:2.5,vol:0.95},
  shot_heavy: {len:1.1,crack:0.9,crackT:0.0016,blast:1,blastT:0.05,f0:5500,f1:500,sweepT:0.018,boom:1,boomF:160,boomT:0.13,sub:0.75,subF:50,mech:[[0.05,0.12]],slap:0.55,drive:2.7,vol:1},
  shot_sniper:{len:1.7,crack:1.2,crackT:0.0016,blast:1,blastT:0.055,f0:8000,f1:480,sweepT:0.02,boom:1,boomF:150,boomT:0.16,sub:0.85,subF:45,mech:[[0.55,0.2,1],[0.72,0.24,1]],slap:0.7,drive:2.8,vol:1},
  shot_heavyar:{len:0.85,crack:0.85,crackT:0.0013,blast:1,blastT:0.038,f0:6000,f1:620,sweepT:0.014,boom:0.9,boomF:190,boomT:0.09,sub:0.55,subF:60,mech:[[0.03,0.15]],slap:0.4,drive:2.4,vol:0.93},
  shot_tac:   {len:1.05,crack:0.55,crackT:0.0016,blast:1,blastT:0.06,f0:4600,f1:420,sweepT:0.022,boom:1,boomF:170,boomT:0.12,sub:0.7,subF:55,mech:[[0.06,0.18]],slap:0.55,drive:2.6,vol:0.98},
  shot_dbl:   {len:1.25,crack:0.6,crackT:0.0018,blast:1,blastT:0.08,f0:4200,f1:360,sweepT:0.028,boom:1,boomF:140,boomT:0.16,sub:0.9,subF:45,mech:[],slap:0.62,drive:2.8,vol:1},
  shot_sup:   {len:0.32,crack:0.25,crackT:0.0008,blast:0.7,blastT:0.012,f0:3200,f1:900,sweepT:0.006,boom:0.3,boomF:320,boomT:0.02,sub:0,subF:90,mech:[[0.006,0.55],[0.03,0.3]],slap:0.1,drive:1.6,vol:0.6},
  pump:       {len:1.1,crack:0.55,crackT:0.0016,blast:1,blastT:0.065,f0:4400,f1:400,sweepT:0.024,boom:1,boomF:165,boomT:0.13,sub:0.75,subF:52,mech:[[0.36,0.3,1],[0.48,0.34,1]],slap:0.58,drive:2.7,vol:1}
};
const gunTakes={};
function renderGun(o){ const sr=AC.sampleRate, n=Math.floor(sr*o.len), TAU=Math.PI*2, rnd=(a,b)=>a+Math.random()*(b-a);
  const crack=new Float32Array(n), body=new Float32Array(n), boom=new Float32Array(n);
  const f0=o.f0*rnd(0.9,1.1), f1=o.f1*rnd(0.88,1.12), bT=o.blastT*rnd(0.9,1.12), boT=o.boomT*rnd(0.9,1.1), subF=o.subF*rnd(0.93,1.07);
  let a1=0,a2=0,b1=0,b2=0,hp=0,ph=0;
  for(let i=0;i<n;i++){ const t=i/sr, w=Math.random()*2-1;
    hp+=0.35*(w-hp); crack[i]=(w-hp)*Math.exp(-t/o.crackT)*(t<0.0002?t/0.0002:1);              // the supersonic snap: bright and gone in a millisecond
    const fc=f1+(f0-f1)*Math.exp(-t/o.sweepT), a=1-Math.exp(-TAU*fc/sr); a1+=a*(w-a1); a2+=a*(a1-a2); // the blast darkens as it spreads
    body[i]=a2*(t<0.0004?t/0.0004:Math.exp(-(t-0.0004)/bT));
    const ab=1-Math.exp(-TAU*o.boomF/sr); b1+=ab*(w-b1); b2+=ab*(b1-b2); ph+=TAU*subF*(1+1.4*Math.exp(-t/0.012))/sr; // chest thump with a falling pitch
    boom[i]=(b2*0.7+Math.sin(ph)*o.sub*0.04)*(1-Math.exp(-t/0.0015))*Math.exp(-t/boT); }
  const norm=x=>{ let m=1e-9; for(let i=0;i<n;i++) m=Math.max(m,Math.abs(x[i])); return 1/m; };
  const kc=o.crack*norm(crack), kb=o.blast*norm(body), kk=o.boom*norm(boom), dry=new Float32Array(n);
  for(let i=0;i<n;i++) dry[i]=crack[i]*kc+body[i]*kb+boom[i]*kk;
  // the world answering: close bounces, then a dull slap off something far, a little different in each ear
  const L=new Float32Array(n), R=new Float32Array(n), taps=[[0.009,0.32,0.0115,0.3],[0.021,0.2,0.026,0.22],[0.047,0.14,0.039,0.15]];
  for(let i=0;i<n;i++){ L[i]=dry[i]; R[i]=dry[i]; }
  for(const [dl,gl,dr,gr] of taps){ const sl=Math.floor(dl*sr), sr2=Math.floor(dr*sr); for(let i=n-1;i>=0;i--){ if(i>=sl) L[i]+=dry[i-sl]*gl*o.slap; if(i>=sr2) R[i]+=dry[i-sr2]*gr*o.slap; } }
  const slapT=rnd(0.11,0.2), sd=Math.floor(slapT*sr), sd2=Math.floor((slapT+rnd(0.01,0.03))*sr); let s1=0,s2=0; const as=1-Math.exp(-TAU*900/sr);
  for(let i=0;i<n;i++){ s1+=as*((i>=sd?dry[i-sd]:0)-s1); s2+=as*((i>=sd2?dry[i-sd2]:0)-s2); L[i]+=s1*o.slap*0.55; R[i]+=s2*o.slap*0.5; }
  // the action: steel on steel, a few inharmonic rings that die fast (a bolt or slide, or a pump racking)
  for(const [mt,mv,big] of o.mech){ const s0=Math.floor((mt+rnd(-0.004,0.004))*sr), fs=big?[rnd(900,1300),rnd(2100,2700),rnd(3600,4300)]:[rnd(2400,3000),rnd(4100,4900),rnd(6200,7200)], dk=big?0.011:0.0045;
    for(let j=0;j<sr*0.12&&s0+j<n;j++){ const t=j/sr, e=Math.exp(-t/dk)*(t<0.0005?t/0.0005:1); let v=(Math.random()*2-1)*Math.exp(-t/0.004)*1.6; fs.forEach((f,q)=>v+=Math.sin(TAU*f*t+q)*(0.55-q*0.12)); L[s0+j]+=v*e*mv*0.45; R[s0+j]+=v*e*mv*0.45*(big?0.8:1); } }
  // drive it into a soft limit like a mic that's being pushed, then fade the very end so nothing clicks
  let m=1e-9; for(let i=0;i<n;i++) m=Math.max(m,Math.abs(L[i]),Math.abs(R[i])); const dr=o.drive*0.6, td=Math.tanh(dr); for(let i=0;i<n;i++){ L[i]=Math.tanh(L[i]/m*dr)/td; R[i]=Math.tanh(R[i]/m*dr)/td; } m=1;
  const buf=AC.createBuffer(2,n,sr), cl=buf.getChannelData(0), cr=buf.getChannelData(1), fade=Math.floor(sr*0.05);
  for(let i=0;i<n;i++){ const f=i>n-fade?(n-i)/fade:1; cl[i]=L[i]/m*0.95*f; cr[i]=R[i]/m*0.95*f; }
  return buf; }
function playGun(k){ const o=GUN_SND[k]; let t=gunTakes[k]||(gunTakes[k]=[]);
  try{ if(t.length<4&&(t.length===0||Math.random()<0.5)) t.push(renderGun(o)); }catch(e){ return false; } if(!t.length) return false;
  const s=AC.createBufferSource(), g=AC.createGain(); s.buffer=t[Math.floor(Math.random()*t.length)]; s.playbackRate.value=0.96+Math.random()*0.08; g.gain.value=o.vol;
  s.connect(g).connect(cur); s.start(); return true; }
function sfx(k){
  if(!AC) return;""")
rep("  cur=bus();\n  const r=()=>0.94+Math.random()*0.12;","  cur=bus();\n  if(GUN_SND[k]&&playGun(k)) return;\n  const r=()=>0.94+Math.random()*0.12;")
# render two takes of every gun in the background once sound starts, so the first shot of a gun never hitches
rep("    verb.buffer=ir; const vg=AC.createGain(); vg.gain.value=0.5; verb.connect(vg); vg.connect(comp);","    verb.buffer=ir; const vg=AC.createGain(); vg.gain.value=0.5; verb.connect(vg); vg.connect(comp);\n    const warm=Object.keys(GUN_SND).flatMap(k=>[k,k]); const step=()=>{ const k=warm.shift(); if(!k) return; try{ const t=gunTakes[k]||(gunTakes[k]=[]); if(t.length<2) t.push(renderGun(GUN_SND[k])); }catch(e){} setTimeout(step,60); }; setTimeout(step,500);")
