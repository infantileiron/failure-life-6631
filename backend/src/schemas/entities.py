from pydantic import BaseModel,Field,ConfigDict
from typing import Literal
class InputModel(BaseModel):
 model_config=ConfigDict(allow_inf_nan=False)
class LoginInput(InputModel):
 email:str
 password:str
class DatasetInput(InputModel):
 name:str=Field(min_length=2,max_length=100)
 source:str=Field(default='material_life_202611.csv',max_length=100)
 csv_text:str=Field(min_length=20,max_length=1000000)
class RenameDataset(InputModel):
 name:str=Field(min_length=2,max_length=100)
class RuleInput(InputModel):
 name:str=Field(min_length=2,max_length=100)
 cutoff_hours:float|None=Field(default=240,gt=0,le=10000000)
 note:str=Field(default='独立右删失；截止时点事件计入，晚于截止时点转行政删失。',max_length=1000)
class SurvivalStudyInput(InputModel):
 name:str=Field(min_length=2,max_length=100)
 dataset_id:str
 rule_id:str
 group_a:str=Field(default='A',min_length=1,max_length=30)
 group_b:str=Field(default='B',min_length=1,max_length=30)
class RunInput(InputModel):
 study_id:str
class ReviewInput(InputModel):
 run_id:str
 comment:str=Field(min_length=5,max_length=2000)
class DecisionInput(InputModel):
 status:Literal['approved','rejected']
 comment:str=Field(min_length=5,max_length=2000)
class ReportInput(InputModel):
 run_id:str
 review_id:str
 title:str=Field(min_length=2,max_length=100)
