# ---------- 56. buggy riders sit with legs out along the footwell, boots on the floor pan instead of through it ----------
rep("T.hpL=T.hpR=1.45; T.hpLz=-0.12; T.hpRz=0.12; T.knL=T.knR=-1.3; T.anL=T.anR=-0.12;","T.hpL=T.hpR=1.5; T.hpLz=0.03; T.hpRz=-0.03; T.knL=T.knR=-0.25; T.anL=T.anR=-0.3;")
# the side pods and the lower cage rails stop short of the wheel wells, and the front hoop pulls in, so a tyre (even steered full lock) never cuts through them
rep("put('paint',rbox(0.2,0.25,1.26,0.08),sx*0.6,0.47,-0.1); put('white',rbox(0.205,0.05,1.0,0.02),sx*0.6,0.56,-0.12);","put('paint',rbox(0.2,0.25,0.84,0.08),sx*0.6,0.47,0); put('white',rbox(0.205,0.05,0.7,0.02),sx*0.6,0.56,0);")
rep("tube(C,V(sx*0.52,1.41,-0.3),V(sx*0.6,0.73,-0.72));","tube(C,V(sx*0.52,1.41,-0.3),V(sx*0.5,0.73,-0.72));")
rep("tube(C,V(sx*0.66,0.42,-0.78),V(sx*0.66,0.42,0.8)); tube(C,V(sx*0.63,0.73,-0.72),V(sx*0.62,0.73,0.42));","tube(C,V(sx*0.56,0.42,-0.5),V(sx*0.56,0.42,0.46)); tube(C,V(sx*0.5,0.73,-0.72),V(sx*0.62,0.73,0.42));")
rep("tube(C,V(sx*0.6,0.73,-0.72),V(sx*0.66,0.42,-0.78)); }","tube(C,V(sx*0.5,0.73,-0.72),V(sx*0.56,0.42,-0.5)); }")
rep("tube(C,V(-0.6,0.73,-0.72),V(0.6,0.73,-0.72));","tube(C,V(-0.5,0.73,-0.72),V(0.5,0.73,-0.72));")
# wheels track the ground under each one with more travel, so a tyre on a bump rides up instead of sinking in
rep("off=Math.max(-0.1,Math.min(0.1,k.wh[i]-p.y));","off=Math.max(-0.16,Math.min(0.2,k.wh[i]-p.y));")
