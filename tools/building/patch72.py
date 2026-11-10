# ---------- 72. the glider itself pitches with the flight: nose down into a dive, nose up as it climbs (it used to stay level) ----------
rep("gd.rotation.set(-th-0.02-(1-e)*0.5+Math.sin(t*1.3)*0.025*e,0,-A.skyZ*0.25); } }",
    "A.glP=lerp(A.glP||0,gl?Math.max(-0.95,Math.min(0.45,0.1+gam*0.95)):0,Math.min(1,dt*4)); gd.rotation.set(A.glP-th-0.02-(1-e)*0.5+Math.sin(t*1.3)*0.025*e,0,-A.skyZ*0.25); } }")
