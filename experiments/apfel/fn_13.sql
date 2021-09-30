CREATE OR REPLACE FUNCTION maxPurchaseChannel(ckey int4, 
                                              fromdatesk int4, 
                                              todatesk int4) RETURNS varchar
AS
$$
    SELECT "ifresult4".*
    FROM (LATERAL
          (SELECT (SELECT count(*) AS "count"
                   FROM store_sales_history AS "RTE0"("ss_sold_date_sk", 
                                                      "ss_sold_time_sk", 
                                                      "ss_item_sk", 
                                                      "ss_customer_sk", 
                                                      "ss_cdemo_sk", 
                                                      "ss_hdemo_sk", 
                                                      "ss_addr_sk", 
                                                      "ss_store_sk", 
                                                      "ss_promo_sk", 
                                                      "ss_ticket_number", 
                                                      "ss_quantity", 
                                                      "ss_wholesale_cost", 
                                                      "ss_list_price", 
                                                      "ss_sales_price", 
                                                      "ss_ext_discount_amt", 
                                                      "ss_ext_sales_price", 
                                                      "ss_ext_wholesale_cost", 
                                                      "ss_ext_list_price", 
                                                      "ss_ext_tax", 
                                                      "ss_coupon_amt", 
                                                      "ss_net_paid", 
                                                      "ss_net_paid_inc_tax", 
                                                      "ss_net_profit")
                   WHERE ("RTE0"."ss_customer_sk" = "ckey"
                          AND
                          "RTE0"."ss_sold_date_sk" >= "fromdatesk"
                          AND
                          "RTE0"."ss_sold_date_sk" <= "todatesk")) AS "numsalesfromstore_1"
          ) AS "let0"("numsalesfromstore_1")
          LEFT OUTER JOIN
          (LATERAL
           (SELECT (SELECT count(*) AS "count"
                    FROM catalog_sales_history AS "RTE1"("cs_sold_date_sk", 
                                                         "cs_sold_time_sk", 
                                                         "cs_ship_date_sk", 
                                                         "cs_bill_customer_sk", 
                                                         "cs_bill_cdemo_sk", 
                                                         "cs_bill_hdemo_sk", 
                                                         "cs_bill_addr_sk", 
                                                         "cs_ship_customer_sk", 
                                                         "cs_ship_cdemo_sk", 
                                                         "cs_ship_hdemo_sk", 
                                                         "cs_ship_addr_sk", 
                                                         "cs_call_center_sk", 
                                                         "cs_catalog_page_sk", 
                                                         "cs_ship_mode_sk", 
                                                         "cs_warehouse_sk", 
                                                         "cs_item_sk", 
                                                         "cs_promo_sk", 
                                                         "cs_order_number", 
                                                         "cs_quantity", 
                                                         "cs_wholesale_cost", 
                                                         "cs_list_price", 
                                                         "cs_sales_price", 
                                                         "cs_ext_discount_amt", 
                                                         "cs_ext_sales_price", 
                                                         "cs_ext_wholesale_cost", 
                                                         "cs_ext_list_price", 
                                                         "cs_ext_tax", 
                                                         "cs_coupon_amt", 
                                                         "cs_ext_ship_cost", 
                                                         "cs_net_paid", 
                                                         "cs_net_paid_inc_tax", 
                                                         "cs_net_paid_inc_ship", 
                                                         "cs_net_paid_inc_ship_tax", 
                                                         "cs_net_profit")
                    WHERE ("RTE1"."cs_bill_customer_sk" = "ckey"
                           AND
                           "RTE1"."cs_sold_date_sk" >= "fromdatesk"
                           AND
                           "RTE1"."cs_sold_date_sk" <= "todatesk")) AS "numsalesfromcatalog_1"
           ) AS "let1"("numsalesfromcatalog_1")
           LEFT OUTER JOIN
           (LATERAL
            (SELECT (SELECT count(*) AS "count"
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
                                                      "ws_net_profit")
                     WHERE ("RTE2"."ws_bill_customer_sk" = "ckey"
                            AND
                            "RTE2"."ws_sold_date_sk" >= "fromdatesk"
                            AND
                            "RTE2"."ws_sold_date_sk" <= "todatesk")) AS "numsalesfromweb_1"
            ) AS "let2"("numsalesfromweb_1")
            LEFT OUTER JOIN
            (LATERAL
             (SELECT "numsalesfromstore_1" > "numsalesfromcatalog_1" AS "q4_1"
             ) AS "let3"("q4_1")
             LEFT OUTER JOIN
             LATERAL
             ((SELECT "ifresult7".*
               FROM (LATERAL
                     (SELECT 'Store' AS "maxchannel_6") AS "let5"("maxchannel_6")
                     LEFT OUTER JOIN
                     (LATERAL
                      (SELECT "numsalesfromweb_1" > "numsalesfromstore_1" AS "q8_4"
                      ) AS "let6"("q8_4")
                      LEFT OUTER JOIN
                      LATERAL
                      ((SELECT "return9".*
                        FROM (LATERAL
                              (SELECT 'Web' AS "maxchannel_8") AS "let8"("maxchannel_8")
                              LEFT OUTER JOIN
                              LATERAL (SELECT "maxchannel_8" AS "result") AS "return9"
                              ON True)
                        WHERE "q8_4")
                         UNION ALL
                       (SELECT "maxchannel_6" AS "result"
                        WHERE NOT "q8_4")
                      ) AS "ifresult7"
                      ON True)
                     ON True)
               WHERE "q4_1")
                UNION ALL
              (SELECT "ifresult13".*
               FROM (LATERAL
                     (SELECT 'Catalog' AS "maxchannel_2") AS "let11"("maxchannel_2")
                     LEFT OUTER JOIN
                     (LATERAL
                      (SELECT "numsalesfromweb_1" > "numsalesfromcatalog_1" AS "q12_2"
                      ) AS "let12"("q12_2")
                      LEFT OUTER JOIN
                      LATERAL
                      ((SELECT "return15".*
                        FROM (LATERAL
                              (SELECT 'Web' AS "maxchannel_4") AS "let14"("maxchannel_4")
                              LEFT OUTER JOIN
                              LATERAL (SELECT "maxchannel_4" AS "result") AS "return15"
                              ON True)
                        WHERE "q12_2")
                         UNION ALL
                       (SELECT "maxchannel_2" AS "result"
                        WHERE NOT "q12_2")
                      ) AS "ifresult13"
                      ON True)
                     ON True)
               WHERE NOT "q4_1")
             ) AS "ifresult4"
             ON True)
            ON True)
           ON True)
          ON True)
$$ LANGUAGE SQL;