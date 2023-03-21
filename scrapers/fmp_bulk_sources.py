import datetime
import scrapers.postgres_5 as postgres_5

today = datetime.date.today()
current_year = today.year
last_year = today.year - 1


bulk_sources = [
    {
        'title': 'Company Profiles',
        'table_name': 'profiles',
        'url': 'https://financialmodelingprep.com/api/v4/profile/all?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Annual {last_year}',
        'table_name': 'income_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Annual {current_year}',
        'table_name': 'income_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Quarterly {last_year}',
        'table_name': 'income_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Quarterly {current_year}',
        'table_name': 'income_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Annual {last_year}',
        'table_name': 'balance_sheet_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Annual {current_year}',
        'table_name': 'balance_sheet_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Quarterly {last_year}',
        'table_name': 'balance_sheet_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Quarterly {current_year}',
        'table_name': 'balance_sheet_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Annual {last_year}',
        'table_name': 'cash_flow_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Annual {current_year}',
        'table_name': 'cash_flow_statement_annual',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Quarterly {last_year}',
        'table_name': 'cash_flow_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Quarterly {current_year}',
        'table_name': 'cash_flow_statement_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Ratios Annual {last_year}',
        'table_name': 'ratios_annual',
        'url': f'https://financialmodelingprep.com/api/v4/ratios-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Ratios Annual {current_year}',
        'table_name': 'ratios_annual',
        'url': f'https://financialmodelingprep.com/api/v4/ratios-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Ratios Quarterly {last_year}',
        'table_name': 'ratios_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/ratios-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Ratios Quarterly {current_year}',
        'table_name': 'ratios_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/ratios-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Key Metrics Annual {last_year}',
        'table_name': 'key_metrics_annual',
        'url': f'https://financialmodelingprep.com/api/v4/key-metrics-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Key Metrics Annual {current_year}',
        'table_name': 'key_metrics_annual',
        'url': f'https://financialmodelingprep.com/api/v4/key-metrics-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Key Metrics Quarterly {last_year}',
        'table_name': 'key_metrics_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/key-metrics-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Key Metrics Quarterly {current_year}',
        'table_name': 'key_metrics_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/key-metrics-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Stock Peers',
        'table_name': 'stock_peers',
        'url': 'https://financialmodelingprep.com/api/v4/stock_peers_bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Ratings',
        'table_name': 'ratings',
        'url': 'https://financialmodelingprep.com/api/v4/rating-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Key Metrics TTM',
        'table_name': 'key_metrics_ttm',
        'url': 'https://financialmodelingprep.com/api/v4/key-metrics-ttm-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Ratios TTM',
        'table_name': 'ratios_ttm',
        'url': 'https://financialmodelingprep.com/api/v4/ratios-ttm-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Financial Scores',
        'table_name': 'financial_scores',
        'url': 'https://financialmodelingprep.com/api/v4/scores-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Financial Growth Annual {last_year}',
        'table_name': 'financial_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/financial-growth-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Financial Growth Annual {current_year}',
        'table_name': 'financial_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/financial-growth-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Financial Growth Quarterly {last_year}',
        'table_name': 'financial_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/financial-growth-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Financial Growth Quarterly {current_year}',
        'table_name': 'financial_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/financial-growth-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Growth Annual {last_year}',
        'table_name': 'income_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-growth-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Growth Annual {current_year}',
        'table_name': 'income_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-growth-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Growth Quarterly {last_year}',
        'table_name': 'income_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-growth-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Income Statement Growth Quarterly {current_year}',
        'table_name': 'income_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/income-statement-growth-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Growth Annual {last_year}',
        'table_name': 'balance_sheet_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-growth-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Growth Annual {current_year}',
        'table_name': 'balance_sheet_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-growth-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Growth Quarterly {last_year}',
        'table_name': 'balance_sheet_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-growth-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Balance Sheet Statement Growth Quarterly {current_year}',
        'table_name': 'balance_sheet_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/balance-sheet-statement-growth-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Growth Annual {last_year}',
        'table_name': 'cash_flow_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-growth-bulk?year={last_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Growth Annual {current_year}',
        'table_name': 'cash_flow_statement_growth_annual',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-growth-bulk?year={current_year}&period=annual&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Growth Quarterly {last_year}',
        'table_name': 'cash_flow_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-growth-bulk?year={last_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': f'Cash Flow Statement Growth Quarterly {current_year}',
        'table_name': 'cash_flow_statement_growth_qtrly',
        'url': f'https://financialmodelingprep.com/api/v4/cash-flow-statement-growth-bulk?year={current_year}&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Price Target Summary',
        'table_name': 'price_target_summary',
        'url': 'https://financialmodelingprep.com/api/v4/price-target-summary-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
    {
        'title': 'Consensus Score',
        'table_name': 'consensus_score',
        'url': 'https://financialmodelingprep.com/api/v4/upgrades-downgrades-consensus-bulk?apikey=e812649ac124bbb4d773e2ff24a28f0d',
    },
]


# print(bulk_sources[1]['url'])
print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' started bulk inserting '))
for i in range(len(bulk_sources)):
  postgres_5.insert_data(
    bulk_sources[i]['url'],
    bulk_sources[i]['table_name'],
    bulk_sources[i]['title']
    )
print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' finished bulk inserting '))
# postgres_5.what()