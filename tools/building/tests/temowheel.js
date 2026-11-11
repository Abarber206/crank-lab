// emote wheel: in the lobby (button, tap an emote: the hero dances on the pad); in a match, hold the Emote key, move the
// mouse toward an emote and let go: it plays; a quick tap plays the Locker emote; in the lobby the other tabs are solid.
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,LOBBY,EW,EMOTES,camera'),pre?{vp:{width:1100,height:620}}:{fast:true});
 await pg.waitForFunction(()=>window.T&&T.LOBBY&&T.LOBBY.on,null,{timeout:180000}); await sleep(3000); const out={};
 await pg.evaluate(()=>{ const L=window; }); 
 await pg.evaluate(()=>document.getElementById('lobbyEmote').click()); await sleep(600);
 out.lobbyWheel=await pg.evaluate(()=>({open:T.EW.open,n:document.querySelectorAll('#emoRing .sl').length}));
 if(pre) await pg.screenshot({path:pre+'_wheel.png',timeout:200000});
 await pg.evaluate(()=>document.querySelectorAll('#emoRing .sl')[2].click()); await sleep(1800);
 out.lobbyEmote=await pg.evaluate(()=>({em:T.LOBBY.emote&&T.LOBBY.emote.id,closed:!T.EW.open}));
 if(pre) await pg.screenshot({path:pre+'_dance.png',timeout:200000});
 await pg.evaluate(()=>document.querySelector('.mtabs button[data-tab=profile]').click()); await sleep(800);
 if(pre) await pg.screenshot({path:pre+'_profile.png',timeout:200000}); out.solid=await pg.evaluate(()=>getComputedStyle(document.getElementById('menu'),'::before').backgroundImage.slice(0,20));
 await pg.evaluate(()=>document.querySelector('.mtabs button[data-tab=play]').click()); await sleep(500);
 // into a match
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(2500);
 const key=await pg.evaluate(()=>{ const b=JSON.parse(localStorage.getItem('cranklab.binds')||'null'); return 'KeyB'; });
 // hold the key, move right (slice 1 is up-right of 8 / right of fewer), release
 out.state=await pg.evaluate(()=>({playing:T.P&&document.getElementById('menu').hidden,og:T.P.onGround,emo:T.P.emote,lob:T.LOBBY.on})); await pg.keyboard.down('KeyB'); await sleep(300); out.gameWheel=await pg.evaluate(()=>T.EW.open);
 await pg.evaluate(()=>{ for(let i=0;i<10;i++) window.dispatchEvent(new MouseEvent('mousemove',{movementX:12,movementY:0})); }); await sleep(100);
 const sel=await pg.evaluate(()=>({sel:T.EW.sel,id:T.EW.ids[T.EW.sel]})); await pg.keyboard.up('KeyB'); await sleep(300);
 out.picked=sel; out.playing=await pg.evaluate(()=>T.P.emote&&T.P.emote.id);
 await sleep(4000); await pg.evaluate(()=>{ T.P.emote=null; }); await pg.evaluate(()=>{ window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyB'})); window.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyB'})); }); await sleep(200);
 out.tap=await pg.evaluate(()=>[T.P.emote&&T.P.emote.id,T.settings.emote,T.EW.open]);
 console.log(JSON.stringify(out));
 const ok=out.lobbyWheel.open&&out.lobbyWheel.n>=4&&out.lobbyEmote.em&&out.lobbyEmote.closed&&/gradient/.test(out.solid)&&out.gameWheel&&out.picked.sel>=0&&out.playing===out.picked.id&&out.tap[0]===out.tap[1]&&!out.tap[2];
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();
