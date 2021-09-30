CREATE OR REPLACE FUNCTION totalDiscount(manufacture_id int4) RETURNS numeric
AS
$$
    SELECT "return2".*
    FROM (LATERAL
          (SELECT (SELECT avg("RTE0"."ws_ext_discount_amt") AS "avg"
                   FROM web_sales_history AS "RTE0"("ws_sold_date_sk", 
                                                    "ws_sold_time_sk", 
                                                    "ws_ship_date_sk", 
                                                    "ws_item_sk", 
                                                    "ws_bill_customer_sk", 
                                                    "ws_bill_cdemo_sk", 
                                                    "ws_bill_hdemo_sk", 
                                                    "ws_bill_addr_sk", 
                                                    "ws_ship_customer_sk", 
                                                    "ws_ship_cdemo_sk", 
                                                    "ws_ship_hdemo_sk", 
                                                    "ws_ship_addr_sk", 
                                                    "ws_web_page_sk", 
                                                    "ws_web_site_sk", 
                                                    "ws_ship_mode_sk", 
                                                    "ws_warehouse_sk", 
                                                    "ws_promo_sk", 
                                                    "ws_order_number", 
                                                    "ws_quantity", 
                                                    "ws_wholesale_cost", 
                                                    "ws_list_price", 
                                                    "ws_sales_price", 
                                                    "ws_ext_discount_amt", 
                                                    "ws_ext_sales_price", 
                                                    "ws_ext_wholesale_cost", 
                                                    "ws_ext_list_price", 
                                                    "ws_ext_tax", 
                                                    "ws_coupon_amt", 
                                                    "ws_ext_ship_cost", 
                                                    "ws_net_paid", 
                                                    "ws_net_paid_inc_tax", 
                                                    "ws_net_paid_inc_ship", 
                                                    "ws_net_paid_inc_ship_tax", 
                                                    "ws_net_profit"), 
                        item AS "RTE1"("i_item_sk", 
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
                   WHERE ("RTE0"."ws_item_sk" = "RTE1"."i_item_sk"
                          AND
                          "RTE1"."i_manufact_id" = "manufacture_id")) AS "average_1"
          ) AS "let0"("average_1")
          LEFT OUTER JOIN
          (LATERAL
           (SELECT (SELECT sum("RTE2"."ws_ext_discount_amt") AS "sum"
                    FROM web_sales_history AS "RTE2"("ws_sold_date_sk", 
                                                     "ws_sold_time_sk", 
                                                     "ws_ship_date_sk", 
                                                     "ws_item_sk", 
                                                     "ws_bill_customer_sk", 
                                                     "ws_bill_cdemo_sk", 
                                                     "ws_bill_hdemo_sk", 
                                                     "ws_bill_addr_sk", 
                                                     "ws_ship_customer_sk", 
                                                     "ws_ship_cdemo_sk", 
                                                     "ws_ship_hdemo_sk", 
                                                     "ws_ship_addr_sk", 
                                                     "ws_web_page_sk", 
                                                     "ws_web_site_sk", 
                                                     "ws_ship_mode_sk", 
                                                     "ws_warehouse_sk", 
                                                     "ws_promo_sk", 
                                                     "ws_order_number", 
                                                     "ws_quantity", 
                                                     "ws_wholesale_cost", 
                                                     "ws_list_price", 
                                                     "ws_sales_price", 
                                                     "ws_ext_discount_amt", 
                                                     "ws_ext_sales_price", 
                                                     "ws_ext_wholesale_cost", 
                                                     "ws_ext_list_price", 
                                                     "ws_ext_tax", 
                                                     "ws_coupon_amt", 
                                                     "ws_ext_ship_cost", 
                                                     "ws_net_paid", 
                                                     "ws_net_paid_inc_tax", 
                                                     "ws_net_paid_inc_ship", 
                                                     "ws_net_paid_inc_ship_tax", 
                                                     "ws_net_profit"), 
                         item AS "RTE3"("i_item_sk", 
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
                    WHERE ("RTE2"."ws_item_sk" = "RTE3"."i_item_sk"
                           AND
                           "RTE3"."i_manufact_id" = "manufacture_id"
                           AND
                           "RTE2"."ws_ext_discount_amt" > "average_1")) AS "addition_1"
           ) AS "let1"("addition_1")
           LEFT OUTER JOIN
           LATERAL (SELECT "addition_1" AS "result") AS "return2"
           ON True)
          ON True)
$$ LANGUAGE SQL;