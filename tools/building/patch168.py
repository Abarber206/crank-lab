# patch168: six new emotes, each dance with its own song, eight bars long.
#  - Twist (uncommon): hips and heels twist one way while the shoulders go the other, sinking low and back up.
#  - Charleston (epic): kick forward, step, kick back, step with jazz hands; then the knees swing in and out while the
#    hands cross over them.
#  - Air Guitar (rare): wide stance, fretting hand out, strumming hand at the hip, head banging; a lean back and a
#    windmill strum at the end of each phrase.
#  - Arm Wave (rare): arms out to the sides, a wave rolls from one fingertip across the shoulders to the other, then back.
#  - Toprock (epic): break-dance cross steps, arms crossing and opening, with kicks.
#  - Flex (uncommon, short): double biceps, a single-arm flex, chest out.
rep("""  disco:{name:'Disco Fever',dur:16,beat:2,rarity:'epic',shop:1},shuffle:{name:'Shuffle',dur:16,beat:2,rarity:'rare',shop:1}};""",
    """  disco:{name:'Disco Fever',dur:16,beat:2,rarity:'epic',shop:1},shuffle:{name:'Shuffle',dur:16,beat:2,rarity:'rare',shop:1},
  twist:{name:'Twist',dur:12.3,beat:2.6,rarity:'uncommon',shop:1},charleston:{name:'Charleston',dur:14.5,beat:2.2,rarity:'epic',shop:1},
  guitar:{name:'Air Guitar',dur:13.3,beat:2.4,rarity:'rare',shop:1},armwave:{name:'Arm Wave',dur:17.8,beat:1.8,rarity:'rare',shop:1},
  toprock:{name:'Toprock',dur:16.8,beat:1.9,rarity:'epic',shop:1},flex:{name:'Flex',dur:3.6,rarity:'uncommon',shop:1}};""")

