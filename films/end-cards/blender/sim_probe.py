import bpy, sys, json, math
params = json.loads(sys.argv[sys.argv.index("--")+1]) if "--" in sys.argv else {}
g = {"OUTRO_MODE": "live", "OUTRO_HERE": r"C:\Users\PC\Videos\WanderBuddy\marketing\outro\blender", "OUTRO_PARAMS": params, "__name__": "__outro__"}
exec(compile(open(r"C:\Users\PC\Videos\WanderBuddy\marketing\outro\blender\build_outro.py", encoding="utf-8").read(), "build_outro.py", "exec"), g)
b, homes = g["baked"], g["homes"]
sc = bpy.context.scene
rig = bpy.data.objects["AssetsRig"]
rz = {}
for f in (1,20,30,40,50,60,70,80,90,100,110,120,138):
    sc.frame_set(f); rz[f] = round(rig.location.z,2)
print("RIG z:", rz)
for n, rows in b.items():
    h = homes[n]
    print(n, "home", (round(h.x,2), round(h.z,2)))
    print("   dz:", [ (f, round(rows[f-1][0].z - h.z,2)) for f in (1,20,30,40,50,60,70,80,90,100,110,120,138)])
    print("   dx:", [ (f, round(rows[f-1][0].x - h.x,2)) for f in (1,20,30,40,50,60,70,80,90,100,110,120,138)])
    print("   rot:", [ (f, round(math.degrees(rows[f-1][1]),1)) for f in (1,20,30,40,50,60,70,80,90,100,110,120,138)])
