# Python Class for Investment and Startup Research
Python class "HTGF_portfolio" for scientific and research purposes: Structuring public data about German High-Tech Gründerfonds' investment and startup portfolio (HTGF, said to be Germany's largest venture capital firm)

- Purpose: Provide simple functionality for researching data about HTGF investment portfolio.
- Sources used: Webpages stored locally (e.g. in browser cache) and contain lists of startups
- The class provides some methods for extracting relevant company data from local HTML files.
- It uses BeautifulSoup and stores the data extracted in a CSV file on a local storage, too.

# Output: Target data model and data types
- The output data has the following data types: String and Integer
- Columns/ attributes are as follows:
  - company_name: String - contains company name (usually including its legal form)
  - company_description: String - contains company's business model and product(s)
  - company_branch: String - contains the industry/ branch the company is active in
  - company_address: String - contains the company's full location and address
  - company_address_street, company_address_zip, company_address_city: see above
  - company_url_website: String -  contains URL of the company's corporate website
  - company_url_htgf: String - URL of HGTF portfolio page for the respective company
  - htgf_category: String - HTGF's own types/ categories of branches/ industries
  - htgf_in_portfolio: String - time period in which HTGF was or still is invested
  - htgf_exit_likelihood: Integer - contains 1 if startup is still in portfolio, 0 otherwise
  - htgf_date_investment: YYYY-MM-DD - contains the date by when HTGF invested in company
  - htgf_date_investment_year, htgf_date_investment_month, htgf_date_investment_day: see above
  - htgf_date_exit: YYYY-MM-DD - contains the date by when HTGF sold hir shares (=exit)
  - htgf_date_exit_year, htgf_date_exit_month, htgf_date_exit_day: see above
  - source_filename: String - contains the source's filename (see structure given above)
  - source_date: YYYY-MM-DD - contains the date according to source filename
