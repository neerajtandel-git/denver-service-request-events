--- Monthly Trends in the Total Number of Cases in Denver City ? ---

SELECT 
EXTRACT( month from TO_DATE(casecreateddate,'MM/DD/YYYY') ) as casecreateddate,
count(*) as num_of_cases
FROM service_request_events_schema.denver_311_service_request_events
GROUP BY EXTRACT( month from TO_DATE(casecreateddate,'MM/DD/YYYY') )
ORDER BY casecreateddate;



--- Trend in Top 5 Complaint Types over the Month ---

SELECT a.complaint, to_char( TO_DATE(casecreateddate,'MM/DD/YYYY'),'YYYY-MM') as month, count(*)
FROM 
(
  SELECT lower(casesummary) as complaint, count(*) as total_count
  FROM service_request_events_schema.denver_311_service_request_events
  GROUP BY lower(casesummary)
  ORDER BY total_count desc
  LIMIT 5
) a JOIN service_request_events_schema.denver_311_service_request_events b
ON a.complaint = lower(b.casesummary)
GROUP BY a.complaint, to_char( TO_DATE(casecreateddate,'MM/DD/YYYY'),'YYYY-MM')
ORDER BY month



--- Monthly Volume ---

SELECT to_char( TO_DATE(casecreateddate,'MM/DD/YYYY'), 'YYYY-MM' ) as month, count(*) as monthly_count
FROM service_request_events_schema.denver_311_service_request_events
GROUP BY to_char( TO_DATE(casecreateddate,'MM/DD/YYYY'), 'YYYY-MM' )
ORDER BY month



--- Top 10 Cases - UnResolved ---

SELECT lower(casesummary) as case_summary, count(*) as total_count
FROM service_request_events_schema.denver_311_service_request_events
WHERE casestatus like '%In-Progress%'
GROUP BY lower(casesummary)
ORDER BY total_count desc
LIMIT 10;



--- Service Request Calls by Hourly ---

SELECT to_char( cast(casecreateddttm as timestamp), 'HH24') as hour, count(*) as total_complaints
FROM service_request_events_schema.denver_311_service_request_events
GROUP BY to_char( cast(casecreateddttm as timestamp), 'HH24')
ORDER BY hour








