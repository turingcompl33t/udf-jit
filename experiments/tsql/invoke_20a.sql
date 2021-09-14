-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"

WITH t AS (
  SELECT TOP 25000 ws_item_sk, COUNT(*) cnt from web_sales GROUP BY ws_item_sk ORDER BY cnt)
) SELECT ws_item_sk FROM t WHERE dbo.getManufact_simple(ws_item_sk) = 'oughtn st';
