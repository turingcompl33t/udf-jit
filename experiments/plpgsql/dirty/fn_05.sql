-- SQL ProcBench Scalar UDF 05: "Morning to Evening Ratio"

CREATE OR REPLACE FUNCTION morningToEveRatio(dep INT) RETURNS INT AS $$
DECLARE
	morningSale INT;
	eveningSale INT;
	totalSale INT;
BEGIN
	morningSale := (SELECT COUNT(*)
		FROM web_sales_history, time_dim, customer_demographics
		WHERE ws_sold_time_sk = t_time_sk 
      AND ws_bill_customer_sk = cd_demo_sk
			AND t_hour >= 8 AND t_hour <= 9
			AND cd_dep_count = dep);

	eveningSale := (SELECT COUNT(*)
		FROM web_sales_history, time_dim, customer_demographics 
		WHERE ws_sold_time_sk = t_time_sk 
			AND ws_bill_customer_sk = cd_demo_sk
			AND t_hour >= 19 AND t_hour <= 20
			AND cd_dep_count = dep);

	totalSale := morningSale + eveningSale;
	RETURN totalSale;
end; 
$$ LANGUAGE PLPGSQL;
