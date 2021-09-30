-- SQL ProcBench Scalar UDF 06: "Total Discount"

SELECT DISTINCT i_manufact_id, totalDiscount(i_manufact_id) FROM item;
