-- SQL ProcBench Scalar UDF 12: "Increase in Web Spending"

create or replace function increaseInWebSpending(cust_sk int) returns decimal as
$$
declare
    spending1  decimal;
	spending2  decimal;
	increase  decimal;
begin
	spending1:=0;
    spending2:=0;
    increase:=0;
    
	select sum(ws_net_paid_inc_ship_tax) into spending1 
    from web_sales_history, date_dim
    where d_date_sk = ws_sold_date_sk
        and d_year = 2001
        and ws_bill_customer_sk=cust_sk;
        
	select sum(ws_net_paid_inc_ship_tax)  into spending2
    from web_sales_history, date_dim
    where d_date_sk = ws_sold_date_sk
        and d_year = 2000
        and ws_bill_customer_sk=cust_sk;
        
	if(spending1<spending2) then
		return -1;
	else
		increase := spending1-spending2;
    end if;
	return increase;

end;
$$ LANGUAGE PLPGSQL;
