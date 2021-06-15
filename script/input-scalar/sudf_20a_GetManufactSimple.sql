create or replace function getManufact_simple(itm int)
returns char(50)
language plpgsql
as
$$
begin
	return (select i_manufact from item where i_item_sk = itm);
end; $$