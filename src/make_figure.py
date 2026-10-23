"""Render the LinkedIn figure (1080x1350) from figures/summary.json.

Run the notebook first, then:  python src/make_figure.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "figures" / "summary.json").read_text())
KEYS = ["<=30 days", "31-90 days", "91-180 days", "No 2nd order"]


def pct_100(shares):
    """Whole percents that sum to 100.

    The headline segment (<=30 days) is rounded normally so it matches the
    headline number; the rest use largest-remainder rounding.
    """
    raw = [shares[k] * 100 for k in KEYS]
    out = [int(round(raw[0]))] + [int(v) for v in raw[1:]]
    rest = sorted(range(1, len(raw)), key=lambda i: raw[i] - int(raw[i]), reverse=True)
    for i in rest[: 100 - sum(out)]:
        out[i] += 1
    return out


cust = pct_100(S["share_of_customers"])
rev = pct_100(S["share_of_revenue"])
med = S["median_revenue_6m"]
fo = S["median_first_order"]
fast, none = "<=30 days", "No 2nd order"
ratio = med[fast] / med[none]

BK='#0D0D0D'; YL='#FFC72C'; RD='#E63228'; W='#F4F1EA'; G1='#8C8C8C'; G2='#3A3A3A'; YD='#8A6B12'
plt.rcParams['font.family']=['Inter Display','Inter','DejaVu Sans']
fig=plt.figure(figsize=(10.8,13.5),dpi=100,facecolor=BK)
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1080); ax.set_ylim(0,1350); ax.axis('off')
# header band
ax.add_patch(Rectangle((0,1130),1080,220,color=YL))
ax.text(70,1280,"E-COMMERCE GROWTH · UK ONLINE RETAILER",fontsize=15,weight='bold',color=BK)
ax.text(70,1195,"The 30-day window",fontsize=58,weight='black',color=BK)
ax.text(70,1152,"When the 2nd order happens matters more than the 1st basket",fontsize=19,color=BK,weight='medium')
# hero stat
ax.text(70,995,f"{cust[0]}%",fontsize=80,weight='black',color=RD)
ax.text(370,1040,"of new customers ordered again",fontsize=21,color=W,weight='semibold')
ax.text(370,1008,"within 30 days…",fontsize=21,color=W,weight='semibold')
ax.text(70,865,f"{rev[0]}%",fontsize=80,weight='black',color=YL)
ax.text(370,910,"…and generated more than half",fontsize=21,color=W,weight='semibold')
ax.text(370,878,"of the cohort's 6-month revenue",fontsize=21,color=W,weight='semibold')
# stacked bars
segs=[('≤30 days',RD),('31–90',YL),('91–180',YD),('No 2nd order',G2)]
X0,WID=70,940
def bar(y,vals,label):
    ax.text(X0,y+62,label,fontsize=15,color=G1,weight='bold')
    x=X0
    for v,(n,c) in zip(vals,segs):
        w=WID*v/100; ax.add_patch(Rectangle((x,y),w-3,50,color=c))
        if v>8: ax.text(x+12,y+25,f"{v:.0f}%",fontsize=17,weight='bold',va='center',color=BK if c in(RD,YL) else W)
        x+=w
bar(740,cust,"SHARE OF CUSTOMERS")
bar(620,rev,"SHARE OF 6-MONTH REVENUE")
lx=X0
for n,c in segs:
    ax.add_patch(Rectangle((lx,575),16,16,color=c)); ax.text(lx+24,583,n,fontsize=14,color=W,va='center'); lx+=200 if n!='No 2nd order' else 0
ax.text(X0+WID,583,"time to 2nd order",fontsize=14,color=G1,va='center',ha='right')
# medians
ax.plot([70,1010],[530,530],color=G2,lw=1.5)
ax.text(70,480,"MEDIAN REVENUE PER CUSTOMER",fontsize=15,color=G1,weight='bold')
rows=[('2nd order ≤30 days',int(med[fast]),0,RD),('No 2nd order',int(med[none]),0,G2)]
ys=[400,320]; mx=med[fast]
for (n,v,f,c),y in zip(rows,ys):
    ax.text(70,y+18,n,fontsize=18,color=W,weight='semibold',va='center')
    w=560*v/mx; ax.add_patch(Rectangle((360,y),w,40,color=c))
    ax.text(360+w+14,y+20,f"£{v:,}",fontsize=22,color=W,weight='black',va='center')
ax.text(70,265,f"First order value: £{fo[fast]:,.0f} vs £{fo[none]:,.0f}.  6-month value: {ratio:.1f}× apart.",fontsize=19,color=YL,weight='bold')
# takeaway
ax.add_patch(Rectangle((70,135),6,80,color=RD))
ax.text(96,190,"Growth lever: move one-timers into the red bucket.",fontsize=21,color=W,weight='bold')
ax.text(96,152,"Onboarding, replenishment nudges and CRM timing all live inside day 1–30.",fontsize=16,color=G1)
ax.text(70,62,"Data: UCI Online Retail (UK, Dec 2010–Dec 2011) · cohort of {:,} customers with first order Dec–May".format(S["cohort_size"]),fontsize=12.5,color=G1)
ax.text(70,38,"6-month revenue measured from each customer's first order · returns & cancellations excluded",fontsize=12.5,color=G1)
fig.savefig(ROOT / 'figures' / '30-day-window.png', facecolor=BK)
print('Saved figures/30-day-window.png')
