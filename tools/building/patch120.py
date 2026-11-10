# ---------- 120. emotes and their songs, redone for the new bodies. Each dance has its own four-bar song (drums, a bass
# line, chords and a tune, sequenced in sixteenths) and is danced with the whole body: weight goes from foot to foot,
# the feet stay on the floor, hips, ribs and shoulders move against each other, and the hands take part ----------
rep("const EMOTES={wave:{name:'Wave',dur:2.6,rarity:'common'},dance:{name:'Groove',dur:12,beat:1.9,rarity:'uncommon'},cheer:{name:'Cheer',dur:2.4,rarity:'common'},salute:{name:'Salute',dur:2.2,rarity:'common'},\n  floss:{name:'Floss',dur:10,beat:2.2,rarity:'rare',shop:1},robot:{name:'Robot',dur:10,beat:2.2,rarity:'uncommon',shop:1},hype:{name:'Hype',dur:8,beat:2.1,rarity:'uncommon',shop:1},\n  disco:{name:'Disco Fever',dur:10,beat:2,rarity:'epic',shop:1},shuffle:{name:'Shuffle',dur:10,beat:2,rarity:'rare',shop:1}};",
    "const EMOTES={wave:{name:'Wave',dur:2.8,rarity:'common'},dance:{name:'Groove',dur:16.8,beat:1.9,rarity:'uncommon'},cheer:{name:'Cheer',dur:2.7,rarity:'common'},salute:{name:'Salute',dur:2.4,rarity:'common'},\n  floss:{name:'Floss',dur:14.5,beat:2.2,rarity:'rare',shop:1},robot:{name:'Robot',dur:14.5,beat:2.2,rarity:'uncommon',shop:1},hype:{name:'Hype',dur:15.2,beat:2.1,rarity:'uncommon',shop:1},\n  disco:{name:'Disco Fever',dur:16,beat:2,rarity:'epic',shop:1},shuffle:{name:'Shuffle',dur:16,beat:2,rarity:'rare',shop:1}}; // each dance lasts eight bars of its song")

