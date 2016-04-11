from datetime import timedelta

from transaction.models import Transaction
from transaction.models import TransactionReal


def create_transaction_history_table_html(userprofile, date_start, date_end):
    transactions_all = Transaction.get_transactions_sorted_by_last_modified(userprofile.id)

    transactions_in_timerange = []
    for transaction in transactions_all:
        if (transaction.last_modified.date() > date_start) and (transaction.last_modified.date() < date_end + timedelta(1)):
            transactions_in_timerange.append(transaction)

    if not transactions_in_timerange:
        return ''
    transaction_table = '<table>'
    transaction_table += '<tr align=\'left\'>'
    transaction_table += '<th><b>&#8364;/pp</b></th>'
    transaction_table += '<th><b>&#8364;</b></th>'
    transaction_table += '<th><b>What</b></th>'
    transaction_table += '<th><b>Who</b></th>'
    transaction_table += '<th><b>Date</b></th>'
    for transaction in transactions_in_timerange:
        transaction_table += '<tr style="font-size: 12px">'
        transaction_table += '<td>&#8364;' + transaction.amount_per_person + '</td>'
        transaction_table += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
        transaction_table += '<td>' + transaction.what + '</td>'
        transaction_table += '<td>' + transaction.buyer.displayname + '</td>'
        transaction_table += '<td>' + transaction.date.strftime('%d %b') + '</td>'
        transaction_table += '</tr>'

    transaction_table += '</table>'
    return transaction_table


def create_transaction_real_history_table_html(userprofile, date_start, date_end):
    transactionreal_all = TransactionReal.get_transactions_real_sorted_by_last_modified(userprofile.id)
    transactions_in_timerange = []
    for transaction in transactionreal_all:
        if transaction.last_modified.date() > date_start and transaction.last_modified.date() < date_end + timedelta(1):
            transactions_in_timerange.append(transaction)

    if not transactions_in_timerange:
        return ''
    transaction_table = '<table style="font-size: 12px">'
    transaction_table += '<tr align=\'left\'>'
    transaction_table += '<th><b>&#8364;</b></th>'
    transaction_table += '<th><b>From</b></th>'
    transaction_table += '<th><b>To</b></th>'
    transaction_table += '<th><b>Date</b></th>'
    for transaction in transactions_in_timerange:
        transaction_table += '<tr>'
        transaction_table += '<td>&#8364;' + '%.2f' % float(transaction.amount) + '</td>'
        transaction_table += '<td>' + transaction.sender.displayname + '</td>'
        transaction_table += '<td>' + transaction.receiver.displayname + '</td>'
        transaction_table += '<td>' + transaction.date.strftime('%d %b') + '</td>'
        transaction_table += '</tr>'

    transaction_table += '</table>'
    return transaction_table