# songs
rep("""const M2F=n=>440*Math.pow(2,(n-69)/12);""","""Object.assign(SONGS,{
  twist:{swing:.3,k:['x.......x.......'],s:['....x.......x...'],h:['x.x.x.x.x.x.x.x.'],
    bass:{w:'triangle',v:.2,len:1.3,n:[[36,0,40,0,43,0,45,0,46,0,45,0,43,0,40,0],[36,0,40,0,43,0,45,0,46,0,45,0,43,0,40,0],[41,0,45,0,48,0,50,0,51,0,50,0,48,0,45,0],[43,0,47,0,50,0,52,0,53,0,52,0,50,0,47,0]]},
    chord:{w:'square',v:.015,len:.09,r:['..x...x...x...x.'],c:[[60,64,67,70],[60,64,67,70],[65,69,72,75],[67,71,74,77]]},
    lead:{w:'sawtooth',v:.02,len:.14,n:[[72,0,0,72,0,0,75,0,76,0,0,0,79,0,76,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[77,0,0,77,0,0,80,0,81,0,0,0,84,0,81,0],[79,0,79,0,77,0,76,0,74,0,72,0,71,0,0,0]]}},
  charleston:{swing:.45,k:['x...x...x...x...'],s:['....c.......c...'],h:['x.x.x.x.x.x.x.x.'],
    bass:{w:'triangle',v:.2,len:1.6,n:[[41,0,0,0,48,0,0,0,41,0,0,0,48,0,0,0],[46,0,0,0,41,0,0,0,46,0,0,0,41,0,0,0],[43,0,0,0,50,0,0,0,48,0,0,0,52,0,0,0],[41,0,0,0,45,0,0,0,48,0,0,0,40,0,0,0]]},
    chord:{w:'triangle',v:.03,len:.12,r:['....x.......x...','....x...x...x...'],c:[[57,60,65],[58,62,65],[58,62,67],[57,60,64]]},
    lead:{w:'square',v:.022,len:.13,echo:1,n:[[72,0,74,0,77,0,0,0,74,0,72,0,69,0,0,0],[70,0,0,0,74,0,77,0,82,0,0,0,77,0,0,0],[74,0,76,0,79,0,0,0,76,0,74,0,72,0,0,0],[77,0,0,76,0,0,74,0,72,0,0,0,0,0,0,0]]}},
  guitar:{k:['x.x...x.x.x.....','x.x...x.x...x.x.'],s:['....x.......x...'],h:['x.x.x.x.x.x.x.x.'],
    bass:{w:'sawtooth',v:.06,len:.8,n:[[28,28,28,28,28,28,28,28,31,31,31,31,33,33,33,33],[28,28,28,28,28,28,28,28,35,35,35,35,33,33,31,31],[28,28,28,28,28,28,28,28,31,31,31,31,33,33,33,33],[36,36,36,36,35,35,35,35,33,33,33,33,31,31,31,31]]},
    chord:{w:'sawtooth',v:.018,len:.11,r:['x.x.x.x.x.x.x.x.'],c:[[52,59,64],[52,59,64],[55,62,67],[57,64,69]]},
    lead:{w:'square',v:.026,len:.12,n:[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[76,0,79,0,81,0,79,0,76,0,74,0,76,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[83,0,81,0,79,0,81,0,79,0,76,0,74,0,76,0]]}},
  armwave:{k:['x.......x.......'],s:['....x.......x...'],h:['..x...x...x...x.'],
    bass:{w:'sawtooth',v:.05,len:.9,n:[[33,0,45,0,33,0,45,0,33,0,45,0,33,0,45,0],[29,0,41,0,29,0,41,0,29,0,41,0,29,0,41,0],[36,0,48,0,36,0,48,0,36,0,48,0,36,0,48,0],[31,0,43,0,31,0,43,0,31,0,43,0,31,0,43,0]]},
    chord:{w:'sawtooth',v:.012,len:.1,r:['p...............'],c:[[57,60,64,69],[53,57,60,65],[60,64,67,72],[55,59,62,67]]},
    lead:{w:'triangle',v:.045,len:.3,echo:1,n:[[76,0,0,0,0,0,0,0,74,0,0,0,72,0,0,0],[69,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[72,0,0,0,0,0,0,0,74,0,0,0,76,0,0,0],[79,0,0,0,0,0,0,0,74,0,0,0,0,0,0,0]]}},
  toprock:{swing:.2,k:['x.........x.x...','x.x.......x.....'],s:['....x.......x..x','....x.......x...'],h:['x.x.x.x.x.x.x.o.'],
    bass:{w:'triangle',v:.22,len:1.2,n:[[38,0,0,0,0,0,38,0,0,0,41,0,43,0,0,0],[36,0,0,0,0,0,36,0,0,0,38,0,41,0,0,0],[34,0,0,0,0,0,34,0,0,0,36,0,38,0,0,0],[33,0,0,0,0,0,33,0,0,0,36,0,37,0,0,0]]},
    chord:{w:'square',v:.02,len:.1,r:['x.....x...x.....','..........x.....'],c:[[62,65,69],[60,64,67],[58,62,65],[57,61,64]]},
    lead:{w:'square',v:.02,len:.08,zap:1,n:[[0,0,0,0,0,0,0,0,0,0,0,0,86,0,86,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,84,0,84,0],[0,0,0,0,0,0,0,0,86,0,84,0,81,0,79,0]]}} });
const M2F=n=>440*Math.pow(2,(n-69)/12);""")