# --- the songs
a=s.index("const GROOVE={ // per beat: kick pattern, snare pattern, hats per beat, bass notes (Hz), lead notes"); b=s.index("let _gId='dance', _gB=0;",a)
s=s[:a]+r"""/* The songs, one per dance, each a four-bar loop in sixteenths. Drums are strings (x a hit, c a clap, o an open hat,
   r a roll); bass, chords and tune are MIDI notes (0 a rest). Groove is funk in E minor, Floss bubblegum pop in C,
   Robot electro in F minor, Hype half-time with a sliding sub bass, Disco Fever four-on-the-floor with octave bass
   and strings, Shuffle swung house with organ stabs. */
const SONGS={
  dance:{k:['x.....x...x.....','x.....x..x.x....'],s:['....x.......x...','....x..x....x...'],h:['x.x.x.x.x.x.x.xo'],
    bass:{w:'triangle',v:.2,len:1.5,n:[[40,0,0,52,0,0,43,0,45,0,47,0,50,0,52,0],[40,0,0,52,0,0,43,0,45,0,43,0,40,0,38,0],[45,0,0,57,0,0,48,0,50,0,52,0,55,0,57,0],[47,0,0,59,0,0,47,0,45,0,47,0,43,0,42,0]]},
    chord:{w:'sawtooth',v:.018,len:.08,r:['..x..x....x..x..'],c:[[64,67,71,74],[64,67,71,74],[61,64,67,69],[63,66,69,71]]},
    lead:{w:'square',v:.024,len:.1,n:[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,76,0,74,0,71,0,74,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[79,0,76,0,74,0,71,0,69,0,71,0,67,0,64,0]]}},
  floss:{k:['x...x...x...x...'],s:['....c.......c...'],h:['..x...x...x...x.'],
    bass:{w:'triangle',v:.2,len:1.5,n:[[36,0,36,0,36,0,36,0,36,0,36,0,43,0,36,0],[43,0,43,0,43,0,43,0,43,0,43,0,50,0,43,0],[45,0,45,0,45,0,45,0,45,0,45,0,52,0,45,0],[41,0,41,0,41,0,41,0,41,0,43,0,45,0,47,0]]},
    chord:{w:'triangle',v:.03,len:.12,r:['x..x..x.x..x..x.'],c:[[60,64,67],[59,62,67],[60,64,69],[60,65,69]]},
    lead:{w:'square',v:.026,len:.13,echo:1,n:[[76,0,76,0,79,0,76,0,72,0,74,0,76,0,0,0],[74,0,74,0,79,0,74,0,71,0,72,0,74,0,0,0],[72,0,72,0,76,0,72,0,69,0,71,0,72,0,0,0],[77,0,76,0,74,0,72,0,74,0,0,0,79,0,0,0]]}},
  robot:{k:['x.....x.x.......','x.....x.x.....x.'],s:['....x.......x...'],h:['x.xxx.xxx.xxx.xx'],
    bass:{w:'square',v:.055,len:.9,n:[[29,0,41,0,29,0,41,0,29,0,41,0,29,41,29,41],[29,0,41,0,29,0,41,0,29,0,41,0,29,41,29,41],[25,0,37,0,25,0,37,0,25,0,37,0,25,37,25,37],[27,0,39,0,27,0,39,0,27,0,39,0,27,39,27,39]]},
    chord:{w:'square',v:.016,len:.07,r:['x..x..x.....x...'],c:[[65,68,72],[65,68,72],[65,68,73],[63,67,70]]},
    lead:{w:'square',v:.026,len:.09,zap:1,n:[[77,0,0,84,0,0,80,0,0,0,89,0,0,84,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[73,0,0,80,0,0,77,0,0,0,85,0,0,80,0,0],[75,0,79,0,82,0,87,0,91,0,87,0,82,0,79,0]]}},
  hype:{sub:1,k:['x.........x..x..','x.....x...x.....'],s:['........c.......'],h:['x.x.x.r.x.x.xrx.','x.x.r.x.x.r.x.rr'],
    bass:{w:'sine',v:.26,len:3,n:[[38,0,0,0,0,0,0,0,0,0,38,0,0,41,0,0],[38,0,0,0,0,0,36,0,0,0,33,0,0,0,0,0],[34,0,0,0,0,0,0,0,0,0,34,0,0,38,0,0],[36,0,0,0,0,0,36,0,0,0,40,0,0,0,43,0]]},
    chord:{w:'sawtooth',v:.024,len:.14,r:['x.....x.....x...','....x.....x.....'],c:[[62,65,69],[62,65,69],[58,62,65],[60,64,67]]},
    lead:{w:'sine',v:.04,len:.22,n:[[86,0,0,0,0,0,81,0,0,0,0,0,84,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[82,0,0,0,0,0,77,0,0,0,0,0,81,0,0,0],[84,0,0,0,0,0,0,0,88,0,0,0,91,0,0,0]]}},
  disco:{k:['x...x...x...x...'],s:['....x.......x...'],h:['x.o.x.o.x.o.x.o.'],
    bass:{w:'triangle',v:.19,len:1.1,n:[[35,0,47,0,35,0,47,0,35,0,47,0,35,47,35,47],[40,0,52,0,40,0,52,0,40,0,52,0,40,52,40,52],[33,0,45,0,33,0,45,0,33,0,45,0,33,45,33,45],[42,0,54,0,42,0,54,0,42,0,54,0,42,54,44,46]]},
    chord:{w:'sawtooth',v:.012,len:.08,pad:1,r:['p...x..x..x...x.'],c:[[62,66,69,74],[62,64,68,71],[61,64,69,73],[61,64,66,69]]},
    lead:{w:'triangle',v:.045,len:.17,echo:1,n:[[78,0,0,0,81,0,83,0,0,0,81,0,78,0,0,0],[76,0,0,0,80,0,83,0,0,0,80,0,76,0,0,0],[73,0,0,0,76,0,81,0,0,0,85,0,83,0,81,0],[78,0,0,0,0,0,73,0,76,0,0,0,78,0,0,0]]}},
  shuffle:{swing:.34,k:['x...x...x...x...'],s:['....c.......c...'],h:['..x..xx...x..xx.'],
    bass:{w:'triangle',v:.2,len:1.3,n:[[0,0,43,0,0,0,43,0,0,0,43,0,0,43,46,0],[0,0,39,0,0,0,39,0,0,0,39,0,0,39,41,0],[0,0,41,0,0,0,41,0,0,0,41,0,0,41,45,0],[0,0,38,0,0,0,38,0,0,0,38,0,0,38,42,0]]},
    chord:{w:'triangle',v:.03,len:.1,r:['..x..x.x..x..x.x'],c:[[62,65,67,70],[62,63,67,70],[60,65,69,72],[60,62,65,69]]},
    lead:{w:'sawtooth',v:.018,len:.12,n:[[0,0,0,0,0,0,0,0,74,0,77,0,79,0,0,0],[82,0,0,79,0,0,77,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,72,0,77,0,81,0,0,0],[84,0,0,81,0,0,77,0,74,0,0,0,0,0,0,0]]}} };
const M2F=n=>440*Math.pow(2,(n-69)/12);
// one beat of a song: its four sixteenths, each scheduled a little later
function songBeat(id,b){ const S=SONGS[id]||SONGS.dance, bd=1/((EMOTES[id]||{}).beat||2), sx=bd/4, bar=Math.floor(b/4), q=((b%4)+4)%4, at=(a)=>a[bar%a.length];
  for(let st=0;st<4;st++){ const i=q*4+st, d=st*sx+(S.swing&&st%2?sx*S.swing:0), K=at(S.k)[i], N=at(S.s)[i], H=at(S.h)[i];
    if(K==='x'){ if(S.sub){ tone('sine',150,40,0.3,0.26,d); } else tone('sine',125,44,0.17,0.24,d); noise(3000,0.012,0.05,1,d,'highpass'); }
    if(N==='x'){ noise(1900,0.13,0.15,0.8,d); tone('triangle',200,150,0.06,0.07,d); } else if(N==='c'){ noise(1500,0.04,0.1,1.5,d); noise(1300,0.05,0.12,1.5,d+0.012); noise(1300,0.09,0.1,1.5,d+0.026); }
    if(H==='x') noise(8000,0.025,0.03,1,d,'highpass'); else if(H==='o') noise(7500,0.1,0.038,1,d,'highpass'); else if(H==='r'){ for(let k=0;k<3;k++) noise(8500,0.018,0.024,1,d+k*sx/3,'highpass'); }
    const B=S.bass, bn=at(B.n)[i]; if(bn){ const f=M2F(bn); tone(B.w,f,S.sub?f*0.94:f*0.995,sx*B.len,B.v,d); if(B.w==='triangle') tone('sine',f,f,sx*B.len*0.7,B.v*0.5,d); }
    const C=S.chord, cr=C&&at(C.r)[i]; if(cr==='x'||cr==='p'){ for(const n of at(C.c)){ const f=M2F(n); if(cr==='p'){ tone('sawtooth',f,f,bd*3.6,C.v*0.9,d); tone('sawtooth',f*1.005,f*1.005,bd*3.6,C.v*0.7,d); } else tone(C.w,f,f,C.len,C.v,d); } }
    const L=S.lead, ln=L&&at(L.n)[i]; if(ln){ const f=M2F(ln); tone(L.w,f,L.zap?f*0.5:f,L.len,L.v,d); if(!L.zap) tone(L.w,f*1.006,f*1.006,L.len,L.v*0.55,d); if(L.echo) tone(L.w,f,f,L.len,L.v*0.3,d+sx*3); } } }
"""+s[b:]
a=s.index("    case 'groove': { const G=GROOVE[_gId]||GROOVE.dance,"); b=s.index("    case 'beat_kick':",a)
s=s[:a]+"    case 'groove': songBeat(_gId,_gB); break;\n"+s[b:]

