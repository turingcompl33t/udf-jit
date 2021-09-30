-- SQL ProcBench Scalar UDF 15: "Income Band of Max Buy Customer"

SELECT s_store_sk FROM store WHERE incomeBandOfMaxBuyCustomer(s_store_sk) = 'lowerMiddle' ORDER BY s_store_sk;
