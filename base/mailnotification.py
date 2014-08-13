from transaction.models import Transaction

def createTransactionHistoryTableHtml(userprofile, date_start, date_end):
  consumerTransactions = Transaction.getConsumerTransactions(userprofile.id)
  consumerTransactions = consumerTransactions.filter(date__range=[date_start, date_end])
  transactionTableHtml = '<table>'
  transactionTableHtml += '<tr align=\'left\'>'
  transactionTableHtml += '<th>What</th>'
  transactionTableHtml += '<th>Who</th>'
  transactionTableHtml += '<th>&#8364</th>'
  transactionTableHtml += '<th>&#8364 pp</th>'
  transactionTableHtml += '<th>Date</th>'
  for transaction in consumerTransactions:
    transactionTableHtml += '<tr>'
    transactionTableHtml += '<td>' + transaction.what + '</td>'
    transactionTableHtml += '<td>' + transaction.buyer.displayname + '</td>'
    transactionTableHtml += '<td>' + '%.2f' % float(transaction.amount) + '</td>'
    transactionTableHtml += '<td>' + '%.2f' % (float(transaction.amount) / transaction.consumers.count()) + '</td>'
    transactionTableHtml += '<td>' + transaction.date.strftime('%d %b') + '</td>'
    transactionTableHtml += '</tr>'
  
  transactionTableHtml += '</table>'
  return transactionTableHtml