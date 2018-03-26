SELECT sum(billing.amount) as Total_Revenue_for_March_2012 FROM billing
WHERE billing.charged_datetime LIKE "2012-03%"
