-- SQL ProcBench Scalar UDF 01: "Total Large Purchases"

CREATE OR REPLACE FUNCTION totalLargePurchases(givenState VARCHAR, amount FLOAT8, yr INT, qtr INT) RETURNS FLOAT8 AS $$
DECLARE
    largePurchase FLOAT8;
BEGIN
    SELECT SUM(cs_net_paid_inc_ship_tax) INTO largePurchase
    FROM catalog_sales_history, customer, customer_address, date_dim
    WHERE cs_bill_customer_sk = c_customer_sk AND
            c_current_addr_sk = ca_address_sk AND
            ca_state = givenState AND
            cs_net_paid_inc_ship_tax >= amount AND
            d_date_sk = cs_sold_date_sk AND d_year = yr AND d_qoy = qtr;
    RETURN largePurchase;
END;
$$ LANGUAGE PLPGSQL;