# the moves
rep("""      T.hop=0.035*Math.abs(c)*K; plant(); A.handL=A.handR='fist'; }
  }""","""      T.hop=0.035*Math.abs(c)*K; plant(); A.handL=A.handR='fist'; }
    else if(id==='twist'){ const s=Math.sin(Math.PI*bt), low=0.5-0.5*Math.cos(TAU*bt/16); // hips and heels twist one way, the shoulders the other; over four bars sink low and come back up
      pose({hipsY:0.5*s,chY:-0.85*s,nkY:0.3*s,knL:-0.3-0.75*low,knR:-0.3-0.75*low,hpL:0.15+0.38*low,hpR:0.15+0.38*low,hpLz:-0.05,hpRz:0.05,
        shL:0.6-0.25*s,shR:0.6+0.25*s,shLz:-0.5,shRz:0.5,elL:1.45,elR:1.45,nkX:0.05*dip});
      plant(); A.handL=A.handR='fist'; }
    else if(id==='charleston'){ const knees=Math.floor(bt/8)%2; // four beats of kicks, then four of crossing hands over swinging knees
      if(!knees){ const p=hit([
          {hpR:1.15,knR:-0.05,hpL:0.0,knL:-0.2,shL:1.0,shR:-0.45,shLz:-0.45,shRz:0.55,elL:0.25,elR:0.25,chY:-0.15,hipsY:0.08},
          {hpL:0.1,knL:-0.3,hpR:0.1,knR:-0.3,shL:0.25,shR:0.25,shLz:-0.85,shRz:0.85,elL:0.55,elR:0.55,chY:0,hipsY:0},
          {hpL:-0.55,knL:-0.9,hpR:0.05,knR:-0.25,shR:1.0,shL:-0.45,shLz:-0.55,shRz:0.45,elL:0.25,elR:0.25,chY:0.15,hipsY:-0.08},
          {hpL:0.1,knL:-0.3,hpR:0.1,knR:-0.3,shL:0.25,shR:0.25,shLz:-0.85,shRz:0.85,elL:0.55,elR:0.55,chY:0,hipsY:0}],bt,0.35);
        p.wrL=0.45*Math.sin(t*22); p.wrR=-0.45*Math.sin(t*22); pose(p); A.handL=A.handR='flat'; A.turnL=A.turnR=0; }
      else { const q=Math.sin(Math.PI*bt), o=0.5-0.5*q; // q>0: knees together, hands crossed; q<0: knees apart, hands on their own knees
        pose({hpL:0.42,hpR:0.42,knL:-0.75,knR:-0.75,hpLz:-0.32*o+0.1*(1-o),hpRz:0.32*o-0.1*(1-o),spX:-0.38,chX:-0.14,nkX:0.34,
          shL:0.55,shR:0.55,shLz:-0.15*o+0.32*(1-o),shRz:0.15*o-0.32*(1-o),elL:0.25,elR:0.25}); A.handL=A.handR='flat'; A.turnL=A.turnR=0; }
      plant(); }
    else if(id==='guitar'){ const ph=Math.floor(bt/4)%4, wind=ph===3, lean=ph===2, st=Math.sin(TAU*bt*2); // fretting hand out, strumming at the hip, head banging on the beat
      pose({hpLz:-0.2,hpRz:0.2,hpL:0.2,hpR:0.2,knL:-0.42,knR:-0.42,nkX:lean?0.25-0.2*dip:0.12-0.45*dip,chX:lean?0.3:-0.08,spX:lean?0.12:-0.04,chY:0.25,hipsY:0.1,
        shL:1.05,shLz:-0.62,shLy:-0.5,elL:0.55,wrL:-0.3});
      if(wind){ const a=(bt%1)*TAU; T.shR=lerp(T.shR,0.25,K); T.shRz=lerp(T.shRz,0.35+a,K); T.elR=lerp(T.elR,0.15,K); } // a full windmill strum each beat
      else pose({shR:0.38,shRz:0.42,elR:1.45+0.32*st,wrR:0.35*st});
      plant(); A.handL='fist'; A.handR='point'; A.turnL=A.turnR=0; }
    else if(id==='armwave'){ const dir=Math.floor(bt/8)%2?-1:1, p=((bt%2)/2)*8-1, w=u=>{ const d=(dir>0?p:6-p)-u; return Math.exp(-d*d/0.55); }; // arms out; a wave rolls along them, fingertip to fingertip
      pose({shL:0,shR:0,shLz:-1.42-0.45*w(2),shRz:1.42+0.45*w(4),shLy:1.45,shRy:-1.45,elL:-0.05+0.95*w(1),elR:-0.05+0.95*w(5),wrL:0.9*w(0)-0.45*w(1),wrR:0.9*w(6)-0.45*w(5),
        chZ:0.17*(w(2)-w(4)),chX:0.12*w(3),nkZ:0.2*(w(2)-w(4)),nkX:-0.08*w(3),hipsZ:-0.05*(w(2)-w(4)),knL:-0.15*dip,knR:-0.15*dip,hpL:0.08*dip,hpR:0.08*dip});
      plant(); A.handL=A.handR='flat'; A.turnL=A.turnR=0; }
    else if(id==='toprock'){ const kick=Math.floor(bt/4)%4===3, R=[
        {hpR:0.3,hpRz:-0.48,knR:-0.32,hpL:0.05,hpLz:-0.06,knL:-0.3,hipsY:0.4,chY:-0.3,shL:0.95,shR:0.95,shLz:0.28,shRz:-0.28,elL:1.25,elR:1.25,nkX:-0.1,chX:-0.1},
        {hpLz:-0.15,hpRz:0.15,knL:-0.38,knR:-0.38,hpL:0.17,hpR:0.17,shL:0.45,shR:0.45,shLz:-1.1,shRz:1.1,elL:0.45,elR:0.45,chX:0.08,nkX:0.06},
        {hpL:0.3,hpLz:0.48,knL:-0.32,hpR:0.05,hpRz:0.06,knR:-0.3,hipsY:-0.4,chY:0.3,shL:0.95,shR:0.95,shLz:0.28,shRz:-0.28,elL:1.25,elR:1.25,nkX:-0.1,chX:-0.1},
        {hpLz:-0.15,hpRz:0.15,knL:-0.38,knR:-0.38,hpL:0.17,hpR:0.17,shL:0.45,shR:0.45,shLz:-1.1,shRz:1.1,elL:0.45,elR:0.45,chX:0.08,nkX:0.06}],
        KR=[{hpR:0.95,knR:-0.25,hpL:0.08,knL:-0.35,shL:0.3,shR:-0.3,shLz:-1.2,shRz:1.0,elL:0.3,elR:0.4,chX:-0.1,hipsY:0.1},R[1],{hpL:0.95,knL:-0.25,hpR:0.08,knR:-0.35,shR:0.3,shL:-0.3,shRz:1.2,shLz:-1.0,elL:0.4,elR:0.3,chX:-0.1,hipsY:-0.1},R[3]];
      pose(hit(kick?KR:R,bt,0.3)); T.hop=0.04*Math.max(0,Math.sin(TAU*bt+0.6))*K; plant(); A.handL=A.handR='fist'; }
    else if(id==='flex'){ const ph=t<1.25?0:t<2.45?1:2, pump=0.5+0.5*Math.sin(t*9); // double biceps, a single-arm flex with the other fist on the hip, then double biceps again, squeezing
      const D={shL:0.05,shR:0.05,shLz:-1.4,shRz:1.4,shLy:1.4,shRy:-1.4,elL:2.0,elR:2.0,chX:0.12,nkX:-0.08,hpLz:-0.12,hpRz:0.12,knL:-0.1,knR:-0.1,hpL:0.05,hpR:0.05};
      if(ph===1) pose(Object.assign({},D,{shL:-0.1,shLz:-0.8,shLy:-1.4,elL:1.75,chY:-0.25,chZ:0.06,nkY:0.45,nkZ:0.08}));
      else pose(Object.assign({},D,{elL:2.0+0.25*pump*(ph/2),elR:2.0+0.25*pump*(ph/2)}));
      plant(); A.handL=A.handR='fist'; A.turnL=A.turnR=0; }
  }""")

