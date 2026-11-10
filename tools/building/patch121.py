# ---------- 121. water has a sound: surf that swells and hisses with the waves on the beach, a brook's babble by the
# rivers and streams, and splashing footsteps when you wade ----------
rep("  amb.t+=dt; const on=playing&&!document.hidden, hi=Math.max(0,Math.min(1,(P.pos.y-terrainH(P.pos.x,P.pos.z)+P.pos.y*0.15)/60));",
    """  amb.t+=dt; const on=playing&&!document.hidden, hi=Math.max(0,Math.min(1,(P.pos.y-terrainH(P.pos.x,P.pos.z)+P.pos.y*0.15)/60));
  // water: how far the sea and the nearest running water are is looked up a few times a second
  if(!amb.sea){ const mk=(type,freq,q)=>{ const s=AC.createBufferSource(); s.buffer=noiseBuf; s.loop=true; s.playbackRate.value=0.7+Math.random()*0.5; const f=AC.createBiquadFilter(); f.type=type; f.frequency.value=freq; f.Q.value=q; const g=AC.createGain(); g.gain.value=0; s.connect(f).connect(g).connect(master); s.start(0,Math.random()*0.3); return {f,g}; };
    amb.sea=mk('lowpass',520,0.5); amb.hiss=mk('highpass',2600,0.5); amb.riv=mk('bandpass',1500,0.9); amb.riv2=mk('bandpass',3200,1.2); amb.wT=0; amb.dSea=1e9; amb.dRiv=1e9; }
  amb.wT-=dt; if(amb.wT<=0){ amb.wT=0.3; const SEA_=WGEN.sea(), px=P.pos.x, pz=P.pos.z; let ds=1e9, dr=1e9;
    for(const R of [0,6,14,26,42,62,86]) for(let q=0;q<(R?8:1);q++){ const a=q*Math.PI/4+R, w=waterAt(px+Math.cos(a)*R,pz+Math.sin(a)*R); if(w>-999){ if(SEA_&&Math.abs(w-SEA_.Y)<0.3){ if(R<ds) ds=R; } else if(R<dr) dr=R; } }
    amb.dSea=ds; amb.dRiv=dr; }
  { const now=AC.currentTime, k01=x=>Math.max(0,Math.min(1,x)), up=P.sky?0.25:1, wt=typeof WATER!=='undefined'&&WATER&&WATER.mat?WATER.mat.uniforms.time.value:amb.t, swell=0.5+0.5*Math.sin(wt*0.9+1.2); // the surf comes in with the wave you can see
    const ks=on?Math.pow(k01(1-amb.dSea/95),1.6)*up:0, kh=on?Math.pow(k01(1-amb.dSea/40),2)*up:0, kr=on?Math.pow(k01(1-amb.dRiv/30),2)*up:0;
    amb.sea.g.gain.setTargetAtTime((0.02+0.05*swell)*ks,now,0.5); amb.sea.f.frequency.setTargetAtTime(380+420*swell,now,0.6); amb.hiss.g.gain.setTargetAtTime(0.024*swell*swell*swell*kh,now,0.35);
    amb.riv.g.gain.setTargetAtTime(0.034*kr*(0.75+0.25*Math.sin(amb.t*5.3)*Math.sin(amb.t*1.7)),now,0.12); amb.riv2.g.gain.setTargetAtTime(0.012*kr*(0.6+0.4*Math.sin(amb.t*8.1+1)),now,0.1); }""")
rep("function stepSound(E){\n  if(E.groundSlab) return 'step_'+(E.groundSlab.mat||'wood');","function stepSound(E){\n  if(E.groundSlab) return 'step_'+(E.groundSlab.mat||'wood');\n  { const w=waterAt(E.pos.x,E.pos.z); if(w>-999&&w>terrainH(E.pos.x,E.pos.z)+0.03&&E.pos.y<w+0.3) return 'step_water'; } // wading")
rep("    case 'step_dirt':","    case 'step_water': noise(700*r(),0.16,0.09,0.7,0,'lowpass',260); noise(3200*r(),0.09,0.035,1,0.02,'highpass'); for(let q=0;q<2;q++) tone('sine',500+Math.random()*500,300,0.05,0.012,0.04+q*0.05); break; // a splash\n    case 'step_dirt':")
