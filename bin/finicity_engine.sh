#!/bin/bash

# activate the python virtual environment

if [ $# -ne 2 ] 
then
	echo "usage: finicity_engine.sh <action> <new-user-obj>"
	echo "usage: ADD USER"
	echo -e "\tsh  finicity_engine.sh \"ADD-USER\" \"{'username' : 'slt-user6' , 'firstName' : 'slt', 'lastName' : 'technology' }\""
	echo "usage: GET CUSTOMERS"
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{}\""
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{'search' : 'customerusername1'}\""
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{'search' : 'slt'}\""
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{'limit' : 3 }\""
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{'start' : 10, 'limit' : 2}\""
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMERS\" \"{'username' : 'slt-user1'}\""
	echo "usage: GET CUSTOMER BY ID"
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMER-BY-ID\" \"6007416155\""
	exit 100
fi

action=$1
obj=$2

source ~/slt/venv/slt-python3.7/bin/activate

echo "******************** get the token *******************"

token=`python3 finicity_engine.py "create_token"`

if [ $? -ne 0 ]
then
	echo "create_token failed"
	exit 101
fi

echo "$token"

echo "****************** new test-user creation *****************"

echo "${action}"
if [ "X${action}" == "XADD-USER" ]
then
	echo "python3 finicity_engine.py \"add_customer\" -t \"${token}\" -b \"${obj}\""
	user_attr=`python3 finicity_engine.py "add_customer" -t "${token}" -b "${obj}"`

	if [ $? -ne 0 ]
	then
        	echo "test user creation failed"
        	exit 102
	fi

	echo "$user_attr"
elif [ "X${action}" == "XGET-CUSTOMERS" ]
then
	echo "python3 finicity_engine.py \"get_customers\" -t \"${token}\" -p \"${obj}\""
        customers=`python3 finicity_engine.py "get_customers" -t "${token}" -p "${obj}"`

        if [ $? -ne 0 ]
        then
                echo "get customers failed"
                exit 102
        fi

        echo "$customers"
elif [ "X${action}" == "XGET-CUSTOMER-BY-ID" ]
then
        echo "python3 finicity_engine.py \"get_customer_by_id\" -t \"${token}\" -id \"${obj}\""
        customer=`python3 finicity_engine.py "get_customer_by_id" -t "${token}" -id "${obj}"`

        if [ $? -ne 0 ]
        then
                echo "get customer failed"
                exit 103
        fi

        echo "$customer"	
fi

