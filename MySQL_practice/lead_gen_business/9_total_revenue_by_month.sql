SELECT concat(clients.first_name, " ", clients.last_name) as client_name, sum(billing.amount) as revenue,  MONTHNAME(billing.charged_datetime) as month_charge, YEAR(billing.charged_datetime) as year_charge
FROM clients
JOIN billing ON clients.client_id = billing.client_id
GROUP BY clients.client_id, YEAR(billing.charged_datetime), MONTH(billing.charged_datetime)