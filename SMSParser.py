# SMS Parser for picking out target data from Test messages
# This code is for Nigerian Bank SMSes.

import pandas as pd
import re
import numpy as np


def sms(file, num):
      from datetime import datetime, timedelta
      
      # To get the Account number
      def acctno(bank, message):
        import re
        if bank == 'Diamond':
          return re.findall('\*{3,6}\d*',message)

        elif bank == 'GTBank':
          return re.findall('\d*?\*+\d*',message)

        elif bank == 'UBA':
          return re.findall('\d+\w\w\.\.\d+x',message)

        elif bank == 'FCMB':
          return re.findall('\d*?\*+\d*',message)

        elif bank == 'Ecobank':
          return re.findall('\d*\*{3,6}\d*', message)

        elif bank == 'StanbicIBTC':
          return re.findall('\d*?x+\d*', message)

        elif bank == 'Accessbank':
          return re.findall('\d*?\*+\d*', message)

       # To get the Transaction types
      def transtype(bank, message):
        import re
        if bank == 'Diamond':
          return re.findall('^debit|credit',message)

        elif bank == 'GTBank':
          return re.findall('amt.\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d (\w\w)',message)

        elif bank == 'UBA':
          return re.findall('credit|debit',message)

        elif bank == 'FCMB':
          return re.findall('^credit|debit|cr|dr',message)

        elif bank == 'Ecobank':
          return re.findall('dr|cr', message)

        elif bank == 'StanbicIBTC':
          return re.findall('debit|credit', message)

        elif bank == 'Accessbank':
          return re.findall('^debit|credit', message)  

      # To get the transaction amounts
      def transamt(bank, message):
        import re
        if bank == 'Diamond':
          return re.findall('amt.\s?(\d*.?\d*.?\d*.?\d*.?\d)',message)

        elif bank == 'GTBank':
          return re.findall('amt.\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d',message)

        elif bank == 'UBA':
          return re.findall('amt.\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d',message)

        elif bank == 'FCMB':
          return re.findall('amt.\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d',message)

        elif bank == 'Ecobank':
          return re.findall('^\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d', message)

        elif bank == 'StanbicIBTC':
          return re.findall('of\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d', message)

        elif bank == 'Accessbank':
          return re.findall('amt.\s?\w?\w?\w?\d*.?\d*.?\d*.?\d*.?\d', message)


      # To get the balance
      def balance(bank, message):
        import re
        if bank == 'Diamond':
          return re.findall('avail\sbal.\s?(\d*.?\d*.?\d*.?\d*.?\d)',message)

        elif bank == 'GTBank':
          return re.findall('bal.\s?\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)',message)

        elif bank == 'UBA':
          return re.findall('bal.\s?\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)',message)

        elif bank == 'FCMB':
          return re.findall('bal.\s?\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)',message)

        elif bank == 'Ecobank':
          return re.findall('bal.\s?is\s\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)', message)

        elif bank == 'StanbicIBTC':
          return re.findall('balance.\s?\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)', message)

        elif bank == 'Accessbank':
          return re.findall('bal.\s?\w?\w?\w?(\d*.?\d*.?\d*.?\d*.?\d)', message)
      
      # Clean up the text gotten
      def clean(dirty) :
        import re
        x = re.sub('[a-z:,\[\]\'\'\s]','', str(dirty))
        return re.sub('\.\d\d', '',x)

      # Get the date from the messages
      def fordate(date):
        import re
        x = re.findall('\d\d\d\d-\d\d-\d\d', date)
        return re.sub('[\[\]\'\']','', str(x))

      def fortype(ttype):
        import re
        return re.sub('[:,\[\]\'\']', '', str(ttype))
      
      #loading the extracted components to a csv
      data = pd.read_csv(str(file),encoding = "ISO-8859-1")
      data['message'] = data['message'].str.lower()
      
      #cleaning the text 
      data['acct no'] = data.apply(lambda row: acctno(row['address'], row['message']), axis=1)
      data['trans type'] = data.apply(lambda row: transtype(row['address'], row['message']), axis=1)
      data['trans amt'] = data.apply(lambda row: transamt(row['address'], row['message']), axis=1)
      data['balance'] = data.apply(lambda row: balance(row['address'], row['message']), axis=1)
      data['date'] = data.apply(lambda row: fordate(row['date']), axis=1)
      data['trans type'] = data.apply(lambda row: fortype(row['trans type']), axis=1)
      data['trans amt'] = data.apply(lambda row: clean(row['trans amt']), axis=1)
      data['balance'] = data.apply(lambda row: clean(row['balance']), axis=1)
      
      #cleaning 
      data['trans amt'] = data['trans amt'].apply(lambda x: np.NaN if x == '' else x)
      data['balance'] = data['balance'].apply(lambda x: np.NaN if x == '' else x)
      data['trans type'] = data['trans type'].apply(lambda x: np.NaN if x == '' else x)
      
      #conversion
      data['trans amt'] = data['trans amt'].astype(float)
      data['balance'] = data['balance'].astype(float)
      data['date'] = data['date'].astype('datetime64[ns]')
      
      #replacement
      data['trans type'] = data['trans type'].replace('cr', 'credit')
      data['trans type'] = data['trans type'].replace('dr', 'debit')
      data['trans type'] = data['trans type'].replace('credit credit', 'credit')
      data['trans type'] = data['trans type'].replace('debit cr', 'debit')
      
      #extraction
      dayx = data[(data['date'] >  datetime.now().date() - timedelta(days=num))]
      credit = dayx[dayx['trans type'] == 'credit']
      debit = dayx[dayx['trans type'] == 'debit']
      avg_cred = np.average( credit['trans amt'])
      avg_deb = np.average(debit['trans amt'])
      max_deb = np.max(debit['trans amt'])
      max_cred = np.max(credit['trans amt'])
      
      # Output of the extraction.
      print('-----------------------------------------------')
      print('Average Debit for Last ',num, 'days:',avg_deb )
      print('-----------------------------------------------')
      print('Average Credit for Last',num, ' days:', avg_cred)
      print('-----------------------------------------------')
      print('Max Credit for Last',num, ' days:', max_cred)
      print('-----------------------------------------------')
      print('Max Debit for Last ',num, ' days:', max_deb)
