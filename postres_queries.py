good_price_targets = f'select symbol,last_month_avg_pt,last_quarter_avg_pt,last_year_avg_pt from price_target_summary
where last_month_avg_pt > last_quarter_avg_pt and last_quarter_avg_pt > last_year_avg_pt
order by last_month desc'