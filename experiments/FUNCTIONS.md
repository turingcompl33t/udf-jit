## Functions

This document provides a quick reference for the scalar UDFs provided in SQL ProcBench.

### Support

SQL ProcBench consists of 24 scalar UDFs. Some of these functions are not viable for use in experiments because they contain constructs that are not supported by one or more of the systems involved in the evaluation.

**Supported Functions (15):**
- 1 "Total Large Purchases"
- 2 "Max Promo Channel"
- 4 "Generate Random Integer"
- 5 "Morning to Evening Ratio"
- 6 "Total Discount"
- 7 "Profitable Manager"
- 10 "Is List Distinct"
- 11 "Generate Random Character"
- 12 "Increase in Web Spending"
- 13 "Max Purchase Channel"
- 17 "Preferred Channel WRT Count"
- 18 "Preferred Channel WRT Expenditure"
- 20a "Get Manufacturer (Simple)"
- 20b "Get Manufacturer (Complex)"

**Unsupported Functions (9):**
- 3a: "Max Return Reason (Web)"
- 3b: "Max Return Reason (Catalog)"
- 3c: "Max Return Reason (Store)"
- 8: "Max Return Class"
- 9a: "Wealth Ship Cost Correlation Catalog"
- 9b: "Wealth Ship Cost Correlation Web"
- 14 "Same Manager"
- 15: "Income Band of Max Buy Customer"
- 16: "Promo Versus No Promo"
- 19: "Web Deficiency Amount"

### Descriptions

A brief description of each function is provided below. If the function is unsupported, a brief explanation is given.

- **1** `TotalLargePurchases`: A single aggregation followed by a `RETURN`.
- **2** `MaxPromoChannel`: Just defers all logic to another UDF (call).
- **3a** `MaxReturnReasonWeb`: Unsupported because it contains subqueries that NoisePage cannot execute.
- **3b** `MaxReturnReasonCatalog`: Unsupported because it contains subqueries that NoisePage cannot execute.
- **3c** `MaxReturnReasonStore`: Unsupported because it contains subqueries that NoisePage cannot execute.
- **4** `GenerateRandomInteger`: Simple control flow with a call to a builtin.
- **5** `MorningToEveningRatio`: Some aggregations followed by calculations.
- **6** `TotalDiscount`: Aggregation queries.
- **7** `ProfitableManager`: An aggregation followed by conditional control flow.
- **8** `MaxReturnClass`: Unsuported because it contains a cursor loop.
- **9a** `WealthShipCostCorrelationCatalog`: Unsupported because it contains subqueries that NoisePage cannot execute.
- **9b** `WealthShipCostCorrelationWeb`: Unsupported because it contains subqueries that NoisePage cannot execute.
- **10** `IsListDistinct`: Consists primarily of builtin string operations, arranged in a `WHILE`-loop construct.
- **11** `GenerateRandomCharacter`: Calls another UDF (`GenerateRandomInteger`), with some basic conditional control flow.
- **12** `IncreaseInWebSpending`: A couple simple aggregation queries with some conditional control flow at the end.
- **13** `MaxPurchaseChannel`: Three aggregations followed by some conditional control flow.
- **14** `SameManager`: Unsupported because of cursor loop. Calls another UDF, contains a query-style `FOR`-loop construct meaning that it may be out of reach for Froid.
- **15** `IncomeBandOfMaxBuyCustomer`: Complex queries followed by conditional control flow; unsupported because it contains subqueries that NoisePage cannot execute.
- **16** `PromoVersusNoPromo`: Complex queries followed by conditional control flow, unsupported because it contains subqueries that NoisePage cannot execute.
- **17** `PreferredChannelWrtCount`: Aggregations followed by conditional control flow.
- **18** `PreferredChannelWrtExpenditure`: Aggregations contained within conditional control flow, guarded by `IF EXISTS` predicates.
- **19** `WebDeficiencyAmount`: Contains three distinct UDFs, two of which are unsupported because they contain `RETURN QUERY` constructs.
- **20a** `GetManufacturerSimple`: Simple aggregation query.
- **20b** `GetManufacturerComplex`: Aggregations with some conditional control flow.

### Inlining

Even if some functions are supported by all systems, Froid is only capable of inlining a subset.

Inlined:

- Function 01: `TotalLargePurchases`
- Function 04: `GenerateRandomInteger`
- Function 06: `TotalDiscount`
- Function 11: `GenerateRandomCharacter`
- Function 13: `MaxPurchaseChannel`

Not Inlined:
- Function 12: `IncreaseInWebSpending`
- Function 17: `PreferredChannelWrtCount`
- Function 18: `PreferredChannelWrtExpenditure`