# --- the dances
a=s.index("  if(emo){ const t=emo.t, id=emo.id;\n    if(id==='wave'){"); b=s.index("  // ----- upper body by activity -----",a)
s=s[:a]+r"""  A.handL=A.handR=null; A.turnL=A.turnR=null;
  if(emo){ const t=emo.t, id=emo.id, E=EMOTES[id], bt=t*(E.beat||2), TAU=Math.PI*2, cl=x=>Math.max(0,Math.min(1,x)), ez=x=>x*x*(3-2*x), K=ez(cl(t*3.5))*ez(cl((E.dur-t)*3)); // K eases the emote in and out
    // hit(): step through key poses one a beat, arriving early and holding; pose(): arms are set, the body is added to
    const hit=(rows,x,snap=0.5)=>{ const n=rows.length, fl=Math.floor(x), i=((fl%n)+n)%n, f=ez(cl((x-fl)/snap)), a=rows[(i+n-1)%n], b=rows[i], o={}; for(const k in b) o[k]=(a[k]||0)+(b[k]-(a[k]||0))*f; return o; };
    const ARM=['shL','shR','shLz','shRz','shLy','shRy','elL','elR','wrL','wrR','wrLy','wrRy','wrLz','wrRz'], BODY=['hipsX','hipsY','hipsZ','hipX','spX','spY','spZ','chX','chY','chZ','nkX','nkY','nkZ','hpL','hpR','hpLz','hpRz','hpLy','hpRy','knL','knR'];
    const pose=p=>{ for(const k of ARM) if(p[k]!==undefined) T[k]=lerp(T[k]||0,p[k],K); for(const k of BODY) if(p[k]!==undefined) T[k]=(T[k]||0)+p[k]*K; };
    // plant(): the standing leg sets how high the hips are, and both soles stay flat
    const plant=()=>{ const ext=(h,k,z)=>(0.4*Math.cos(h)+0.37*Math.cos(h+k))*Math.cos(z)+0.13; T.hipY=Math.max(ext(T.hpL,T.knL,T.hpLz),ext(T.hpR,T.knR,T.hpRz))+0.041+(T.hop||0); T.anL=-(T.hpL+T.knL); T.anR=-(T.hpR+T.knR); };
    const dip=0.5+0.5*Math.cos(TAU*bt), sw2=Math.sin(Math.PI*bt), sw4=Math.sin(Math.PI*bt/2); // down on every beat; side to side over two beats, and over four
    A.handL=A.handR='relax';
    if(id==='wave'){ const w=Math.sin(t*8.5); // the forearm upright beside the head, palm out, rocking at the elbow and wrist; the head tips towards it
      pose({shR:0.2,shRz:1.3,shRy:-1.5,elR:1.7+0.3*w,wrRy:1.45,wrRz:0.2*w,chZ:-0.05,spZ:-0.04,nkZ:0.1,nkY:0.15,hipsZ:0.03}); A.handR='flat'; A.turnR=0; }
    else if(id==='cheer'){ const b=t*TAU*2.2, s=Math.sin(b), j=Math.max(0,Math.sin(b*0.5)); // fists pumping overhead, bouncing off the knees
      pose({shL:2.45+0.4*s,shR:2.45-0.4*s,shLz:-0.4,shRz:0.4,elL:0.95-0.85*Math.max(0,s),elR:0.95-0.85*Math.max(0,-s),nkX:-0.22,chX:-0.08,knL:-0.35*(1-j),knR:-0.35*(1-j),hpL:0.17*(1-j),hpR:0.17*(1-j)});
      T.hop=0.07*j*K; plant(); A.handL=A.handR='fist'; A.turnL=A.turnR=0; }
    else if(id==='salute'){ const up=ez(cl(t*4))*ez(cl((E.dur-t)*5)); // standing straight, the flat hand to the brow, then snapped down
      T.shR=lerp(T.shR,1.95,up); T.shRz=lerp(T.shRz,0.8,up); T.elR=lerp(T.elR,2.45,up); T.shL=lerp(T.shL,0,up); T.shLz=lerp(T.shLz,-0.04,up); T.elL=lerp(T.elL,0.06,up); T.chX-=0.07*up; T.spX-=0.03*up; T.nkX-=0.04*up; A.handR='flat'; }
    else if(id==='dance'){ const W=sw4; // a two-step: the weight rocks from foot to foot over four beats, the free foot taps in, the arms swing across, fingers snap on two and four
      pose({hipX:0.06*W,hipsZ:0.09*W,spZ:-0.05*W,chZ:-0.05*W,chY:0.2*W,hipsY:-0.1*W,nkZ:0.05*W,nkX:0.07*dip-0.03,
        knL:-0.22*dip-0.3*Math.max(0,W)*(1-dip),knR:-0.22*dip-0.3*Math.max(0,-W)*(1-dip),hpL:0.1*dip+0.16*Math.max(0,W)*(1-dip),hpR:0.1*dip+0.16*Math.max(0,-W)*(1-dip),hpLz:-0.06-0.05*Math.max(0,-W),hpRz:0.06+0.05*Math.max(0,W),
        shL:0.35+0.45*W,shR:0.35-0.45*W,shLz:-0.28,shRz:0.28,shLy:-0.35,shRy:0.35,elL:1.3+0.3*dip,elR:1.3+0.3*dip}); plant(); A.handL=A.handR=(Math.floor(bt)%2?'fist':'relax'); }
    else if(id==='floss'){ const b=t*TAU*1.6, s=Math.sin(b), q=Math.sin(b*2); // straight arms swing to one side, one in front of the body and one behind, as the hips swing the other way
      pose({shL:0.7*s,shR:-0.7*s,shLz:-0.25+0.75*s,shRz:0.25+0.75*s,elL:0.1,elR:0.1,hipX:-0.05*s,hipsZ:-0.14*s,hipsY:0.1*q,chZ:0.07*s,spZ:0.05*s,knL:-0.12-0.14*Math.max(0,s),knR:-0.12-0.14*Math.max(0,-s),hpL:0.06+0.07*Math.max(0,s),hpR:0.06+0.07*Math.max(0,-s),nkZ:-0.06*s});
      plant(); A.handL=A.handR='fist'; }
    else if(id==='robot'){ const x=t*2.2, f=x-Math.floor(x), wob=Math.exp(-9*f)*Math.sin(f*46)*0.035, n=Math.floor(x); // right angles, snapped to on the beat and held, with a shudder as each one stops
      const R_=[{shL:1.57,shR:1.57,shLz:-0.1,shRz:0.1,elL:1.57,elR:0.05,nkY:0.55,chY:0.18,spZ:0,hipsY:0},{shL:1.57,shR:1.57,shLz:-0.1,shRz:0.1,elL:0.05,elR:1.57,nkY:-0.55,chY:-0.18,spZ:0,hipsY:0},
        {shL:0,shR:0,shLz:-1.5,shRz:1.5,elL:1.5,elR:1.5,nkY:0,chY:0,spZ:0.1,hipsY:0.15},{shL:0,shR:0,shLz:-1.5,shRz:1.5,elL:0.05,elR:1.5,nkY:0.5,chY:0,spZ:-0.1,hipsY:-0.15},
        {shL:0.25,shR:1.57,shLz:-0.15,shRz:0.1,elL:1.57,elR:1.57,nkY:-0.5,chY:-0.22,spZ:0,hipsY:0},{shL:1.57,shR:0.25,shLz:-0.1,shRz:0.15,elL:1.57,elR:1.57,nkY:0.5,chY:0.22,spZ:0,hipsY:0},
        {shL:2.6,shR:0.1,shLz:-0.2,shRz:0.5,elL:0.1,elR:1.57,nkY:0,chY:0,spZ:0.08,hipsY:0},{shL:1.57,shR:1.57,shLz:-0.1,shRz:0.1,elL:1.57,elR:1.57,nkY:0,chY:0,spZ:0,hipsY:0}], p=hit(R_,x,0.22);
      p.shL+=wob; p.shR-=wob; p.elL+=wob; p.elR-=wob; p.nkX=wob*0.8; p.knL=-0.14*(n%2); p.knR=-0.14*((n+1)%2); pose(p); plant(); A.handL=A.handR='flat'; A.turnL=A.turnR=0; }
    else if(id==='hype'){ const s=Math.sin(Math.PI*bt), roof=Math.floor(bt/8)%2, p1=Math.max(0,s), p2=Math.max(0,-s), pu=0.5-0.5*Math.cos(TAU*bt); // bouncing: fists punched up in turn, then both palms pushing the roof up
      if(!roof) pose({shR:1.1+1.8*p1,elR:1.6-1.4*p1,shL:1.1+1.8*p2,elL:1.6-1.4*p2,shLz:-0.3,shRz:0.3,chY:0.18*s,nkX:0.08*dip});
      else pose({shL:2.2+0.5*pu,shR:2.2+0.5*pu,shLz:-0.45,shRz:0.45,elL:1.5-1.2*pu,elR:1.5-1.2*pu,nkX:-0.15,chX:-0.06});
      pose({knL:-0.5*dip,knR:-0.5*dip,hpL:0.24*dip,hpR:0.24*dip,chX:0.05*dip,hpLz:-0.07,hpRz:0.07}); T.hop=0.05*Math.max(0,Math.sin(TAU*bt-1.2))*K; plant(); A.handL=A.handR=roof?'flat':'fist'; A.turnL=A.turnR=0; }
    else if(id==='disco'){ const up=Math.floor(bt/2)%2===0, roll=Math.floor(bt/8)%2, g=ez(cl(((bt/2)%1)/0.3)), k2=up?g:1-g; // a finger pointed to the sky then down across the body, the other hand on the hip; then the forearms rolled round each other
      if(!roll){ pose({shR:lerp(0.5,2.65,k2),shRz:lerp(-0.7,0.6,k2),elR:0.1,shL:-0.25,shLz:-0.6,shLy:-0.9,elL:1.75,nkY:lerp(0.3,-0.3,k2),nkX:lerp(0.18,-0.22,k2),chY:lerp(0.25,-0.2,k2),chZ:lerp(0.06,-0.08,k2),hipsZ:lerp(0.1,-0.12,k2),hipX:lerp(-0.04,0.05,k2)}); A.handR='point'; A.handL='fist'; }
      else { const a=bt*TAU; pose({shL:1.25+0.25*Math.sin(a),shR:1.25-0.25*Math.sin(a),shLz:-0.25,shRz:0.25,shLy:-0.9,shRy:0.9,elL:1.6+0.35*Math.cos(a),elR:1.6-0.35*Math.cos(a),hipsZ:0.1*sw2,hipX:0.04*sw2,chZ:-0.06*sw2,chY:0.15*sw4}); A.handL=A.handR='fist'; }
      pose({knL:-0.14*dip-0.22*Math.max(0,sw2)*(1-dip),knR:-0.14*dip-0.22*Math.max(0,-sw2)*(1-dip),hpL:0.07*dip+0.1*Math.max(0,sw2)*(1-dip),hpR:0.07*dip+0.1*Math.max(0,-sw2)*(1-dip)}); plant(); }
    else if(id==='shuffle'){ const s=sw2, c=Math.cos(Math.PI*bt), L=Math.max(0,s), R=Math.max(0,-s); // the running man: a knee comes up as the standing foot slides back, arms pumping against the legs
      pose({hpL:0.75*L-0.25*R,knL:-1.15*L-0.1,hpR:0.75*R-0.25*L,knR:-1.15*R-0.1,hipsY:0.2*s,chY:-0.3*s,chX:0.1,spX:0.05,shL:-0.55*s,shR:0.55*s,shLz:-0.18,shRz:0.18,elL:1.4,elR:1.4,nkX:-0.05});
      T.hop=0.035*Math.abs(c)*K; plant(); A.handL=A.handR='fist'; }
  }
"""+s[b:]

