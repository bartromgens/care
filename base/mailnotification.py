from transaction.models import Transaction
from transactionreal.models import TransactionReal

from datetime import timedelta

def create_transaction_history_table_html(userprofile, date_start, date_end):
  transactionsAll = Transaction.get_transactions_sorted_by_last_modified(userprofile.id)
  
  transactionsInRange = []
  for transaction in transactionsAll:
    if (transaction.lastModified.date() > date_start) and (transaction.lastModified.date() < date_end + timedelta(1)):
      transactionsInRange.append(transaction)
  
  if not transactionsInRange:
    return 'No shares in date range.'
  transactionTableHtml = '<table>'
  transactionTableHtml += '<tr align=\'left\'>'
  transactionTableHtml += '<th><b>&#8364;/pp</b></th>'
  transactionTableHtml += '<th><b>&#8364;</b></th>'
  transactionTableHtml += '<th><b>What</b></th>'
  transactionTableHtml += '<th><b>Who</b></th>'
  transactionTableHtml += '<th><b>Date</b></th>'
  for transaction in transactionsInRange:
    transactionTableHtml += '<tr style="font-size: 12px">'
    transactionTableHtml += '<td>&#8364;' + transaction.amountPerPerson + '</td>'
    transactionTableHtml += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
    transactionTableHtml += '<td>' + transaction.what + '</td>'
    transactionTableHtml += '<td>' + transaction.buyer.displayname + '</td>'
    transactionTableHtml += '<td>' + transaction.date.strftime('%d %b') + '</td>'
    transactionTableHtml += '</tr>'
  
  transactionTableHtml += '</table>'
  return transactionTableHtml


def create_transaction_real_history_table_html(userprofile, date_start, date_end):
  transactionsRealAll = TransactionReal.getTransactionsRealAllSortedByDateLastModified(userprofile.id)
  transactionsInRange = []
  for transaction in transactionsRealAll:
    if transaction.lastModified.date() > date_start and transaction.lastModified.date() < date_end + timedelta(1):
      transactionsInRange.append(transaction)
      
  if not transactionsInRange:
    return 'No transactions in date range.' 
  transactionTableHtml = '<table style="font-size: 12px">'
  transactionTableHtml += '<tr align=\'left\'>'
  transactionTableHtml += '<th><b>&#8364;</b></th>'
  transactionTableHtml += '<th><b>From</b></th>'
  transactionTableHtml += '<th><b>To</b></th>'
  transactionTableHtml += '<th><b>Date</b></th>'
  for transaction in transactionsInRange:
    transactionTableHtml += '<tr>'
    transactionTableHtml += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
    transactionTableHtml += '<td>' + transaction.sender.displayname + '</td>'
    transactionTableHtml += '<td>' + transaction.receiver.displayname + '</td>'
    transactionTableHtml += '<td>' + transaction.date.strftime('%d %b') + '</td>'
    transactionTableHtml += '</tr>'
  
  transactionTableHtml += '</table>'
  return transactionTableHtml