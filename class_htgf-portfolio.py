# ---------------------------------------------------------------------------------------
# Python class "HTGF_portfolio" for scientific and research purposes: Structuring public data
# about German High-Tech Gründerfonds' (HTGF) investment and startup portfolio
#
# Purpose: Provide simple functionality for researching data about HTGF investment portfolio.
# Sources used: Webpages stored locally (e.g. in browser cache) and contain lists of startups
# The class provides some methods for extracting relevant company data from local HTML files.
# It uses BeautifulSoup and stores the data extracted in a CSV file on a local storage, too.
#
# Input: Assumption about data acquisition
# - Each webpage to be analyzed is stored locally in a file referred to as "source file"
# - Each source file contains the HTML/ CSS/ JavaScript/ etc. data "just as they are"
# - Each source file has the following filename structure: htgf_CATEGORY_NO_YYYY-MM-DD
#
# Output: Target data model and data types
# - The output data has the following data types: String and Integer
# - Columns/ attributes are as follows:
#   - company_name: String - contains company name (usually including its legal form)
#   - company_description: String - contains company's business model and product(s)
#   - company_branch: String - contains the industry/ branch the company is active in
#   - company_address: String - contains the company's full location and address
#   - company_address_street, company_address_zip, company_address_city: see above
#   - company_url_website: String -  contains url of the company's corporate website
#   - company_url_htgf: String - url of HGTF portfolio page for the respective company
#   - htgf_category: String - HTGF's own types/ categories of branches/ industries
#   - htgf_in_portfolio: String - time period in which HTGF was or still is invested
#   - htgf_exit_likelihood: Integer - contains 1 if startup is still in portfolio, 0 otherwise
#   - htgf_date_investment: YYYY-MM-DD - contains the date by when HTGF invested in company
#   - htgf_date_investment_year, htgf_date_investment_month, htgf_date_investment_day: see above
#   - htgf_date_exit: YYYY-MM-DD - contains the date by when HTGF sold its shares (=exit)
#   - htgf_date_exit_year, htgf_date_exit_month, htgf_date_exit_day: see above
#   - source_filename: String - contains the source's filename (see structure given above)
#   - source_date: YYYY-MM-DD - contains the date according to source filename
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------
from bs4 import BeautifulSoup   # Let's use BeautifulSoup for extracting data from HTML
import os                       # Will be used for reading filenames from input directory
import csv                      # We'll export all the data we extract into a csv file
import sys                      # Used only for determining the current version of Python
from datetime import datetime   # Used for formatting date-related inputs in a proper way
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Class definition: Variables, constructor and methods
# ---------------------------------------------------------------------------------------
class HTGF_portfolio:

    # -----------------------------------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------------------------------
    def __init__(self):
        self.data_raw = None
        self.data_extracted = []
        print("%s%s" %("Python version: ", sys.version[:5]))   # Tested with 3.7.1 64-bit
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
    # Parse raw data and extract information
    # -----------------------------------------------------------------------------------
    def parse(self,content,filename):
        try:
            # Use BeautifulSoup for reading HTML data and extract relevant contents
            self.data_raw = BeautifulSoup(content,'html5lib',from_encoding='None')
            all_products = self.data_raw.find_all('section',{'class':'porfolio_company'})
            
            # For each product extracted from HTML/ CSS data, do the following
            for each in all_products:
                try:
                    ld=[]

                    # Extract the company's name (usually including its legal form) 
                    # Sometimes a company name includes "(Exit)", let's delete it
                    company_name = each.find('h2',{'class':'company_headline'}).get_text().strip()
                    company_name_clean = company_name.replace('(Exit)', '').strip()
                    ld.append(company_name_clean)

                    # Extract description of the company's business model and product(s)
                    company_description = each.find('div',{'class':'company_description'}).get_text().replace('\n', ' ').strip()
                    ld.append(company_description)

                    # Extract the industry/ branch the company is active in
                    company_branch = each.find('div',{'class':'subinfo_branch'}).get_text().replace('Branche:', '').strip()
                    ld.append(company_branch)

                    # Extract the company's location and address
                    # Since addresses aren't formatted in the same structure, we have to take care of some cases 
                    company_address= each.find('div',{'class':'subinfo_adress'}).get_text().replace('Adresse:', '').replace('\t','').replace('\n','<br>').replace('<br>', '', 1).replace('<br><br><br>','').strip()
                    ld.append(company_address)

                    if "<br><br>" not in company_address and "GmbH" in company_address:
                        company_address = '<br>'.join(company_address.replace('D-','').replace('D -','').split('<br>')[1:])

                    if "<br><br>" not in company_address and "GmbH" not in company_address and "<br>" in company_address and "Building" not in company_address and "Gebäude" not in company_address and "c/o" not in company_address:
                        company_address_street = company_address.split('<br>')[0]
                        company_address_zip = company_address.split('<br>')[1].split(' ')[0].replace('D-','').replace('D -','')
                        company_address_city = ' '.join(company_address.split('<br>')[1].split(' ')[1:]) 
                    else:
                        company_address_street = ''
                        company_address_zip = ''
                        company_address_city = ''

                    ld.append(company_address_street)
                    ld.append(company_address_zip)
                    ld.append(company_address_city)

                    # Extract the URL of the company's corporate website
                    company_url_website = each.find('div',{'class':'subinfo_website'}).get_text().replace('Webseite:', '').strip()
                    ld.append(company_url_website)

                    # Extract the URL of HGTF portfolio page for the respective company
                    company_url_htgf = each.find('a', {'class': 'portfolio_finder_link_portfolio'})['href'].strip()
                    ld.append(company_url_htgf)

                    # Extract HTGF's branch/ industry from source filename
                    htgf_category = filename.split('_')[1]
                    ld.append(htgf_category)

                    # Extract the date by when HTGF invested in the company
                    htgf_in_portfolio = each.find('div',{'class':'subinfo_inportfolio'}).get_text().strip()
                    ld.append(htgf_in_portfolio)

                    # Derive from "(Exit)" phrase, if HTGF is still invested
                    if "Exit" in company_name:
                        htgf_exit_likelihood = str(1)
                    else:
                        htgf_exit_likelihood = str(0)
                    ld.append(htgf_exit_likelihood)

                    # Extract time period in which HTGF was or still is invested
                    if "seit" not in htgf_in_portfolio:
                        htgf_in_portfolio = htgf_in_portfolio.replace('�','–').replace('â€“', '–')
                        htgf_date_investment = htgf_in_portfolio.split('–')[0].replace('Im Portfolio', '').strip()
                        htgf_date_exit = htgf_in_portfolio.split('–')[1].strip()
                    else:
                        htgf_date_investment = htgf_in_portfolio.replace('Im Portfolio seit', '').strip()
                        htgf_date_exit = ''
                    
                    # Append date by when HTGF invested in the respective company
                    htgf_date_investment = str(datetime.strptime(htgf_date_investment.replace('Dez', 'Dec').replace('Mrz', 'Mar').replace('Mai', 'May').replace('Okt', 'Oct'), '%d. %b %Y')).split(' ')[0]
                    ld.append(htgf_date_investment)

                    # Split date of investment into its temporal components
                    htgf_date_investment_year = htgf_date_investment.split('-')[0]
                    htgf_date_investment_month = htgf_date_investment.split('-')[1]
                    htgf_date_investment_day = htgf_date_investment.split('-')[2]
                    ld.append(htgf_date_investment_year)      # Append year solely, i.e. YYYY
                    ld.append(htgf_date_investment_month)     # Append month solely, i.e. MM
                    ld.append(htgf_date_investment_day)       # Append day solely, i.e. DD

                    # Append date by when HTGF sold its shares he owned in the respective company
                    if htgf_date_exit != '':
                        htgf_date_exit = str(datetime.strptime(htgf_date_exit.replace('Dez', 'Dec').replace('Mrz', 'Mar').replace('Mai', 'May').replace('Okt', 'Oct'), '%d. %b %Y')).split(' ')[0]
                    ld.append(htgf_date_exit)

                    # Split date of exit into its temporal components
                    if htgf_date_exit != '' and '-' in htgf_date_exit:
                        htgf_date_exit_year = htgf_date_exit.split('-')[0]
                        htgf_date_exit_month = htgf_date_exit.split('-')[1]
                        htgf_date_exit_day = htgf_date_exit.split('-')[2]
                    else:
                        htgf_date_exit_year = ''
                        htgf_date_exit_month = ''
                        htgf_date_exit_day = ''
                    ld.append(htgf_date_exit_year)      # Append year solely, i.e. YYYY
                    ld.append(htgf_date_exit_month)     # Append month solely, i.e. MM
                    ld.append(htgf_date_exit_day)       # Append day solely, i.e. DD

                    # Remember date and filename of source file
                    source_filename = filename
                    ld.append(source_filename)

                    source_date = filename.split('_')[3].replace('.html','')
                    ld.append(source_date)

                    # Append data to the collection
                    self.data_extracted.append(ld)

                except Exception (e):
                    continue

        except Exception (e):
            print ("Parsing error...")
            #print str (e)
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
    # Write extracted information to CSV file
    # -----------------------------------------------------------------------------------
    def write(self):
        try:
            columns = ['company_name',
                        'company_description',
                        'company_branch',
                        'company_address',
                        'company_address_street',
                        'company_address_zip',
                        'company_address_city',
                        'company_url_website',
                        'company_url_htgf',
                        'htgf_category',
                        'htgf_in_portfolio',
                        'htgf_exit_likelihood',
                        'htgf_date_investment',
                        'htgf_date_investment_year',
                        'htgf_date_investment_month',
                        'htgf_date_investment_day',
                        'htgf_date_exit',
                        'htgf_date_exit_year',
                        'htgf_date_exit_month',
                        'htgf_date_exit_day',
                        'source_filename',
                        'source_date']
           
            with open('htgf_portfolio_output.csv', 'w', encoding="utf-8") as f:
                f.write(';'.join(columns) + '\n')
                for row in self.data_extracted:
                    f.write(';'.join(row) + '\n')

        except Exception (e):
            print ("Error: Writing data into the output file failed")
            #print str(e)
    # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------
    # Open local files that contain raw data
    # Filenames of local html files can be specified in the array "files"
    # -----------------------------------------------------------------------------------
    def file_handling(self):
        files = os.listdir()    # Read all filenames from working directory (= source files)
        for filename in files:
            with open(filename,'rb') as fl:
                content = fl.read()
                fl.close()
                self.parse(content,filename)
    # -----------------------------------------------------------------------------------
        
    # -----------------------------------------------------------------------------------
    # Run methods
    # -----------------------------------------------------------------------------------     
    def run(self):
        self.file_handling()
        self.write()
    # -----------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Create new object and execute code
# ---------------------------------------------------------------------------------------
a = HTGF_portfolio()
a.run()
# ---------------------------------------------------------------------------------------