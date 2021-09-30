-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"

CREATE OR REPLACE function maxpurchasechannel(ckey INT, fromdatesk INT, todatesk INT) RETURNS VARCHAR AS $$
DECLARE
    numSalesFromStore   INT;
    numSalesFromCatalog INT;
    numSalesFromWeb     INT;
    maxChannel          VARCHAR;
BEGIN
    numSalesFromStore := (SELECT COUNT(*)
        FROM   store_sales_history
        WHERE  ss_customer_sk = ckey
        AND    ss_sold_date_sk >= fromdatesk
        AND    ss_sold_date_sk <= todatesk);

    numSalesFromCatalog := (SELECT COUNT(*)
        FROM   catalog_sales_history
        WHERE  cs_bill_customer_sk = ckey
        AND    cs_sold_date_sk >= fromdatesk
        AND    cs_sold_date_sk <= todatesk);

    numSalesFromWeb := (SELECT COUNT(*)
        FROM   web_sales_history
        WHERE  ws_bill_customer_sk = ckey
        AND    ws_sold_date_sk >= fromdatesk
        AND    ws_sold_date_sk <= todatesk);

    IF (numSalesFromStore > numSalesFromCatalog) THEN
        maxChannel := 'Store';
        IF (numsalesfromweb > numSalesFromStore) THEN
            maxChannel := 'Web';
        END IF;
    ELSE
        maxChannel := 'Catalog';
        IF (numsalesfromweb > numSalesFromCatalog) THEN
            maxChannel := 'Web';
        END IF;
    END IF;
    
    RETURN maxChannel;
END;
$$ LANGUAGE PLPGSQL;
