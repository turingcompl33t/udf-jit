-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"
--
-- Modifications: Current implementation hits an error in the optimizer,
-- likely as a result of the use of UDF in the predicate condition.

-- WITH t AS (
--   SELECT ws_item_sk, COUNT(*) cnt FROM web_sales GROUP BY ws_item_sk ORDER BY cnt LIMIT 25000
-- ) SELECT ws_item_sk FROM t WHERE getManufact_simple(ws_item_sk) = 'oughtn st';

WITH t(item_id) AS (SELECT ws_item_sk FROM web_sales LIMIT 10) SELECT item_id, getManufact_simple(item_id) FROM t;
