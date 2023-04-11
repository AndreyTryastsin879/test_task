polygon = {
            'name': 'Polygon',
            'url':'https://polygon.llamarpc.com',
            'min_amount_for_sending':0.0001,
            'max_amount_for_sending':0.001,
            'min_transactions':5,
            'max_transactions':10,
            'explorer_url':'https://polygonscan.com/',
            'explorer_txn_path':'tx',
            }


bsc = {
            'name': 'Binance Smart Chain',
            'url':'https://bsc.publicnode.com',
            'min_amount_for_sending':0.0001,
            'max_amount_for_sending':0.001,
            'min_transactions':5,
            'max_transactions':10,
            'explorer_url':'https://bscscan.com/',
            'explorer_txn_path':'tx',
            }


avalanche = {
            'name': 'Avalanche',
            'url':'https://avalanche-c-chain.publicnode.com',
            'min_amount_for_sending':0.0001,
            'max_amount_for_sending':0.001,
            'min_transactions':5,
            'max_transactions':10,
            'explorer_url':'https://snowtrace.io/',
            'explorer_txn_path':'tx',
            }


arbitrum_nova = {
            'name': 'Arbitrum Nova',
            'url':'https://arbitrum-nova.public.blastapi.io',
            'min_amount_for_sending':0.0001,
            'max_amount_for_sending':0.001,
            'min_transactions':5,
            'max_transactions':10,
            'explorer_url':'https://nova.arbiscan.io/',
            'explorer_txn_path':'tx',
            }


zksync_era = {
            'name': 'Zksync Era',
            'url':'https://mainnet.era.zksync.io',
            'min_amount_for_sending':0.0001,
            'max_amount_for_sending':0.001,
            'min_transactions':5,
            'max_transactions':10,
            'explorer_url':'https://explorer.zksync.io/',
            'explorer_txn_path':'tx',
            }


__all__ = ['arbitrum_nova', 'zksync_era', 'polygon', 'bsc', 'avalanche'] 
	

#template = {
#            'name':'',
#            'symbol':'',
#            'url':'',
#            'min_value_for_sending':'',
#            'max_value_for_sending':'',
#            'explorer_url':'',
#            'explorer_txn_path':'tx',
#            }


#polygon_testnet = {
#            'name': 'Polygon',
#            'url':'https://endpoints.omniatech.io/v1/matic/mumbai/public',
#            'min_amount_for_sending':0.0001,
#            'max_amount_for_sending':0.001,
#            'min_transactions':5,
#            'max_transactions':10,
#            'explorer_url':'https://mumbai.polygonscan.com',
#            'explorer_txn_path':'tx',
#            }
#
#
#bsc_testnet = {
#        'name':'Binance Smart Chain',
#        'url':'https://bsc-testnet.public.blastapi.io',
#        'min_amount_for_sending':0.0001,
#        'max_amount_for_sending':0.001,
#        'min_transactions':5,
#        'max_transactions':10,
#        'explorer_url':'https://testnet.bscscan.com/',
#        'explorer_txn_path':'tx',
#        }
#
#
#avalanche_testnet = {
#            'name':'Avalanche',
#            'url':'https://endpoints.omniatech.io/v1/avax/fuji/public',
#            'min_amount_for_sending':0.0001,
#            'max_amount_for_sending':0.001,
#            'min_transactions':5,
#            'max_transactions':10,
#            'explorer_url':'https://testnet.snowtrace.io',
#            'explorer_txn_path':'tx',
#            }
#

#__all__ = ['polygon_testnet', 'bsc_testnet', 'avalanche_testnet']