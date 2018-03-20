SELECT concat(clients.first_name, " ", clients.last_name) as client_name, count(leads.registered_datetime) as total_leads, MONTHNAME(leads.registered_datetime) as month_generated
FROM clients
JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON sites.site_id = leads.site_id
WHERE YEAR(leads.registered_datetime) = 2011 AND MONTH(leads.registered_datetime)  BETWEEN 1 AND 6
GROUP BY MONTH(leads.registered_datetime), client_name