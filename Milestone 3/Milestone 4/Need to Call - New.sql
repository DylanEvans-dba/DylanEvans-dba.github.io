SELECT  page0.serial,page0.security,
        ilname,ifname,atty,detail,status,grp,page0.fileno,
        ASST,PAGE48.cltadd,page72.serial AS p72s,Page72a.Atyp,
        Page72a.Astat,Page72a.Aduedt,Page72a.Atodont,calldt,
        callstat,page48.email,status2,
        
        (
            SELECT login 
            FROM filelocks 
            WHERE caseserial = page0.serial
        ) AS LOCK,
        
        wdstat,
        a.TaskToAsst as TaskTo,
        a.DateAssigned as DateAssigned,

        (
            CASE
                WHEN page1.state1 IN ('PR','VI') 
                THEN 'ATC (CST+1) Call times: DAL: 7am-7pm  STT: 8am-8pm'
                WHEN page1.state1 IN ('AL','AR','IA','IL','LA','MN','MO','MS','OK','WI')
                THEN 'CST (CST) Call times: DAL: 8am-8am STT: 9am-9pm'
                WHEN page1.state1 IN ('KS','SD','ND','NE','TX')
                THEN 'CST/MST (Split State) Call times: DAL: 9am-8pm STT: 10am-9pm'
                WHEN page1.state1 IN ('CT','DC','DE','GA','MA','MD','ME','NC','NH','NJ','NY','OH','PA','RI','SC','VA','VT','WV')
                THEN 'EST (CST+1) Call times: DAL: 7am-7pm  STT: 8am-8pm'
                WHEN page1.state1 IN ('FL','IN','MI','TN','KY')
                THEN 'EST/CST (Split State) Call times: DAL: 8am-7pm STT: 9am-8pm'
                WHEN page1.state1='HI'
                THEN 'HST (CST-5) Call times: DAL: 1pm-1am STT: 2pm-2am'
                WHEN page1.state1 IN ('CO','MT','NM','UT','WY','AZ')
                THEN 'MST (CST-1) Call times DAL: 9am-9pm STT: 10am-10pm'
                WHEN page1.state1 IN ('ID','NV','OR')
                THEN 'MST/PST (Split State) Call times: DAL: 10am-9pm STT: 11am-10pm'
                WHEN page1.state1 IN ('CA','WA')
                THEN 'PST (CST-2) Call times: DAL: 10am-10pm STT: 11am-11pm'
                WHEN page1.state1 = 'AK'
                THEN 'AKST/HST (Split State) Call times: DAL: 1pm-12am STT: 2pm-1am'
                ELSE 'Time zone not found' 
                END
        ) AS TZ,

        dtsigned,sol, page48.phone1, page48.phone2, page48.phone3, page48.phone4

FROM page0
LEFT OUTER JOIN LBCALLLIST a WITH (NOLOCK) ON a.FileNo = Page0.FileNo
LEFT OUTER JOIN page1 ON page0.serial = page1.caseserial
LEFT OUTER JOIN page72 ON page0.serial = page72.caseserial
LEFT OUTER JOIN page48 ON page0.serial = page48.caseserial
LEFT OUTER JOIN page49 ON page0.serial = page49.caseserial
LEFT OUTER JOIN page72a ON page0.serial = page72a.caseserial

WHERE EXISTS (SELECT * FROM page72a WHERE page72a.caseserial = page0.serial)
    AND atyp IN ('Census Call','Certification Form') 
    AND astat IN 
        (
            'Need to Call','Request Call','Low - Call back',
            'High - Call back','Need to call - Deficient','Pending'
        )

OR atyp IN ('Census Call','Certification Form') 
    AND acallst IN 
        (
            'Need to Call','Request Call','Low - Call back',
            'High - Call back','Need to call - Deficient','Pending'
        )
    AND (page0.stattype = 'Active Signed')
    AND grp IN ( 'ZC3', 'ZC2', 'ZC1','ZC4')
    AND 
        (
            page0.calldt < DATEADD(dd,-3,GETDATE()) 
            OR page0.calldt IS NULL 
            OR callstat IN ('Hotline Callback')
        )
        
ORDER BY dtsigned