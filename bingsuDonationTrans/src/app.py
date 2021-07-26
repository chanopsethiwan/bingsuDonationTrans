import json
from uuid import uuid4
from datetime import datetime
from .bingsuDonationTrans import PynamoBingsuDonationTrans, PynamoBingsuTotalSum

def add_donation_trans(event, context):
    item = event['arguments']
    donation_trans_item = PynamoBingsuDonationTrans(
        transaction_id = str(uuid4()),
        user_id = item.get('user_id', 'anonymous'),
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        amount_baht = item['amount_baht'],
        amount_tree = item['amount_tree'],
        co2_offset_amount = item['co2_offset_amount']
    )
    donation_trans_item.save()
    iterator = PynamoBingsuTotalSum.query("0")
    total_sum_list = list(iterator)
    lst = []
    if len(total_sum_list) > 0:
        for i in total_sum_list:
            lst.append(i.returnJson())
    else:
        return {'status': 400}
    total_sum_item = lst[0]
    total_amount_tree = total_sum_item['total_amount_tree'] + item['amount_tree']
    total_co2_offset_amount = total_sum_item['total_co2_offset_amount'] + item['co2_offset_amount']
    total_sum_item_to_update = PynamoBingsuTotalSum(
        transaction_id = "0",
        total_amount_tree = total_amount_tree,
        total_co2_offset_amount = total_co2_offset_amount
    )
    total_sum_item_to_update.save()
    return {'status': 200}

def get_total_sum(event, context):
    iterator = PynamoBingsuTotalSum.query("0")
    total_sum_list = list(iterator)
    lst = []
    if len(total_sum_list) > 0:
        for i in total_sum_list:
            lst.append(i.returnJson())
    else:
        return {'status': 400}
    total_sum_item = lst[0]
    return {'status': 200,
            'total_amount_tree': total_sum_item['total_amount_tree'],
            'total_co2_offset_amount': total_sum_item['total_co2_offset_amount']}