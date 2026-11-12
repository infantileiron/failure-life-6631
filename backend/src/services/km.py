import math

def kaplan_meier(rows):
 if not rows:raise ValueError('组内没有试件')
 rows=[{**r,'entry_hours':float(r.get('entry_hours') or 0)} for r in rows]
 if any(not math.isfinite(r['duration_hours']) or r['duration_hours']<=0 or r['event'] not in (0,1) for r in rows):raise ValueError('生存观测时间/事件无效')
 if any(not math.isfinite(r['entry_hours']) or not 0<=r['entry_hours']<r['duration_hours'] for r in rows):raise ValueError('入组小时无效：须为≥0且早于观察终点的有限值')
 times=sorted({r['duration_hours'] for r in rows}|{r['entry_hours'] for r in rows if r['entry_hours']>0});survival=1.;greenwood=0.;curve=[];median=None
 for t in times:
  at_risk=sum(r['entry_hours']<=t<=r['duration_hours'] for r in rows)
  entries=sum(r['entry_hours']==t for r in rows)
  events=sum(r['duration_hours']==t and r['event']==1 for r in rows)
  censored=sum(r['duration_hours']==t and r['event']==0 for r in rows)
  if events:
   survival*=1-events/at_risk
   if at_risk>events:greenwood+=events/(at_risk*(at_risk-events))
  variance=survival*survival*greenwood if survival>0 else 0.
  if survival==0:lower=upper=0.
  elif survival==1:lower=upper=None
  else:
   se=math.sqrt(greenwood)/abs(math.log(survival));theta=math.log(-math.log(survival))
   lower=math.exp(-math.exp(theta+1.959963984540054*se));upper=math.exp(-math.exp(theta-1.959963984540054*se))
  if median is None and survival<=.5:median=t
  curve.append({'time':t,'entries':entries,'at_risk':at_risk,'events':events,'censored':censored,'risk_after':at_risk-events-censored,'survival':survival,'greenwood_sum':greenwood if survival>0 else None,'variance':variance,'ci95_low':lower,'ci95_high':upper,'terminal_all_failed':events==at_risk})
 events_total=sum(r['event'] for r in rows)
 return {'n':len(rows),'delayed_entries':sum(r['entry_hours']>0 for r in rows),'events':events_total,'censored':len(rows)-events_total,'curve':curve,'median_hours':median,'has_failure_events':events_total>0,'warning':'' if events_total else '全删失：观测内KM点估计为1，但寿命中位和失效分布不能由此估计；置信区间留空'}
