#!/bin/bash

# activate the python virtual environment

if [ $# -lt 2 ] 
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
	echo "usage: DELETE CUSTOMER BY ID"
        echo -e "\tsh  finicity_engine.sh \"DELETE-CUSTOMER-BY-ID\" \"6007416155\""
	echo "usage: GENERATE URL"
        echo -e "\tsh  finicity_engine.sh \"GENERATE-URL\" \"6007465953\""
	echo "usage: TRANSACTION REPORT"
        echo -e "\tsh  finicity_engine.sh \"TRANSACTION-REPORT\" \"6007465953\""
	echo "usage: ADD CONSUMER"
	echo -e "\tsh  finicity_engine.sh \"ADD-CONSUMER\" \"6007465953\" \"{ 'firstName': 'Suzi','lastName': ' Builder','address': '434 W Ascension Way','city': 'Murray','state': 'UT','zip': '84123', 'phone': '6786786786','ssn' : '999606666', 'birthday' : { 'year' : 1995, 'month' : 7, 'dayOfMonth' : 7 }, 'email': 'finicity@test.com' }\""
	echo "usage: GET CUSTOMER TRANSACTION REPORT"
	echo -e "\tsh  finicity_engine.sh \"GET-CUSTOMER-TRANSACTION-REPORT\" \"6007465953\" \"sdy0k5kw188q-transactions\""
	echo "usage: GET CONSUMER BY ID"
	echo -e "\tsh  finicity_engine.sh \"GET-CONSUMER-BY-ID\" \"6007416155\""
	exit 100
fi

action=$1
obj=$2  # body or param or customer_id
obj1=$3 # body if obj is customer_id or any string object
obj2=$4 # param if obj, obj1 is customerid|str and body
obj3=$5 # token_YN


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
elif [ "X${action}" == "XDELETE-CUSTOMER-BY-ID" ]
then
        echo "python3 finicity_engine.py \"delete_customer_by_id\" -t \"${token}\" -id \"${obj}\""
        customer=`python3 finicity_engine.py "delete_customer_by_id" -t "${token}" -id "${obj}"`

        if [ $? -ne 0 ]
        then
                echo "delete customer failed"
                exit 103
        fi

        echo "$customer"
elif [ "X${action}" == "XGENERATE-URL" ]
then
        echo "python3 finicity_engine.py \"generate_url\" -t \"${token}\" -id \"${obj}\" -b \"${obj1}\""
        url=`python3 finicity_engine.py "generate_url" -t "${token}" -id "${obj}" -b "${obj1}"` 

        if [ $? -ne 0 ]
        then
                echo "generate url failed"
                exit 103
        fi

        echo "$url"
elif [ "X${action}" == "XTRANSACTION-REPORT" ]
then
        echo "python3 finicity_engine.py \"trnx_rprt\"  -t \"${token}\" -id \"${obj}\" -b \"${obj1}\" -p \"${obj2}\""
        report=`python3 finicity_engine.py "trnx_rprt" -t "${token}" -id "${obj}" -b "${obj1}" -p "${obj2}"`

        if [ $? -ne 0 ]
        then
                echo "generate transactions report failed"
                exit 103
        fi

        echo "$report"
elif [ "X${action}" == "XADD-CONSUMER" ]
then
        echo "python3 finicity_engine.py \"add_consumer\" -t \"${token}\" -id \"${obj}\" -b \"${obj1}\""
        consumer_attr=`python3 finicity_engine.py "add_consumer" -t "${token}" -id "${obj}" -b "${obj1}"`

        if [ $? -ne 0 ]
        then
                echo "consumer creation failed"
                exit 102
        fi

        echo "$conusmer_attr"
elif [ "X${action}" == "XGET-CUSTOMER-TRANSACTION-REPORT" ]
then
        echo "python3 finicity_engine.py \"customer_trnx_rprt\" -t \"${token}\" -id \"${obj}\" -tid \"${obj1}\""
        customer_rprt=`python3 finicity_engine.py "customer_trnx_rprt" -t "${token}" -id "${obj}" -tid "${obj1}"`

        if [ $? -ne 0 ]
        then
                echo "customer rprt creation failed"
                exit 102
        fi

        echo "$customer_rprt"
elif [ "X${action}" == "XGET-CONSUMER-BY-ID" ]
then
	echo "python3 finicity_engine.py \"get_consumer_by_id\" -t \"${token}\" -id \"${obj}\""
        consumer=`python3 finicity_engine.py "get_consumer_by_id" -t "${token}" -id "${obj}"`

        if [ $? -ne 0 ]
        then
                echo "get consumer by customer failed"
                exit 102
        fi

        echo "$consumer"

fi

