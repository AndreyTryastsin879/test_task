import time
import random
from datetime import datetime

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
        report_table['private_key'] = np.nan
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
                  private_key, transaction_type, transaction_status, 
                  amount, trasaction_url, error):
    d={}
    d['chain_name'] = chain_name
    d['private_key'] = private_key
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


def create_random_timesleeps(min_timesleep_between_transactions, max_timesleep_between_transactions):
    
    timesleep_between_trasactions_range = range(min_timesleep_between_transactions,
                                                max_timesleep_between_transactions)
    
    timesleep_value = random.choice(timesleep_between_trasactions_range)
        
    return timesleep_value


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
                            transaction_type, chain_name, explorer_url,
                            min_timesleep_between_transactions, max_timesleep_between_transactions):

    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)['status']
    
    print('Проверка статуса транзакции', '\n')

    if transaction_receipt == 0:
        time.sleep(random.choice(range(10,20)))
        report_table = open_csv()
        create_report(report_table, chain_name, private_key,
                      transaction_type, 'FAIL', amount,
                      f'{explorer_url}/{transaction_hash}', '-')
        
        counter = 0
        while counter != 5:
                        
            transaction_hash = create_sign_send_transaction(web3, from_address, to_address, amount, private_key)
            
            transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)['status']
            
            if transaction_receipt == 0:
                time.sleep(random.choice(range(10,20)))
                report_table = open_csv()
                create_report(report_table, chain_name, private_key,
                              transaction_type, 'FAIL', amount,
                              f'{explorer_url}/{transaction_hash}', '-')
                counter += 1

                timesleep_value = create_random_timesleeps(min_timesleep_between_transactions,
                                                           max_timesleep_between_transactions)

                time.sleep(timesleep_value)
                
            else:
                time.sleep(random.choice(range(10,20)))
                report_table = open_csv()
                create_report(report_table, chain_name, private_key,
                               transaction_type, 'SUCCESS', amount,
                              f'{explorer_url}/{transaction_hash}', '-') 
                break

    else:
        time.sleep(random.choice(range(10,20)))
        report_table = open_csv()
        create_report(report_table, chain_name, private_key,
                       transaction_type, 'SUCCESS', amount,
                      f'{explorer_url}/{transaction_hash}', '-')   
        pass


def self_transaction(web3, amount, private_key,
                     min_timesleep_between_transactions,
                     max_timesleep_between_transactions, 
                     explorer_url, chain_name):

    transaction_type = 'SELF-транзакция'
    
    print(f'{transaction_type} {chain_name}')
    
    print(f'Количество монет для отправки: {amount}')
    
    my_address = web3.eth.account.from_key(private_key).address
    
    transaction_hash = create_sign_send_transaction(web3, my_address, my_address, 
                                                    amount, private_key)

    check_transaction_status(web3, my_address, my_address, 
                             amount, private_key, transaction_hash, 
                             transaction_type, chain_name, explorer_url,
                             min_timesleep_between_transactions, max_timesleep_between_transactions)

    print(f'{explorer_url}/{transaction_hash}')
    
    timesleep_value = create_random_timesleeps(min_timesleep_between_transactions, 
                                               max_timesleep_between_transactions)

    print(f'Пауза {timesleep_value}', '\n')

    time.sleep(timesleep_value)
 

def random_transaction(web3, amount, private_key,
                       min_timesleep_between_transactions,
                       max_timesleep_between_transactions,
                       explorer_url, chain_name):

    transaction_type = 'RANDOM-транзакция'
    
    print(f'{transaction_type} {chain_name}')
    
    print(f'Количество монет для отправки: {amount}')
        
    with open(TXT_WITH_RECEPIENT_FOR_RANDOM_SENDING) as file:
        list_of_addresses = [line.strip() for line in file.readlines()]

    random_wallet = random.choice(list_of_addresses)

    my_address = web3.eth.account.from_key(private_key).address

    print(f'Адресат {random_wallet}')
    
    prepared_wallet = web3.to_checksum_address(random_wallet)
    
    transaction_hash = create_sign_send_transaction(web3, my_address, prepared_wallet, 
                                                    amount, private_key)

    check_transaction_status(web3, my_address, prepared_wallet, 
                             amount, private_key, transaction_hash, 
                             transaction_type, chain_name, explorer_url,
                             min_timesleep_between_transactions, max_timesleep_between_transactions)
    
    print(f'{explorer_url}/{transaction_hash}')

    timesleep_value = create_random_timesleeps(min_timesleep_between_transactions, 
                                               max_timesleep_between_transactions)

    print(f'Пауза {timesleep_value}', '\n')

    time.sleep(timesleep_value)


def main_function(private_key):

    timesleep_value = create_random_timesleeps(MIN_TIMESLEEP_BETWEEN_MULTIPROCESSING, 
                                               MAX_TIMESLEEP_BETWEEN_MULTIPROCESSING)
    time.sleep(timesleep_value)

    
    for chain in map(chain_settings.__dict__.get, chain_settings.__all__):

        chain_tnx_counter = 0

        try:
            chain_name = chain['name']
            print(chain_name)
            print(f'Ключ {private_key}', '\n')

            web3 = create_connection(chain['url'])
            #web3 = create_testnet_connection(chain['url'], chain['port'])

            if web3.is_connected() == False:
                print(f'Соединение не установлено', '\n')
                report_table = open_csv()
                create_report(report_table, chain_name, private_key, '-', '-', '-', '-', 'Соединение не установлено') 
                
                time.sleep(5)
                continue

            print('Соединение установлено', '\n')
            time.sleep(5)

            min_amount_for_sending = chain['min_amount_for_sending']
            max_amount_for_sending = chain['max_amount_for_sending']

            blockchain_explorer_url = chain['explorer_url']
            explorer_txn_path = chain['explorer_txn_path']

            explorer_url = f'{blockchain_explorer_url}/{explorer_txn_path}'

            for transaction in range(NUMBER_OF_TRANSACTIONS):

                try:
                  amount = create_random_amount_for_sending(min_amount_for_sending, max_amount_for_sending,
                                                            NUMBER_OF_VARIATIONS_BETWEEN_SENDING_AMOUNT)

                  random.choice([self_transaction, random_transaction])(web3, amount, private_key,
                                                                        MIN_TIMESLEEP_BETWEEN_TRANSACTIONS,
                                                                        MAX_TIMESLEEP_BETWEEN_TRANSACTIONS,
                                                                        explorer_url, chain_name)

                  chain_tnx_counter += 1

                except Exception as error:
                  report_table = open_csv()
                  create_report(report_table, chain_name, private_key, '-', '-', '-', '-', error)  

                  chain_tnx_counter += 1

                  print(error,'\n')

        except Exception as error:
            report_table = open_csv()
            create_report(report_table, chain_name, private_key, '-', '-', '-', '-', error)  
            print(error,'\n')

        print(CHAIN_TNX_COUNTER_STRING.format(chain_name, chain_tnx_counter),'\n')        


