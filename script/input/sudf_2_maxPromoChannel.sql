create or replace function maxPromoChannel(year int)
returns varchar
language plpgsql
as
$$
declare
begin
	return promoVsNoPromoItems(year);
end;
$$