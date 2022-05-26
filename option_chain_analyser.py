"""Option Chain Analyser

# Nifty50 Option Chain Analyser 
In this python script we scrape the Nifty50 **Option Chain** Data from NSE (National Stock Exchange) website.
We use the fundamentals of **technical analysis** and **effecient markets theory** to do some rudimentary Option Chain Analysis. 

**Libraries Used** 
- Request
- Pandas 

### Option Chain
An options chain, also known as an option matrix, is a listing of all available options contracts for a given security. 
It shows all listed puts, calls, their expiration, strike prices, and volume and pricing information for a single underlying asset within a given maturity period.
The chain will typically be categorized by expiration date and segmented by calls vs. puts.

An options chain provides detailed quote and price information and should not be confused with an options series or cycle, which instead simply denotes the available strike prices or expiration dates.

### Technical Analysis
Technical analysis is a trading discipline employed to evaluate investments and identify trading opportunities by analyzing statistical trends gathered from trading activity, such as price movement and volume. Unlike fundamental analysis, which attempts to evaluate a security's value based on business results such as sales and earnings, technical analysis focuses on the study of price and volume.

### Effecient Markets Theory
The efficient market hypothesis (EMH), alternatively known as the efficient market theory, is a hypothesis that states that share prices reflect all information and consistent alpha generation is impossible.

According to the EMH, stocks always trade at their fair value on exchanges, making it impossible for investors to purchase undervalued stocks or sell stocks for inflated prices. Therefore, it should be impossible to outperform the overall market through expert stock selection or market timing, and the only way an investor can obtain higher returns is by purchasing riskier investments.
"""

#Importing Dependencies
import requests
import pandas as pd

#Forging request to scrape data from the NSE website
r = requests.get('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY', headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'})
#print(r.json())

#Cleaning the Raw JSON and filtering the required data
j = r.json()
j_filtered = j['filtered']
j_data = j_filtered['data']
assert all(d['PE']['strikePrice'] == d['CE']['strikePrice'] for d in j_data)
dfPE = pd.DataFrame((d['PE'] for d in j_data)).add_prefix('PE')
dfCE = pd.DataFrame((d['CE'] for d in j_data)).add_prefix('CE')
df = pd.concat([dfPE, dfCE], axis=1)
df.drop(columns=['CEstrikePrice', 'CEexpiryDate'])

#Rudimentary Option Chain Analysis on df and printing final value
maxPE = df['PEstrikePrice'][df['PEopenInterest'].idxmax()]
maxCE = df['CEstrikePrice'][df['CEopenInterest'].idxmax()]

expiry = df["PEexpiryDate"][1]

print(f"The Nifty50 Index is estimated to close between {maxPE} and {maxCE} this expiry on {expiry}")
print(f"The Strongest resistance is {maxCE}")
print(f"The Strongest support is {maxPE}")
