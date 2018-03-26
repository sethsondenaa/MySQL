SELECT concat(clients.first_name, " ", clients.last_name) as client_name, sites.domain_name as website, count(leads.registered_datetime) as total_leads, DATE_FORMAT(leads.registered_datetime, "%M %d, %Y")
FROM clients
JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON sites.site_id = leads.site_id
WHERE YEAR(leads.registered_datetime) BETWEEN "2011-01-01 00:00:00" AND "2011-12-31 59:59:59"
GROUP BY sites.domain_name
ORDER BY clients.client_id