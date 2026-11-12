from dataclasses import dataclass,field
from typing import Any
@dataclass
class SpecimenDataset:
 id:str
 name:str
 source:str
 rows:list[dict]
 created_at:str=''
@dataclass
class CensoringRule:
 id:str
 name:str
 cutoff_hours:float|None
 note:str=''
 created_at:str=''
@dataclass
class SurvivalStudy:
 id:str
 name:str
 dataset_id:str
 rule_id:str
 group_a:str='A'
 group_b:str='B'
 created_at:str=''
@dataclass
class SurvivalRun:
 id:str
 study_id:str
 status:str='queued'
 result:dict[str,Any]=field(default_factory=dict)
 error:str=''
 created_at:str=''
@dataclass
class LifeReview:
 id:str
 run_id:str
 comment:str
 status:str='pending'
 reviewer:str=''
 created_at:str=''
@dataclass
class Report:
 id:str
 run_id:str
 review_id:str
 title:str
 created_at:str=''
