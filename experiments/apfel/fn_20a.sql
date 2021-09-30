CREATE OR REPLACE FUNCTION getManufact_simple(itm int4) RETURNS varchar
AS
$$
    SELECT "return1".*
    FROM (LATERAL
          (SELECT (SELECT "RTE0"."i_manufact" AS "i_manufact"
                   FROM item AS "RTE0"("i_item_sk", 
                                       "i_item_id", 
                                       "i_rec_start_date", 
                                       "i_rec_end_date", 
                                       "i_item_desc", 
                                       "i_current_price", 
                                       "i_wholesale_cost", 
                                       "i_brand_id", 
                                       "i_brand", 
                                       "i_class_id", 
                                       "i_category_id", 
                                       "i_category", 
                                       "i_manufact_id", 
                                       "i_manufact", 
                                       "i_size", 
                                       "i_formulation", 
                                       "i_color", 
                                       "i_units", 
                                       "i_container", 
                                       "i_manager_id", 
                                       "i_product_name")
                   WHERE "RTE0"."i_item_sk" = "itm") AS "r_1"
          ) AS "let0"("r_1")
          LEFT OUTER JOIN
          LATERAL (SELECT "r_1" AS "result") AS "return1"
          ON True)
$$ LANGUAGE SQL;