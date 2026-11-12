from src.models.entities import SurvivalStudy
from src.utils import repository as repo
from src.utils.identity import new_id,now

def list_studies():return repo.all_rows('studies')
def create(data):
 dataset=repo.get('datasets',data.dataset_id);repo.get('rules',data.rule_id)
 groups={r['group'] for r in dataset['rows']}
 if data.group_a==data.group_b:raise ValueError('比较组必须不同')
 if data.group_a not in groups or data.group_b not in groups:raise ValueError('比较组在数据中不存在')
 return repo.put('studies',SurvivalStudy(new_id('study'),data.name,data.dataset_id,data.rule_id,data.group_a,data.group_b,now()))
