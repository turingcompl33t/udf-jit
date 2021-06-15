create or replace function morningToEveRatio(dep int)
returns float
language plpgsql
as
$$
declare
	morningSale int;
	declare eveningSale int;
	declare ratio float;
begin
	morningSale := (select  count(*)
						from web_sales_history, time_dim, customer_demographics
						where ws_sold_time_sk = t_time_sk and ws_bill_customer_sk = cd_demo_sk
							and t_hour>=8 and t_hour<=9
							and cd_dep_count=dep);

	eveningSale := (select count(*)
	from web_sales_history, time_dim, customer_demographics 
	where ws_sold_time_sk = t_time_sk and ws_bill_customer_sk = cd_demo_sk
		and t_hour>=19 and t_hour<=20
		and cd_dep_count=dep);

	ratio := cast (morningSale as float) / cast (eveningSale as float);
	return ratio;
end; $$