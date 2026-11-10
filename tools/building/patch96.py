# ---------- 96. every dance has its own groove: a drum pattern, a bass line and (for some) a lead, instead of the same kick/snare ----------
rep("  if(E.beat){ const b=Math.floor(e.t*E.beat); if(b!==e.beat){ e.beat=b; sfx(b%4===2?'beat_snare':'beat_kick'); } }","  if(E.beat){ const b=Math.floor(e.t*E.beat); if(b!==e.beat){ e.beat=b; emoteBeat(e.id,b); } }")
rep("if(bb!==S.beat){ S.beat=bb; if(AC) sfx(bb%4===2?'beat_snare':'beat_kick'); } }","if(bb!==S.beat){ S.beat=bb; if(AC) emoteBeat(st.emote.id,bb); } }")
rep("function startEmote(id){",r"""const GROOVE={ // per beat: kick pattern, snare pattern, hats per beat, bass notes (Hz), lead notes
  dance:  {k:[1,0,1,0],s:[0,1,0,1],hat:2,bw:'triangle',bass:[55,55,65.4,73.4,55,55,49,61.7],lead:null},
  floss:  {k:[1,1,1,1],s:[0,1,0,1],hat:2,bw:'triangle',bass:[82.4,82.4,98,110,82.4,82.4,73.4,98],lead:[659,784,880,784,659,587,659,784],lw:'square'},
  robot:  {k:[1,0,0,1],s:[0,0,1,0],hat:4,bw:'square',bass:[65.4,65.4,65.4,77.8,65.4,65.4,58.3,65.4],lead:[1047,0,1245,0,1047,1568,0,1245],lw:'square',zap:1},
  hype:   {k:[1,1,1,1],s:[0,1,0,1],hat:4,bw:'sawtooth',bass:[73.4,73.4,87.3,73.4,98,98,87.3,110],lead:null,clap:1},
  disco:  {k:[1,1,1,1],s:[0,1,0,1],hat:2,open:1,bw:'triangle',oct:1,bass:[61.7,61.7,73.4,82.4,92.5,92.5,82.4,73.4],lead:[740,0,880,988,0,880,740,0],lw:'triangle'},
  shuffle:{k:[1,0,1,1],s:[0,1,0,1],hat:3,sw:1,bw:'triangle',bass:[49,49,58.3,49,65.4,58.3,49,43.7],lead:[587,0,698,0,784,698,0,587],lw:'sawtooth'} };
let _gId='dance', _gB=0;
function emoteBeat(id,b){ _gId=id; _gB=b; sfx('groove'); }
function startEmote(id){""")
rep("    case 'beat_kick':",r"""    case 'groove': { const G=GROOVE[_gId]||GROOVE.dance, n=_gB, bd=1/((EMOTES[_gId]||{}).beat||2), hb=bd/2, L=G.bass.length;
      if(G.k[n%4]){ tone('sine',125,44,0.17,0.24); noise(3000,0.012,0.05,1,0,'highpass'); }
      if(G.s[n%4]){ noise(1900,0.13,0.15,0.8); tone('triangle',200,150,0.06,0.07); if(G.clap){ noise(1300,0.05,0.12,1.5,0.012); noise(1300,0.08,0.1,1.5,0.026); } }
      for(let i=0;i<G.hat;i++){ const d=G.sw&&i%3===1?bd*(i+0.35)/G.hat:bd*i/G.hat; noise(8000,G.open&&i===G.hat-1?0.09:0.025,G.open&&i===G.hat-1?0.045:0.035,1,d,'highpass'); }
      const f=G.bass[n%L]; tone(G.bw,f,f*0.995,hb*0.85,G.bw==='triangle'?0.2:0.07); if(G.oct) tone(G.bw,f*2,f*2,hb*0.6,0.13,hb); else if(n%2) tone(G.bw,f,f,hb*0.5,G.bw==='triangle'?0.13:0.05,hb);
      if(G.lead){ const l=G.lead[n%G.lead.length]; if(l){ tone(G.lw,l,G.zap?l*0.5:l,G.zap?0.09:0.12,0.03,G.sw?hb*1.3:hb); if(!G.zap) tone(G.lw,l*1.5,l*1.5,0.08,0.014,G.sw?hb*1.3:hb); } }
      break; }
    case 'beat_kick':""")
