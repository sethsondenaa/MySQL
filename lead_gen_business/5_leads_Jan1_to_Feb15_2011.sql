SELECT domain_name, count(leads.leads_id), DATE_FORMAT(leads.registered_datetime, "%b %d, %Y")
FROM sites
JOIN leads ON sites.site_id = leads.site_id
WHERE leads.registered_datetime  BETWEEN "2011-01-01 00:00:00" AND "2011-02-15 11:59:59"
GROUP BY domain_name