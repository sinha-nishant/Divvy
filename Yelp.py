import os
from typing import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
class Yelp:
    api_key = os.environ['YELP']

    # Specifies authorization
    header = {
        'Authorization': 'bearer {}'.format(api_key),
        'Content-Type': "application/json"
    }

    # Specifies endpoint
    transport = RequestsHTTPTransport(
        url = 'https://api.yelp.com/v3/graphql',
        headers = header,
        use_json = True
    )

    client = Client(
        transport = transport,
        fetch_schema_from_transport = True
    )

    # Returns dictionary of required information about restaurant
    @staticmethod
    def search(restaurant_name : str) -> Dict:
        query = gql("""
            {
                search(term: "%s", limit: 1, latitude: 34.020176, longitude: -118.285550) {
                    business {
                        name
                        url
                        location {
                            formatted_address
                        }
                        categories {
                            title
                        }
                    }
                }
            }
            """ % restaurant_name)

        # Sends HTTP request
        response : Dict = Yelp.client.execute(query)
        response = response['search']['business'][0]
        search_result : Dict = dict()
        search_result['Name'] = response['name']
        search_result['URL'] = response['url']
        search_result['Address'] = response['location']['formatted_address'].replace('\n', ' ')
        # Transforms dict of category titles into list of categories
        search_result['Categories'] = [category['title'] for category in response['categories']]
        return search_result

from time import time as time_now
start = time_now()
print(Yelp.search('whole food'))
print(time_now() - start)