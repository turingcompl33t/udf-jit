### Function 06

Function 06 fails with the same error as Function 13, also in the storage layer:

```sql
SELECT AVG(ws_ext_discount_amt) FROM web_sales_history, item WHERE ws_item_sk = i_item_sk AND i_manufact_id = 0;
```

### Function 13

Function 13 contains at least one query that fails on its own, in the storage layer:

```sql
SELECT COUNT(*) FROM store_sales_history WHERE ss_customer_sk = 1 AND ss_sold_date_sk >= 2000 AND ss_sold_date_sk <= 2020;
```

It also contains two other queries I have yet to try:

```sql
SELECT COUNT(*) FROM catalog_sales_history WHERE cs_bill_customer_sk = 1 AND cs_sold_date_sk >= 2000 AND cs_sold_date_sk <= 2020;
SELECT COUNT(*) FROM web_sales_history WHERE ws_bill_customer_sk = 1 AND ws_sold_date_sk >= 2000 AND ws_sold_date_sk <= 2020;
```
