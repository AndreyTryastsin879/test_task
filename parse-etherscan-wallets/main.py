import time
import requests
from requests_html import AsyncHTMLSession


# ### Сколько страниц пагинации парсить
pagination_pages_limit = 100

set_of_addresses_from_ethescan = set()


url_template = 'https://etherscan.io/txs?p={}'

user_agent = {'User-agent': 'Mozilla/5.0'}

async def main():
    for number in range(pagination_pages_limit):
        print(f'Страница №: {number+1}')    
        response = await asession.get(url_template.format(number+1), headers=user_agent)
        print(response)
        links_from_response = response.html.links

        for link in links_from_response:
            if '/address/' in link:
                set_of_addresses_from_ethescan.add(link.strip('/address/'))
        
        time.sleep(5)


    list_of_addresses_from_ethescan = list(set_of_addresses_from_ethescan)


    new_list = []
    for address in list_of_addresses_from_ethescan:
        if len(address) == 42:
            new_list.append(address)


    print('Количество кошельков', len(new_list))


    with open("etherscan_adresses.txt", "w") as etherscan_adresses:
        etherscan_adresses.write("\n".join(new_list))

asession = AsyncHTMLSession()

result = asession.run(main)


#if __name__ == "__main__":
#    asession = AsyncHTMLSession()
#    results = asession.run(main)
    
    

