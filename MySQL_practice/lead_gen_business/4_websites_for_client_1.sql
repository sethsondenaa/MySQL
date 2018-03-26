SELECT clients.client_id, COUNT(domain_name) as number_of_websites, MONTHNAME(sites.created_datetime) as month_created, YEAR(sites.created_datetime) as year_created 
FROM clients
JOIN sites ON clients.client_id = sites.client_id
WHERE clients.client_id = 1
GROUP BY YEAR(sites.created_datetime), MONTH(sites.created_datetime)