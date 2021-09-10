-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"

CREATE OR ALTER FUNCTION maxpurchasechannel(@ckey INT, @fromDateSk INT, @toDateSk INT) RETURNS VARCHAR(50) AS
BEGIN
    DECLARE @numSalesFromStore   INT;
    DECLARE @numSalesFromCatalog INT;
    DECLARE @numSalesFromWeb     INT;
    DECLARE @maxChannel          VARCHAR(50);

    SET @numsalesfromstore = (SELECT COUNT(*)
        FROM   store_sales_history
        WHERE  ss_customer_sk = @ckey
        AND    ss_sold_date_sk >= @fromdatesk
        AND    ss_sold_date_sk <= @todatesk);
        
    SET @numsalesfromcatalog = (SELECT COUNT(*)
        FROM   catalog_sales_history
        WHERE  cs_bill_customer_sk = @ckey
        AND    cs_sold_date_sk >= @fromdatesk
        AND    cs_sold_date_sk <= @todatesk);
    
    SET @numsalesfromweb = (SELECT COUNT(*)
        FROM   web_sales_history
        WHERE  ws_bill_customer_sk = @ckey
        AND    ws_sold_date_sk >= @fromdatesk
        AND    ws_sold_date_sk <= @todatesk);
        
    IF(@numSalesFromStore>@numSalesFromCatalog) 
    BEGIN
        SET @maxChannel = 'Store';
        IF(@numSalesfromWeb > @numSalesFromStore)
        BEGIN
            SET @maxChannel = 'Web';
        END
    END
    ELSE
    BEGIN
        SET @maxChannel = 'Catalog';
        IF(@numSalesfromWeb > @numSalesFromCatalog)
        BEGIN
            SET @maxChannel = 'Web';
        END
    END

    RETURN @maxChannel;
END
