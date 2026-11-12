import csv,io,math
from dataclasses import asdict
from src.models.entities import SpecimenDataset
from src.utils import repository as repo
from src.utils.identity import new_id,now
from src.constants.domain import MAX_SPECIMENS,GROUP_LIMIT

def summary(item):return {k:v for k,v in item.items() if k!='rows'}|{'row_count':len(item['rows']),'groups':sorted({r['group'] for r in item['rows']}),'events':sum(r['event'] for r in item['rows']),'censored':sum(1-r['event'] for r in item['rows']),'delayed_entries':sum(1 for r in item['rows'] if r.get('entry_hours',0)>0)}
def list_datasets():return [summary(x) for x in repo.all_rows('datasets')]
def detail(id):return repo.get('datasets',id)
def rename(id,data):
 item=repo.get('datasets',id);item['name']=data.name;repo.put('datasets',item);return summary(item)
def create(data):
 reader=csv.DictReader(io.StringIO(data.csv_text.lstrip('\ufeff')))
 if not {'specimen_id','group','duration_hours','event'}.issubset(reader.fieldnames or []):raise ValueError('CSV需要specimen_id,group,duration_hours,event；可含censored=1-event与entry_hours入组小时')
 rows=[];seen=set()
 for n,r in enumerate(reader,2):
  if n>MAX_SPECIMENS+1:raise ValueError('最多5000试件')
  id=(r.get('specimen_id') or '').strip();group=(r.get('group') or '').strip()
  try:
   time=float(r.get('duration_hours') or 'nan');event=r.get('event')
   if not math.isfinite(time) or not 0<time<=10000000 or event not in ('0','1') or not id or id in seen or not 1<=len(group)<=30:raise ValueError()
   event=int(event)
   if 'censored' in (reader.fieldnames or []) and r.get('censored')!=str(1-event):raise ValueError()
   entry_text=(r.get('entry_hours') or '').strip();entry=float(entry_text) if entry_text else 0.
   if not math.isfinite(entry) or not 0<=entry<time:raise ValueError()
  except (ValueError,TypeError):raise ValueError(f'第{n}行时间/事件/删失/入组/组别/试件编号无效或重复')
  seen.add(id);rows.append({'specimen_id':id,'group':group,'duration_hours':time,'event':event,'censored':1-event,'entry_hours':entry})
 if len(rows)<2:raise ValueError('至少2个试件')
 if len({r['group'] for r in rows})>GROUP_LIMIT:raise ValueError('最多8个组别')
 item=SpecimenDataset(new_id('ds'),data.name,data.source,rows,now());repo.put('datasets',item);return summary(asdict(item))
