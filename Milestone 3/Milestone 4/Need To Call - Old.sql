Select page0.serial,page0.security,
ilname,ifname,atty,detail,status,grp,page0.fileno,ASST,PAGE48.cltadd,
page72.serial as p72s,Page72a.Atyp,Page72a.Astat,Page72a.Aduedt,Page72a.Atodont,calldt,callstat,page48.email,status2,
(select login from filelocks where caseserial = page0.serial) as LOCK,wdstat,a.TaskToAsst as TaskTo,a.DateAssigned as DateAssigned,
(CASE
                WHEN page1.state1 in ('PR','VI') 
                THEN 'ATC (CST+1) Call times: DAL: 7am-7pm  STT: 8am-8pm'
                WHEN page1.state1 in ('AL','AR','IA','IL','LA','MN','MO','MS','OK','WI')
                THEN 'CST (CST) Call times: DAL: 8am-8am STT: 9am-9pm'
                WHEN page1.state1 in ('KS','SD','ND','NE','TX')
                THEN 'CST/MST (Split State) Call times: DAL: 9am-8pm STT: 10am-9pm'
                WHEN page1.state1 in 

('CT','DC','DE','GA','MA','MD','ME','NC','NH','NJ','NY','OH','PA','RI','SC','VA','VT','WV')
                THEN 'EST (CST+1) Call times: DAL: 7am-7pm  STT: 8am-8pm'
                WHEN page1.state1 in ('FL','IN','MI','TN','KY')
                THEN 'EST/CST (Split State) Call times: DAL: 8am-7pm STT: 9am-8pm'
                WHEN page1.state1='HI'
                THEN 'HST (CST-5) Call times: DAL: 1pm-1am STT: 2pm-2am'
                WHEN page1.state1 in ('CO','MT','NM','UT','WY','AZ')
                THEN 'MST (CST-1) Call times DAL: 9am-9pm STT: 10am-10pm'
                WHEN page1.state1 in ('ID','NV','OR')
                THEN 'MST/PST (Split State) Call times: DAL: 10am-9pm STT: 11am-10pm'
                WHEN page1.state1 in ('CA','WA')
                THEN 'PST (CST-2) Call times: DAL: 10am-10pm STT: 11am-11pm'
                WHEN page1.state1 = 'AK'
                THEN 'AKST/HST (Split State) Call times: DAL: 1pm-12am STT: 2pm-1am'
                ELSE 'Time zone not found' END) as TZ,
dtsigned,sol, page48.phone1, page48.phone2, page48.phone3, page48.phone4

from page0
LEFT OUTER JOIN LBCALLLIST a with (NOLOCK) on a.FileNo = Page0.FileNo
left outer join page1 on page0.serial = page1.caseserial
left outer join page72 on page0.serial = page72.caseserial
left outer join page48 on page0.serial = page48.caseserial
left outer join page49 on page0.serial = page49.caseserial
left outer join page72a on page0.serial = page72a.caseserial
where
EXISTS(select * from page72a where page72a.caseserial = page0.serial)
AND atyp IN ('Census Call','Certification Form') AND astat IN ('Need to Call','Request Call','Low - Call back','High - Call back','Need to call - Deficient','Pending')
OR atyp IN ('Census Call','Certification Form') AND acallst IN ('Need to Call','Request Call','Low - Call back','High - Call back','Need to call - Deficient','Pending')
AND (page0.stattype = 'Active Signed')
AND grp IN ( 'ZC3', 'ZC2', 'ZC1','ZC4')
AND (page0.calldt < dateadd(dd,-3,getdate()) OR page0.calldt IS NULL)
OR callstat IN ('Hotline Callback')
order by dtsigned