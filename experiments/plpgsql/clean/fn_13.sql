-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"

CREATE OR REPLACE function maxpurchasechannel(ckey INT, fromdatesk INT, todatesk INT) RETURNS VARCHAR(50) AS $$
DECLARE
    numsalesfromstore   INT;
    numSalesFromCatalog INT;
    numSalesFromWeb     INT;
    maxChannel          VARCHAR(50);
BEGIN
    SELECT COUNT(*)
        INTO   numsalesfromstore
        FROM   store_sales_history
        WHERE  ss_customer_sk = ckey
        AND    ss_sold_date_sk >= fromdatesk
        AND    ss_sold_date_sk <= todatesk;

    SELECT COUNT(*)
        INTO   numsalesfromcatalog
        FROM   catalog_sales_history
        WHERE  cs_bill_customer_sk = ckey
        AND    cs_sold_date_sk >= fromdatesk
        AND    cs_sold_date_sk <= todatesk;

    SELECT COUNT(*)
        INTO   numsalesfromweb
        FROM   web_sales_history
        WHERE  ws_bill_customer_sk = ckey
        AND    ws_sold_date_sk >= fromdatesk
        AND    ws_sold_date_sk <= todatesk;

    IF (numsalesfromstore > numsalesfromcatalog) THEN
        maxchannel := 'Store';
        IF (numsalesfromweb > numsalesfromstore) THEN
            maxchannel := 'Web';
        END IF;
    ELSE
        maxchannel := 'Catalog';
        IF (numsalesfromweb > numsalesfromcatalog) THEN
            maxchannel := 'Web';
        END IF;
    END IF;
    
    RETURN maxchannel;
END;
$$ LANGUAGE PLPGSQL;
