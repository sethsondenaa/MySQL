SELECT clients.first_name, clients.last_name, clients.client_id, sum(billing.amount) as Total_Revenue FROM billing
JOIN clients ON billing.client_id = clients.client_id
WHERE clients.client_id = 2
