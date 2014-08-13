from transaction.models import Transaction
from transactionreal.models import TransactionReal

def createTransactionHistoryTableHtml(userprofile, date_start, date_end):
  consumerTransactions = Transaction.getConsumerTransactions(userprofile.id)
  consumerTransactions = consumerTransactions.filter(date__range=[date_start, date_end])
  if not consumerTransactions:
    return '- No shares in date range. -'
  transactionTableHtml = '<table>'
  transactionTableHtml += '<tr align=\'left\'>'
  transactionTableHtml += '<th>&#8364;/pp</th>'
  transactionTableHtml += '<th>&#8364;</th>'
  transactionTableHtml += '<th>What</th>'
  transactionTableHtml += '<th>Who</th>'
  transactionTableHtml += '<th>Date</th>'
  for transaction in consumerTransactions:
    transactionTableHtml += '<tr>'
    transactionTableHtml += '<td>&#8364;' + '%.2f' % (float(transaction.amount) / transaction.consumers.count()) + '</td>'
    transactionTableHtml += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
    transactionTableHtml += '<td>' + transaction.what + '</td>'
    transactionTableHtml += '<td>' + transaction.buyer.displayname + '</td>'
    transactionTableHtml += '<td>' + transaction.date.strftime('%d %b') + '</td>'
    transactionTableHtml += '</tr>'
  
  transactionTableHtml += '</table>'
  return transactionTableHtml


def createTransactionRealHistoryTableHtml(userprofile, date_start, date_end):
  transactionsRealAll = TransactionReal.getTransactionsRealAllSortedByDate(userprofile.id)
  if not transactionsRealAll:
    return '- No transactions in date range. -' 
  transactionTableHtml = '<table>'
  transactionTableHtml += '<tr align=\'left\'>'
  transactionTableHtml += '<th>&#8364;</th>'
  transactionTableHtml += '<th>From</th>'
  transactionTableHtml += '<th>To</th>'
  transactionTableHtml += '<th>Date</th>'
  for transaction in transactionsRealAll:
    if transaction.date.date() > date_start and transaction.date.date() < date_end:
      transactionTableHtml += '<tr>'
      transactionTableHtml += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
      transactionTableHtml += '<td>' + transaction.sender.displayname + '</td>'
      transactionTableHtml += '<td>' + transaction.receiver.displayname + '</td>'
      transactionTableHtml += '<td>' + transaction.date.strftime('%d %b') + '</td>'
      transactionTableHtml += '</tr>'
  
  transactionTableHtml += '</table>'
  return transactionTableHtml