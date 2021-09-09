-- SQL ProcBench Scalar UDF 06: "Total Discount"

SELECT DISTINCT i_manufact_id, dbo.totalDiscount(i_manufact_id) AS totalDisc FROM item;
