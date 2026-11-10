# ---------- 39. a magical chest shimmer: scattered soft bell twinkles that never repeat, over a faint airy breath ----------
a=s.index("    case 'chest_hum': {"); b=s.index("    case 'chest_open':")
s=s[:a]+r"""    case 'chest_hum': { const t=AC.currentTime, out=AC.createGain(); out.gain.value=1; out.connect(cur);
      // a faint airy breath underneath (filtered noise swelling in and out)
      { const n=AC.createBufferSource(); n.buffer=noiseBuf; n.loop=true; const f=AC.createBiquadFilter(); f.type='bandpass'; f.frequency.value=2600+Math.random()*900; f.Q.value=3; const g=AC.createGain();
        g.gain.setValueAtTime(0.0001,t); g.gain.linearRampToValueAtTime(0.006,t+0.8); g.gain.linearRampToValueAtTime(0.0001,t+2.2); n.connect(f).connect(g).connect(out); n.start(t); n.stop(t+2.3); }
      // four to six soft bell notes from a major pentatonic scale, scattered in time and pitch, so it twinkles differently every time
      const scale=[1046.5,1174.7,1318.5,1568,1760,2093,2349.3,2637], k=4+(Math.random()*3|0);
      for(let q=0;q<k;q++){ const f=scale[Math.random()*scale.length|0], at=t+0.05+Math.random()*1.7, v=0.006+Math.random()*0.006;
        for(const [mul,amp,dec] of [[1,1,0.9],[2.76,0.25,0.35],[5.4,0.08,0.18]]){ const o=AC.createOscillator(), g=AC.createGain(); o.type='sine'; o.frequency.value=f*mul*(1+(Math.random()-.5)*0.004);
          g.gain.setValueAtTime(0.0001,at); g.gain.linearRampToValueAtTime(v*amp,at+0.012); g.gain.exponentialRampToValueAtTime(0.0001,at+dec); o.connect(g).connect(out); o.start(at); o.stop(at+dec+0.05); } }
      break; }
"""+s[b:]
rep("if(best&&chestHumT<=0){ chestHumT=2.1;","if(best&&chestHumT<=0){ chestHumT=1.6+Math.random()*1.4;")