# --- more of the body can be moved: the pelvis sideways, a side bend, leg and arm twist, the wrists
rep("  r.hips.position.y=lerp(r.hips.position.y,T.hipY,smF);\n","  r.hips.position.y=lerp(r.hips.position.y,T.hipY,smF); r.hips.position.x=lerp(r.hips.position.x,T.hipX||0,smF);\n")
rep("  set(r.spine,'x',T.spX); set(r.spine,'y',T.spY);","  set(r.spine,'x',T.spX); set(r.spine,'y',T.spY); set(r.spine,'z',T.spZ||0);")
rep("  for(const [L,h,hz,kn,an] of [[r.legL,T.hpL,T.hpLz,T.knL,T.anL],[r.legR,T.hpR,T.hpRz,T.knR,T.anR]]){\n    set(L.hp,'x',h,smF); set(L.hp,'z',hz,smF);","  for(const [L,h,hz,kn,an,hy] of [[r.legL,T.hpL,T.hpLz,T.knL,T.anL,T.hpLy||0],[r.legR,T.hpR,T.hpRz,T.knR,T.anR,T.hpRy||0]]){\n    set(L.hp,'x',h,smF); set(L.hp,'z',hz,smF); set(L.hp,'y',hy,smF);")
rep("    set(r.armL.sh,'y',0); set(r.armR.sh,'y',0);","    set(r.armL.sh,'y',T.shLy||0); set(r.armR.sh,'y',T.shRy||0);")
rep("    set(r.armL.wr,'x',building?-0.5:0); set(r.armR.wr,'x',S.gun===false&&!building&&!S.editing?(T.wrR||0):0,fa); r.armL.wr.rotation.y=r.armL.wr.rotation.z=r.armR.wr.rotation.y=r.armR.wr.rotation.z=0;\n  }\n  // ----- weapons: two-handed IK -----",
    "    set(r.armL.wr,'x',building?-0.5:(T.wrL||0)); set(r.armR.wr,'x',(emo||S.gun===false)&&!building&&!S.editing?(T.wrR||0):0,fa);\n    if(emo){ set(r.armL.wr,'y',T.wrLy||0); set(r.armL.wr,'z',T.wrLz||0); set(r.armR.wr,'y',T.wrRy||0); set(r.armR.wr,'z',T.wrRz||0); } else r.armL.wr.rotation.y=r.armL.wr.rotation.z=r.armR.wr.rotation.y=r.armR.wr.rotation.z=0;\n  }\n  // ----- weapons: two-handed IK -----")

