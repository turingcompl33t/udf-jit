CREATE OR REPLACE FUNCTION highDeficiencyAmountItems(month INT)
RETURNS TABLE (item INT8, deficiency INT8) AS
$$
DECLARE
  item INT8;
  amt INT8;
  availableQty INT8;
  catDefItem INT8;
  highDemandCount INT8;
  web_qty INT8;
BEGIN
  FOR item, amt IN (select cs_item_sk, sum(cs_quantity) as ordered_amt
            from catalog_sales, date_dim
            where d_date_sk = cs_sold_date_sk
              and d_moy = month
            group by cs_item_sk) LOOP

    availableQty := (select sum(inv_quantity_on_hand) from inventory, date_dim
                    where inv_item_sk = item
                      and inv_date_sk = d_date_sk
                      and d_moy = month);

    IF availableQty < amt THEN
      RETURN QUERY (SELECT item, amt-availableQty);
    END IF;
  END LOOP;
  RETURN;
END
$$ LANGUAGE PLPGSQL;