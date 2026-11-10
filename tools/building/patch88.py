# ---------- 88. no brown wedges at road bends and town entrances: the ground right under a road is asphalt-coloured, so
# wherever the road surface doesn't quite cover it you see road, not bare dirt (the worn dirt shoulder beside it stays) ----------
rep("    vec3 dirt=vec3(0.52,0.43,0.31)*(0.7+0.55*rk.g);","    vec3 dirt=mix(vec3(0.52,0.43,0.31)*(0.7+0.55*rk.g),vec3(0.255,0.262,0.278),smoothstep(0.55,0.95,vCover.z));")
rep("    diffuseColor.rgb=mix(diffuseColor.rgb,dirt,clamp(vCover.z,0.0,1.0));","    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.255,0.262,0.278),smoothstep(0.5,0.9,vCover.z)); // (no brown shoulder: it showed as wedges where roads meet sidewalks)")
