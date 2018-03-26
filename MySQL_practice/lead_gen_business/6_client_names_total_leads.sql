SELECT concat(clients.first_name, " ", clients.last_name) as client_name, count(leads.registered_datetime) as total_leads
FROM clients
JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON sites.site_id = leads.site_id
WHERE leads.registered_datetime BETWEEN "2011-01-01 00:00:00" AND "2011-12-31 23:59:59"
GROUP BY clients.first_name
