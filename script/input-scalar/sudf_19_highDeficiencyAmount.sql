CREATE OR REPLACE FUNCTION highDeficiencyAmount(mnth INT)
RETURNS INT8 AS
$$
DECLARE
BEGIN
  RETURN (SELECT COUNT(*) FROM highDeficiencyAmountWebItemTable(mnth) WHERE defType = 'high deficiency');
END
$$ LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION highDeficiencyAmountWebItemTable(month INT)
RETURNS TABLE (item INT8, qty INT8, defType VARCHAR(40)) AS
$$
DECLARE
  item INT8;
  amt INT8;
  availableQty INT8;
  catDefItem INT8;
  highDemandCount INT8;
  web_qty INT8;
BEGIN
  FOR catDefItem IN (SELECT * FROM highDeficiencyAmountItems(month)) LOOP
    web_qty := (select sum(ws_quantity)
                from web_sales, date_dim
                where d_date_sk = ws_sold_date_sk
                  and d_moy = month
                  and ws_item_sk = catDefItem);

    IF web_qty > 0 THEN
      IF web_qty < 5 THEN
        RETURN QUERY (SELECT catDefItem, web_qty, 'low deficiency');
      ELSIF web_qty < 10 THEN
        RETURN QUERY (SELECT catDefItem, web_qty, 'medium deficiency');
      ELSE
        RETURN QUERY (SELECT catDefItem, web_qty, 'high deficiency');
      END IF;
    END IF;
  END LOOP;
  RETURN;
END
$$ LANGUAGE PLPGSQL;