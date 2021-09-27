-- Individual queries from Function 13 that fail in storage layer
SELECT COUNT(*) FROM store_sales_history WHERE ss_customer_sk = 1 AND ss_sold_date_sk >= 2000 AND ss_sold_date_sk <= 2020;
SELECT COUNT(*) FROM catalog_sales_history WHERE cs_bill_customer_sk = 1 AND cs_sold_date_sk >= 2000 AND cs_sold_date_sk <= 2020;
SELECT COUNT(*) FROM web_sales_history WHERE ws_bill_customer_sk = 1 AND ws_sold_date_sk >= 2000 AND ws_sold_date_sk <= 2020;
