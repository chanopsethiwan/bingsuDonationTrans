from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
import os

class PynamoBingsuDonationTrans(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_DONATION_TRANS_TABLE_NAME')
        region = 'ap-southeast-1'
    transaction_id = UnicodeAttribute(hash_key = True)
    user_id = UnicodeAttribute(null=True)
    date_time = UnicodeAttribute()
    amount_baht = NumberAttribute()
    amount_tree = NumberAttribute()
    co2_offset_amount = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')
    
class PynamoBingsuTotalSum(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_TOTAL_SUM_TABLE_NAME')
        region = 'ap-southeast-1'
    transaction_id = UnicodeAttribute(hash_key = True)
    total_amount_tree = NumberAttribute()
    total_co2_offset_amount = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')
    
class PynamoBingsuUser(Model):
    ''' database to store user '''
    class Meta:
        table_name = 'BingsuUser'
        region = 'ap-southeast-1'
    user_id = UnicodeAttribute(hash_key = True)
    username = UnicodeAttribute()
    password = UnicodeAttribute()
    grab_points = NumberAttribute(null=True)
    robinhood_points = NumberAttribute(null=True)
    foodpanda_points = NumberAttribute(null=True)
    coins = NumberAttribute()
    email = UnicodeAttribute()
    phone_number = UnicodeAttribute()
    grab_id = UnicodeAttribute(null=True)
    robinhood_id = UnicodeAttribute(null=True)
    foodpanda_id = UnicodeAttribute(null=True)
    co2_amount = NumberAttribute()
    total_amount_tree = NumberAttribute()
    total_co2_offset_amount = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')
    
class PynamoBingsuTotalLastWeek(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_TOTAL_LAST_WEEK_TABLE_NAME')
        region = 'ap-southeast-1'
    company = UnicodeAttribute(hash_key = True)
    day = UnicodeAttribute(range_key = True)
    total_co2_amount = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')