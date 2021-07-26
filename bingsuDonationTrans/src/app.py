import json
from uuid import uuid4
from datetime import datetime
from .bingsuDonationTrans import PynamoBingsuDonationTrans, PynamoBingsuTotalSum, PynamoBingsuUser

def add_donation_trans(event, context):
    item = event['arguments']
    user_id = item.get('user_id', None)
    amount_baht = item['amount_baht']
    amount_tree = amount_baht/46
    co2_offset_amount = amount_tree*21 #each tree absorb around 21 kg of co2 per year
    donation_trans_item = PynamoBingsuDonationTrans(
        transaction_id = str(uuid4()),
        user_id = item.get('user_id', 'anonymous'),
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        amount_baht = amount_baht,
        amount_tree = amount_tree,
        co2_offset_amount = co2_offset_amount
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
    total_amount_tree = total_sum_item['total_amount_tree'] + amount_tree
    total_co2_offset_amount = total_sum_item['total_co2_offset_amount'] + co2_offset_amount
    total_sum_item_to_update = PynamoBingsuTotalSum(
        transaction_id = "0",
        total_amount_tree = total_amount_tree,
        total_co2_offset_amount = total_co2_offset_amount
    )
    total_sum_item_to_update.save()
    if user_id:
        iterator2 = PynamoBingsuUser.query(user_id)
        user_list = list(iterator2)
        lst = []
        if len(user_list) > 0:
            for user in user_list:
                lst.append(user.returnJson())
        else:
            return {'status': 400}
        current_dict = lst[0]
        current_dict['total_amount_tree'] = current_dict['total_amount_tree'] + amount_tree
        current_dict['total_co2_offset_amount'] = current_dict['total_co2_offset_amount'] + co2_offset_amount
        user_item = PynamoBingsuUser(
            user_id = current_dict['user_id'],
            username = current_dict['username'],
            password = current_dict['password'],
            grab_points = current_dict.get('grab_points', None),
            robinhood_points = current_dict.get('robinhood_points', None),
            foodpanda_points = current_dict.get('foodpanda_points', None),
            coins = current_dict['coins'],
            email = current_dict['email'],
            phone_number = current_dict['phone_number'],
            grab_id = current_dict.get('grab_id', None),
            robinhood_id = current_dict.get('robinhood_id', None),
            foodpanda_id = current_dict.get('foodpanda_id', None),
            co2_amount = current_dict['co2_amount'],
            total_amount_tree = current_dict['total_amount_tree'],
            total_co2_offset_amount = current_dict['total_co2_offset_amount']
        )
        user_item.save()
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