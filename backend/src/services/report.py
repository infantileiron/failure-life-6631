import csv,io
from fastapi import HTTPException
from src.models.entities import Report
from src.config.settings import ARTIFACT_DIR
from src.utils import repository as repo
from src.utils.identity import new_id,now

def safe_cell(value):return "'"+value if isinstance(value,str) and value.lstrip().startswith(('=','+','-','@')) else value
def list_reports():return repo.all_rows('reports')
def create(data):
 run,review=repo.get('runs',data.run_id),repo.get('reviews',data.review_id)
 if review['status']!='approved' or review['run_id']!=run['id'] or run['status']!='completed':raise ValueError('报告必须引用该运行已通过的复核')
 report=repo.put('reports',Report(new_id('rpt'),data.run_id,data.review_id,data.title,now()));ARTIFACT_DIR.mkdir(parents=True,exist_ok=True);(ARTIFACT_DIR/(report['id']+'.csv')).write_text(download(report['id']),encoding='utf-8');return report
def download(id):
 report=repo.get('reports',id);run=repo.get('runs',report['run_id']);r=run['result']
 if repo.get('reviews',report['review_id'])['status']!='approved':raise HTTPException(403,'复核未通过')
 out=io.StringIO();w=csv.writer(out);lr=r['logrank']
 w.writerow(['report','included','excluded_other_groups','excluded_entry_not_before_cutoff','delayed_entries','administratively_censored','chi_square_df1','p_value','logrank_estimable','checksum']);w.writerow([safe_cell(report['title']),r['included'],r['excluded_other_groups'],r.get('excluded_entry_not_before_cutoff',0),r.get('delayed_entries',0),r['administratively_censored'],lr['chi_square'],lr['p_value'],lr['estimable'],r['checksum']])
 w.writerow([]);w.writerow(['group','time_hours','entries','at_risk','events','censored','risk_after','survival','greenwood_variance','ci95_low','ci95_high','median_hours'])
 for g in r['groups']:
  for p in g['curve']:w.writerow([safe_cell(g['group']),p['time'],p.get('entries',0),p['at_risk'],p['events'],p['censored'],p['risk_after'],p['survival'],p['variance'],p['ci95_low'],p['ci95_high'],g['median_hours']])
 w.writerow([]);w.writerow(['event_time','n_a','n_b','d_a','d_b','expected_a','observed_minus_expected_a','variance_contribution'])
 for p in lr['contributions']:w.writerow([p[k] for k in ['time','n_a','n_b','d_a','d_b','expected_a','observed_minus_expected_a','variance_contribution']])
 return '\ufeff'+out.getvalue()
