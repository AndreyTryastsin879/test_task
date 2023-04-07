import time
import random
from datetime import datetime
import multiprocessing

import pandas as pd
import numpy as np
from web3 import Web3

import chain_settings
from config import *


def open_csv():
    try:
        table = pd.read_csv(REPORT_TABLE_NAME)
        
        return table.to_dict('records')
    
    except:
        report_table = {}
        report_table['chain_name'] = np.nan
        report_table['wallet_address'] = np.nan
        report_table['transaction_type'] = np.nan
        report_table['transaction_status'] = np.nan
        report_table['sent_amount'] = np.nan
        report_table['transaction_url'] = np.nan
        report_table['date'] = np.nan
        report_table['error'] = np.nan
        
        table_template = pd.DataFrame(report_table, index=[0])
        table_template.to_csv(REPORT_TABLE_NAME, index=False)
        table = pd.read_csv(REPORT_TABLE_NAME)
        
        return table.to_dict('records')


def create_report(report_table, chain_name, 
                  wallet_address, transaction_type, transaction_status, 
                  amount, trasaction_url, error):
    d={}
    d['chain_name'] = chain_name
    d['wallet_address'] = wallet_address
    d['transaction_type'] = transaction_type
    d['transaction_status'] = transaction_status
    d['sent_amount'] = amount
    d['transaction_url'] = trasaction_url
    d['date'] = datetime.now().strftime('%d-%m-%Y')
    d['error'] = error
    
    report_table.append(d)
    
    result_table = pd.DataFrame.from_dict(report_table)
    
    result_table.dropna(inplace=True)
    
    result_table.to_csv(REPORT_TABLE_NAME, index=False)


def create_random_value_from_range(min_value, max_value):
        
    random_value_between_range = random.choice(range(min_value, max_value))
        
    return random_value_between_range


def create_random_amount_for_sending(min_value_for_sending, max_value_for_sending,
                                     number_of_variations_between_sending_amount):
    
    random_position = random.choice(range(number_of_variations_between_sending_amount))
    
    return np.linspace(min_value_for_sending, 
                       max_value_for_sending, 
                       num=number_of_variations_between_sending_amount)[random_position]


def create_connection(url):
    rpc_url = f'{url}'
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    return web3


def create_testnet_connection(url, port):
    rpc_url = f'{url}:{port}/'
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    return web3


def transaction_settings(web3, from_address, to_address, amount):
    gas_price = web3.eth.gas_price
    
    # количество газа
    gas = 2_000_000  # ставим побольше

    # число подтвержденных транзакций отправителя
    nonce = web3.eth.get_transaction_count(from_address)

    transaction = {
      'chainId': web3.eth.chain_id,
      'from': from_address,
      'to': to_address,
      'value': int(Web3.to_wei(amount, 'ether')),
      'nonce': nonce, 
      'gasPrice': gas_price,
      'gas': gas,
    }
    
    return transaction


def create_sign_send_transaction(web3, from_address, to_address, amount, private_key):
    
    create_transaction = transaction_settings(
        web3=web3,
        from_address=from_address,
        to_address=to_address,
        amount=amount
    )
    
    signed_transaction = web3.eth.account.sign_transaction(create_transaction, private_key)
    
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    return transaction_hash.hex()


def check_transaction_status(web3, from_address, to_address, 
                            amount, private_key, transaction_hash, 
                            transaction_type, chain_name, explorer_url):

	print('Проверка статуса транзакции')

	address = web3.eth.account.from_key(private_key).address

	transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)['status']
	
	if transaction_receipt == 0:
		#time.sleep(random.choice(range(3,6)))
		report_table = open_csv()
		create_report(report_table, chain_name, address,
		              transaction_type, 'FAIL', amount,
		              f'{explorer_url}/{transaction_hash}', '-')
		
		counter = 0
		while counter != 5:
	                    
			transaction_hash = create_sign_send_transaction(web3, from_address, to_address, amount, private_key)
			
			transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)['status']
	        
			if transaction_receipt == 0:
				#time.sleep(random.choice(range(3,6)))
				report_table = open_csv()
				create_report(report_table, chain_name, address,
				              transaction_type, 'FAIL', amount,
				              f'{explorer_url}/{transaction_hash}', '-')
				counter += 1

				#небольшой рандомный слип 
				timesleep_value = create_random_value_from_range(5, 15)

				time.sleep(timesleep_value)
	            
			else:
				#time.sleep(random.choice(range(3,6)))
				report_table = open_csv()
				create_report(report_table, chain_name, address,
				               transaction_type, 'SUCCESS', amount,
				              f'{explorer_url}/{transaction_hash}', '-') 
				break

	else:
		#time.sleep(random.choice(range(3,6)))
		report_table = open_csv()
		create_report(report_table, chain_name, address,
	                   transaction_type, 'SUCCESS', amount,
	                  f'{explorer_url}/{transaction_hash}', '-')   
		pass


