base_url = "https://api.finicity.com/"

app_key = "*****************"
partner_id = "*****************"
partner_secret = "*****************"

path_map = { 
        'create_token'  : 'aggregation/v2/partners/authentication',
        'add_customer' : 'aggregation/v2/customers/testing',
        'get_customers' : 'aggregation/v1/customers',
        'get_customer_by_id' : 'aggregation/v1/customers',
        'delete_customer_by_id' : 'aggregation/v1/customers',
        }


# log path

f_log = "/home/ec2-user/slt/finicity-api-log/"
token_file = "token.log"
add_cust_file = "add_customer.log"
get_customers_file = "get_customers.log"
delete_customers_file = "delete_customers.log"
