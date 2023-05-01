#!/bin/bash

lambda_function_name='find_lastest_file.zip'

python3 -m pip install -r requirements.txt -t  trigger_sns/packages/

ls -lrt trigger_sns/packages/

pwd

cd trigger_sns/

zip -rq $lambda_function_name lambda_function.py

cd packages/

zip -rq ../trigger_sns/$lambda_function_name .

rm -rf ../trigger_sns/packages/

cd .. 

ls -lrt