def self_transaction(web3, amount, private_key,
                     min_timesleep_between_transactions,
                     max_timesleep_between_transactions, 
                     explorer_url, chain_name, number_of_process):

	#небольшой рандомный слип перед началом
	timesleep_value = create_random_value_from_range(5, 15)

	time.sleep(timesleep_value)

	transaction_type = 'SELF-транзакция'
	print('\n')
	print(f'{transaction_type} {chain_name} Поток №{number_of_process}')
	    
	my_address = web3.eth.account.from_key(private_key).address

	print(f'Адрес кошелька: {my_address}')
	
	transaction_hash = create_sign_send_transaction(web3, my_address, my_address, 
	                                                amount, private_key)

	print(f'Хеш {transaction_type} {chain_name} Поток №{number_of_process}:', transaction_hash)

	check_transaction_status(web3, my_address, my_address, 
	                         amount, private_key, transaction_hash, 
	                         transaction_type, chain_name, explorer_url)
	
	timesleep_value = create_random_value_from_range(min_timesleep_between_transactions, 
	                                                 max_timesleep_between_transactions)

	print(f'Пауза {timesleep_value} сек {transaction_type} {chain_name} Поток №{number_of_process}', '\n')

	time.sleep(timesleep_value)
 

def random_transaction(web3, amount, private_key,
                       min_timesleep_between_transactions,
                       max_timesleep_between_transactions,
                       explorer_url, chain_name, number_of_process):

	#небольшой рандомный слип перед началом
	timesleep_value = create_random_value_from_range(5, 15)

	time.sleep(timesleep_value)

	transaction_type = 'RANDOM-транзакция'
	print('\n')
	print(f'{transaction_type} {chain_name} Поток №{number_of_process}')
	    
	with open(TXT_WITH_RECEPIENT_FOR_RANDOM_SENDING) as file:
	    list_of_addresses = [line.strip() for line in file.readlines()]

	random_wallet = random.choice(list_of_addresses)

	my_address = web3.eth.account.from_key(private_key).address

	print(f'Адрес кошелька: {my_address}')
	
	prepared_wallet = web3.to_checksum_address(random_wallet)
	
	transaction_hash = create_sign_send_transaction(web3, my_address, prepared_wallet, 
	                                                amount, private_key)

	print(f'Хеш {transaction_type} {chain_name} Поток №{number_of_process}:', transaction_hash)

	check_transaction_status(web3, my_address, prepared_wallet, 
	                         amount, private_key, transaction_hash, 
	                         transaction_type, chain_name, explorer_url)
	
	timesleep_value = create_random_value_from_range(min_timesleep_between_transactions, 
	                                                 max_timesleep_between_transactions)

	print(f'Пауза {timesleep_value} сек {transaction_type} {chain_name} Поток №{number_of_process}', '\n')

	time.sleep(timesleep_value)


def main_function(private_key):
	#небольшой рандомный слип перед объявлением потока
	timesleep_value = create_random_value_from_range(5, 15)

	time.sleep(timesleep_value)

	#определение номера потока
	current_process_name = multiprocessing.current_process().name
	
	number_of_process = current_process_name.split('-')[1]
	
	print('Поток №', number_of_process)	

	#определение отложенного рандомного старта
	timesleep_value = create_random_value_from_range(MIN_TIMESLEEP_BETWEEN_MULTIPROCESSING, 
											         MAX_TIMESLEEP_BETWEEN_MULTIPROCESSING)

	print(f'До старта потока {timesleep_value} сек.', '\n')

	time.sleep(timesleep_value)

	#итерация по запланированным чейнам
	for chain in map(chain_settings.__dict__.get, chain_settings.__all__):

		#chain_tnx_counter = 0

		try:

		    #web3 = create_connection(chain['url'])
			web3 = create_testnet_connection(chain['url'], chain['port'])

			address = web3.eth.account.from_key(private_key).address

			if web3.is_connected() == False:
			    report_table = open_csv()
			    create_report(report_table, chain_name, address, '-', '-', '-', '-', 'Соединение не установлено') 
			    
			    time.sleep(5)
			    continue

			time.sleep(5)

			#определение некоторых переменных для отправки транзакций, проверок и отчетов
			chain_name = chain['name']

			min_amount_for_sending = chain['min_amount_for_sending']
			max_amount_for_sending = chain['max_amount_for_sending']

			blockchain_explorer_url = chain['explorer_url']
			explorer_txn_path = chain['explorer_txn_path']

			explorer_url = f'{blockchain_explorer_url}/{explorer_txn_path}'

			#определение количества рандомных транзакции, которое будет совершено для чейна
			transactions_amount = create_random_value_from_range(chain['min_transactions'], chain['max_transactions'])

			for transaction in range(transactions_amount):

			    try:
			      amount = create_random_amount_for_sending(min_amount_for_sending, max_amount_for_sending,
			                                                NUMBER_OF_VARIATIONS_BETWEEN_SENDING_AMOUNT)

			      random.choice([self_transaction, random_transaction])(web3, amount, private_key,
			                                                            MIN_TIMESLEEP_BETWEEN_TRANSACTIONS,
			                                                            MAX_TIMESLEEP_BETWEEN_TRANSACTIONS,
			                                                            explorer_url, chain_name, number_of_process)

			      #chain_tnx_counter += 1

			    except Exception as error:
			      report_table = open_csv()
			      create_report(report_table, chain_name, address, '-', '-', '-', '-', error)  

			      #chain_tnx_counter += 1

			      print(error,'\n')

		except Exception as error:
		    report_table = open_csv()
		    create_report(report_table, chain_name, '-', '-', '-', '-', '-', error)  
		    print(error,'\n')

		#небольшой рандомный слип перед принтом количество сделанных транзакции для чейна
		#timesleep_value = create_random_value_from_range(5, 15)
#
		#time.sleep(timesleep_value)
#
		#print(CHAIN_TNX_COUNTER_STRING.format(chain_name, number_of_process, chain_tnx_counter),'\n')        


