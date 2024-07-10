SELECT 
  vendor_id,
  AVG(total_amount) AS avg_revenue,
  AVG(trip_distance) as avg_distance,
  count(*) as number
FROM 'bigquery-public-data:new_york_taxi_trips.tlc_yellow_trips_*' WHERE 
  trip_distance > 0 AND
  fare_amount > 0
GROUP BY vendor_id
ORDER BY avg_revenue DESC