# --- hands in emotes; at rest the palms face the thighs
rep("wrap:[[1.25,1.3,.5],[1.25,1.3,.5],[.7,.22,.3,.35]],","wrap:[[1.25,1.3,.5],[1.25,1.3,.5],[.7,.22,.3,.35]],point:[[.04,.06,.04],[1.2,1.5,.9],[.9,.1,.45,.6]],")
rep("  set(r.armR,held?'pgrip':tool||mdl==='nade'?'fist':S.editing?'flat':'relax',held?Math.PI/2:0,0);",
    "  const A_=H.anim, rest=(nm,a,ov)=>ov!=null?ov:nm==='relax'?a.side*1.3:0, nR=A_.handR||(held?'pgrip':tool||mdl==='nade'?'fist':S.editing?'flat':'relax'); // an emote says what its hands do; loose hands hang palm-in\n  set(r.armR,nR,held?Math.PI/2:rest(nR,r.armR,A_.turnR),0);")
rep("const und=sp===undefined||sp===3; set(r.armL,held?(sp===0?'relax':sp===3?'fist':sp?'wrap':'cradle'):two?'fist':S.editing?'flat':'relax',held?(und?0.6:sp?-0.97:0):0,held&&und?1.35:0);",
    "const und=sp===undefined||sp===3, nL=A_.handL||(held?(sp===0?'relax':sp===3?'fist':sp?'wrap':'cradle'):two?'fist':S.editing?'flat':'relax'); set(r.armL,nL,held?(und?0.6:sp?-0.97:0):rest(nL,r.armL,A_.turnL),held&&und?1.35:0);")
