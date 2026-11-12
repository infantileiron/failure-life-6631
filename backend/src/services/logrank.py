import math

def log_rank(group_a,group_b):
 if not group_a or not group_b:raise ValueError('log-rank需要两个非空组')
 group_a=[{**r,'entry_hours':float(r.get('entry_hours') or 0)} for r in group_a];group_b=[{**r,'entry_hours':float(r.get('entry_hours') or 0)} for r in group_b]
 times=sorted({r['duration_hours'] for r in group_a+group_b if r['event']==1});observed_minus_expected=0.;variance=0.;contributions=[]
 for t in times:
  n1=sum(r['entry_hours']<=t<=r['duration_hours'] for r in group_a);n2=sum(r['entry_hours']<=t<=r['duration_hours'] for r in group_b);n=n1+n2
  d1=sum(r['duration_hours']==t and r['event']==1 for r in group_a);d2=sum(r['duration_hours']==t and r['event']==1 for r in group_b);d=d1+d2
  expected=d*n1/n;v=n1*n2*d*(n-d)/(n*n*(n-1)) if n>1 else 0.
  observed_minus_expected+=d1-expected;variance+=v
  contributions.append({'time':t,'n_a':n1,'n_b':n2,'d_a':d1,'d_b':d2,'expected_a':expected,'observed_minus_expected_a':d1-expected,'variance_contribution':v})
 estimable=bool(times) and variance>1e-12
 chi_square=observed_minus_expected**2/variance if estimable else None
 return {'observed_minus_expected_a':observed_minus_expected,'variance':variance,'chi_square':chi_square,'p_value':math.erfc(math.sqrt(chi_square/2)) if estimable else None,'df':1,'estimable':estimable,'warning':'' if estimable else '无失效事件或log-rank方差为0，组间检验不可估计，不返回虚假p值','contributions':contributions}
