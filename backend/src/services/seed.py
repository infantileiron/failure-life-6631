import random
from src.utils import repository as repo
from src.utils.identity import now
from src.utils.security import hash_password
from src.services.statistics import analyze

def demo_rows():
 rng=random.Random(2301);rows=[]
 for group,scale in [('A',180),('B',330)]:
  for i in range(180):
   failure=rng.expovariate(1/scale);censor=rng.uniform(100,340);event=int(failure<=censor);duration=max(5,round(min(failure,censor)/5)*5)
   rows.append({'specimen_id':f'LC-{group}-{i+1:03d}','group':group,'duration_hours':float(duration),'event':event,'censored':1-event})
 return rows

def seed():
 repo.init_db()
 for role,name in [('admin','材料试验复核人'),('analyst','寿命分析员'),('viewer','工艺观察员')]:
  email=f'{role}@lichuan.test';repo.put('users',{'id':email,'email':email,'name':name,'role':role,'password_hash':hash_password('Life2026!')},insert_only=True)
 rows=demo_rows();repo.put('datasets',{'id':'ds-material','name':'11月试件寿命 · 360件','source':'material_life_202611.csv','rows':rows,'created_at':now()},insert_only=True)
 rule={'id':'rule-240h','name':'240小时行政观察截止','cutoff_hours':240.,'note':'独立右删失，截止时刻发生的事件仍计入；同刻先事件风险集再删失。','created_at':now()};repo.put('rules',rule,insert_only=True)
 study={'id':'study-process','name':'A/B加工批寿命复核','dataset_id':'ds-material','rule_id':'rule-240h','group_a':'A','group_b':'B','created_at':now()};repo.put('studies',study,insert_only=True)
 repo.put('runs',{'id':'run-demo','study_id':'study-process','status':'completed','result':analyze(rows,rule,study),'error':'','created_at':now()},insert_only=True)
 repo.put('reviews',{'id':'review-demo','run_id':'run-demo','comment':'独立右删失假设与同刻风险集已核对，中位未达到不填0。','status':'approved','reviewer':'admin@lichuan.test','created_at':now()},insert_only=True)
 repo.put('reports',{'id':'report-demo','run_id':'run-demo','review_id':'review-demo','title':'砾川材料A/B寿命风险集复核册','created_at':now()},insert_only=True)
 return {t:len(repo.all_rows(t)) for t in ('users','datasets','rules','studies','runs','reviews','reports')}
