-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"

WITH t AS (
  SELECT ws_item_sk, COUNT(*) cnt FROM web_sales GROUP BY ws_item_sk ORDER BY cnt LIMIT 25000
) SELECT ws_item_sk FROM t WHERE getManufact_simple(ws_item_sk) = 'oughtn st';