# icons
rep("""function emoteIcon(id){ const P={wave:[-40,150,0],""","""function emoteIcon(id){ const P={twist:[-70,-110,1],charleston:[-150,-30,1],guitar:[20,-20,0],armwave:[0,0,0],toprock:[-150,-150,1],flex:[-100,-80,0],wave:[-40,150,0],""")
# a long one-word name (Charleston) fits its card
rep("""    b.innerHTML=emoteIcon(e.id)+`<span>${e.name}<small>${e.rarity}</small></span>`; b.addEventListener('click',()=>pickEm(e.id)); ebox.appendChild(b); });""",
    """    b.innerHTML=emoteIcon(e.id)+`<span${/\\S{10,}/.test(e.name)?' class="lng"':''}>${e.name}<small>${e.rarity}</small></span>`; b.addEventListener('click',()=>pickEm(e.id)); ebox.appendChild(b); });""")
rep(""".wheelslots{""",""".ofit span.lng{font-size:11px;letter-spacing:0} .wslot span.lng{font-size:9.5px}
.wheelslots{""")
rep("""(id?emoteIcon(id)+`<span>${EMOTES[id].name}</span>""","""(id?emoteIcon(id)+`<span${/\\S{10,}/.test(EMOTES[id].name)?' class="lng"':''}>${EMOTES[id].name}</span>""")
