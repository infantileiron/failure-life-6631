import hashlib,json
from src.services.km import kaplan_meier
from src.services.logrank import log_rank
from src.services.rule import apply_rule

def analyze(rows,rule,study):
 normalized=[{**r,'entry_hours':float(r.get('entry_hours') or 0)} for r in rows]
 included=[r for r in normalized if r['group'] in (study['group_a'],study['group_b'])]
 observed=apply_rule(included,rule['cutoff_hours']);cutoff=rule['cutoff_hours']
 kept=[r for r in observed if cutoff is None or cutoff>r['entry_hours']];excluded_entry=len(observed)-len(kept)
 a=[r for r in kept if r['group']==study['group_a']];b=[r for r in kept if r['group']==study['group_b']]
 groups=[{'group':study['group_a'],**kaplan_meier(a)},{'group':study['group_b'],**kaplan_meier(b)}]
 return {'groups':groups,'logrank':log_rank(a,b),'rule':rule,'study':study,'included':len(kept),'excluded_other_groups':len(normalized)-len(included),'excluded_entry_not_before_cutoff':excluded_entry,'delayed_entries':sum(r['entry_hours']>0 for r in kept),'administratively_censored':sum(r['administratively_censored'] for r in kept),'observations':kept,'checksum':hashlib.sha256(json.dumps({'rows':rows,'rule':rule,'study':study},sort_keys=True).encode()).hexdigest(),'limitations':['同刻失效与删失均进入事件前风险集，计算失效后再从风险集移除删失','中途入组（左截断）按入组至终点计算：同刻入组计入事件前风险集；行政截止不晚于入组的试件剔除并披露数量','KM假设独立、非信息右删失；不能用未失效试件的观察截止时间当失效寿命','Greenwood方差和逐点log-log区间非同时置信带；S=1且无事件时区间留空，S=0末端方差按极限置0','中位寿命未达到返回空值；全删失只说明观测内未记录失效，不证明无限寿命','log-rank渐近卡方df1；零方差不可估计；小样本/不同比例风险尤其交叉曲线时应谨慎解释','不估计风险比，不把组间p值替代材料采购或工程可靠性认证']}
