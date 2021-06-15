create or replace function totalLargePurchases(givenState char, amount decimal, yr int, qtr int)
returns decimal
language plpgsql
as
$$
declare
largePurchase decimal;
begin 
		select sum(cs_net_paid_inc_ship_tax) into largePurchase
		from catalog_sales_history, customer, customer_address, date_dim
		where cs_bill_customer_sk = c_customer_sk and
			  c_current_addr_sk = ca_address_sk and
			  ca_state = givenState and
			  cs_net_paid_inc_ship_tax >= amount and
			  d_date_sk = cs_sold_date_sk and d_year = yr and d_qoy = qtr;
	     return largePurchase;
end;
$$;