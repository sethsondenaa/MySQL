SELECT concat(clients.first_name, " ", clients.last_name) as client_name, GROUP_CONCAT(sites.domain_name SEPARATOR  ' / ')
FROM clients
JOIN sites ON clients.client_id = sites.client_id
GROUP BY clients.client_id