import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def r2(x): return jround(x*100)/100
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

OVERSPRAY=1.25; COVER=350; EFFECTIVE=250

def tip_plan(code):
    if not num(code) or code!=int(code) or code<100 or code>999: return {"error":"the tip code must be a three-digit number"}
    fan=int(code/100)*2
    thou=int(code)%100
    if thou<11: band="stains and lacquers"
    elif thou<15: band="thin paints and sealers"
    elif thou<=19: band="latex"
    else: band="heavy latex and elastomeric"
    return {"fan":fan,"thou":thou,"band":band}

def render_tip(r,code):
    return ("The "+jsnum(code)+" tip throws a fan "+jsnum(r["fan"])+" inches wide from an orifice of "
            +jsnum(r["thou"])+" thousandths - a tip that sprays "+r["band"]+".")

def coverage_plan(sqft,coats,bought):
    if not pos(sqft): return {"error":"the square footage must be above zero"}
    if not pos(coats): return {"error":"the coat count must be above zero"}
    if not pos(bought): return {"error":"the gallons bought must be above zero"}
    needed=sqft*coats*OVERSPRAY/COVER
    margin=bought/needed*100
    if margin>=100: verdict="the cans cover the job"
    elif margin>=85: verdict="close, but one more gallon earns its shelf"
    else: verdict="the cans run dry mid-wall"
    return {"needed":r2(needed),"margin":r1(margin),"verdict":verdict}

def render_coverage(r,sqft,coats,bought):
    word=" coat over " if coats==1 else " coats over "
    return ("At "+jsnum(coats)+word+jsnum(sqft)+" square feet, the overspray allowance wants "+jsnum(r["needed"])
            +" gallons; the "+jsnum(bought)+"-gallon purchase sits at "+jsnum(r["margin"])+"% of that, and "+r["verdict"]+".")

def pace_plan(gpm,sqft,coats):
    if not pos(gpm): return {"error":"the flow rate must be above zero"}
    if not pos(sqft): return {"error":"the square footage must be above zero"}
    if not pos(coats): return {"error":"the coat count must be above zero"}
    minutes=sqft*coats/(gpm*EFFECTIVE)
    if minutes<30: verdict="a quick coat"
    elif minutes<120: verdict="a morning on the trigger"
    else: verdict="a long spray day"
    return {"minutes":r1(minutes),"verdict":verdict}

def render_pace(r,gpm,sqft,coats):
    word=" coat over " if coats==1 else " coats over "
    return ("At "+jsnum(gpm)+" gallons a minute with the overspray loss priced in, "+jsnum(coats)+word
            +jsnum(sqft)+" square feet is about "+jsnum(r["minutes"])+" trigger-minutes - "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="tip": r=tip_plan(*args); fn=render_tip
    elif tool=="coverage": r=coverage_plan(*args); fn=render_coverage
    else: r=pace_plan(*args); fn=render_pace
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(515,),(211,),(517,),(235,),(309,),(411,)]:
    add("tip",a)
for a in [(1200,2,7),(800,1,4),(2000,2,15),(600,2,4),(1500,1,6),(900,3,9)]:
    add("coverage",a)
for a in [(0.5,1200,2),(0.3,3000,2),(0.3,6000,2),(0.8,800,1),(0.4,1800,2),(0.25,500,1)]:
    add("pace",a)
add("tip",[0]); add("tip",[99]); add("tip",[1000]); add("tip",[515.5]); add("tip",["big"])
add("coverage",[0,2,7]); add("coverage",[1200,0,7]); add("coverage",[1200,2,0])
add("pace",[0,1200,2]); add("pace",[0.5,0,2]); add("pace",[0.5,1200,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
