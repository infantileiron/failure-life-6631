from src.models.entities import CensoringRule
from src.utils import repository as repo
from src.utils.identity import new_id,now

def list_rules():return repo.all_rows('rules')
def create(data):return repo.put('rules',CensoringRule(new_id('rule'),data.name,data.cutoff_hours,data.note,now()))
def apply_rule(rows,cutoff):
 if cutoff is None:return [{**r,'administratively_censored':False} for r in rows]
 return [{**r,'duration_hours':min(r['duration_hours'],cutoff),'event':r['event'] if r['duration_hours']<=cutoff else 0,'censored':r['censored'] if r['duration_hours']<=cutoff else 1,'administratively_censored':r['duration_hours']>cutoff} for r in rows]
