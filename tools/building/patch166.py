# patch166: the Locker and Item Shop stage shows only your own hero (party members stand in the lobby, not your
# Locker), and the pad under it is sized to fit inside the picture instead of running off both sides.
rep("""function stageSync(){ const S=_stage, L=stageLineup(), key=""","""function stageSync(){ const S=_stage, L=stageLineup().filter(x=>x.me), key=""")
rep("""  S.cam.position.set(0.2,1.2+wide*0.3,-5.1-wide*3.6); S.cam.lookAt(0,0.78,wide*0.5);""",
    """  S.cam.position.set(0.2,1.2+wide*0.3,-5.1-wide*3.6); S.cam.lookAt(0,0.78,wide*0.5);
  { const d=S.cam.position.length(), half=d*Math.tan(S.cam.fov*Math.PI/360)*S.cam.aspect, k=Math.max(0.55,Math.min(1,half*0.86/1.25)); // the pad's whole width, with a margin, fits the picture
    if(Math.abs(S.pad.scale.x-k)>1e-3){ S.pad.scale.set(k,1,k); S.ring.scale.setScalar(k); } }""")
rep("""  S.ring.scale.setScalar(L.length>1?1:1); }""","""  }""")
# no name tag over your hero in the Locker and Item Shop, and the room code chip only shows in a match (not over menus)
rep(""".plates{position:absolute;inset:0;pointer-events:none}""",""".plates{position:absolute;inset:0;pointer-events:none;display:none}""")
rep("""  $('hudRoom').hidden=!inRoom; if(inRoom) $('hudRoomV').textContent=net.code+' · '+count;""",
    """  $('hudRoom').hidden=!inRoom||!menu.hidden; if(inRoom) $('hudRoomV').textContent=net.code+' · '+count;""")
rep("""  $('pdLeave').hidden=!net.role; }""","""  $('pdLeave').hidden=!net.role; $('hudRoom').hidden=!net.role||!menu.hidden; }""")
rep("""function openMenu(){ ""","""function openMenu(){ $('hudRoom').hidden=true; """)
