import hashlib,json
from src.services.km import kaplan_meier
from src.services.logrank import log_rank
from src.services.rule import apply_rule

def analyze(rows,rule,study):
 included=[r for r in rows if r['group'] in (study['group_a'],study['group_b'])]
 observed=apply_rule(included,rule['cutoff_hours']);a=[r for r in observed if r['group']==study['group_a']];b=[r for r in observed if r['group']==study['group_b']]
 groups=[{'group':study['group_a'],**kaplan_meier(a)},{'group':study['group_b'],**kaplan_meier(b)}]
 return {'groups':groups,'logrank':log_rank(a,b),'rule':rule,'study':study,'included':len(included),'excluded_other_groups':len(rows)-len(included),'administratively_censored':sum(r['administratively_censored'] for r in observed),'observations':observed,'checksum':hashlib.sha256(json.dumps({'rows':rows,'rule':rule,'study':study},sort_keys=True).encode()).hexdigest(),'limitations':['同刻失效与删失均进入事件前风险集，计算失效后再从风险集移除删失','KM假设独立、非信息右删失；不能用未失效试件的观察截止时间当失效寿命','Greenwood方差和逐点log-log区间非同时置信带；S=1且无事件时区间留空，S=0末端方差按极限置0','中位寿命未达到返回空值；全删失只说明观测内未记录失效，不证明无限寿命','log-rank渐近卡方df1；零方差不可估计；小样本/不同比例风险尤其交叉曲线时应谨慎解释','不估计风险比，不把组间p值替代材料采购或工程可靠性认证']}
