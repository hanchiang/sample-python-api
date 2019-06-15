SELECT array_agg(name) FROM customers
GROUP BY dob
ORDER BY dob ASC