SELECT concat(clients.first_name, " ", clients.last_name) as client_name, sites.domain_name as website, count(leads.registered_datetime) as total_leads, DATE_FORMAT(leads.registered_datetime, "%M %d, %Y")
FROM clients
JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON sites.site_id = leads.site_id
GROUP BY sites.domain_name
ORDER BY clients.client_id