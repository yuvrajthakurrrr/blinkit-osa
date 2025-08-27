import pandas as pd
from datetime import datetime
import time, re
from curl_cffi import requests



def run_scraper(input_file, locations_file):
    t=datetime.now()
    time_stamp=t.strftime('%Y-%m-%d')
    time_file= t.strftime('%Y_%m_%d')

    # read inputs
    df=pd.read_excel(input_file)
    codes=df['code']

    locations= pd.read_excel(locations_file)
    cities= locations['store_city']
    lats= locations['lat']
    longs= locations['long']
    stores= locations['store_code']

    result=[]

    for city,lat,long,store in zip(cities,lats,longs,stores):

        for code in codes:
            time.sleep(1)
            headers = {
                'accept': 'application/json',
                # 'accept-encoding': 'gzip, deflate, br',
                'access_token': 'v2::fff4c713-e805-4b81-b3be-12d932d6e608',
                'app_api_version': '25',
                'app_client': 'consumer_android',
                'app_version': '80160033',
                'auth_key': '45bff2b1437ff764d5e5b9b292f9771428e18fc40b7f3b7303d196ea84ab4341',
                'battery-level': 'EXCELLENT',
                'connection': 'keep-alive',
                'content-type': 'application/json; charset=UTF-8',
                'cookie': '_cfuvid=fr_AXQhYZteFM10mSa9.TfnRWVnxitvJAdteMi8gyks-1752011170662-0.0.1.1-604800000; path=/; domain=.grofers.com; HttpOnly; Secure; SameSite=None',
                'cpu-level': 'AVERAGE',
                'cur_lat': '38.9598016',
                'cur_lon': '34.9249996',
                'device_id': '3b86f17cbea38009',
                'entry_source': 'default',
                'host': 'api2.grofers.com',
                'host_app': 'blinkit',
                'is_accessibility_enabled': 'false',
                #'lat': '28.589984800000003',
                #'lon': '77.0443796',
                'lat': str(lat),
                'lon': str(long),
                'memory-level': 'AVERAGE',
                'network-level': 'LOW',
                'qd_sdk_request': 'true',
                'qd_sdk_version': '1',
                'registration_id': 'eLgx48mqSd-1GHgvgXFscO:APA91bH5F3QX6ockWI6WcyziRl-glz0iUXi9igBHNYJQ98PSE1UEbZIjv_Ks0BUsam5QCu_1p0kAQBRbvTc5Sd4b4zPcWrxWsBquP6ddEptsAzrLyJuNS1A',
                'rn_bundle_version': '1009002001',
                'screen_density': '1080px',
                'screen_density_num': '1.75',
                'session_uuid': '2123c3ca-6961-4e86-8d1e-6b092fc9b7c2',
                'storage-level': 'HIGH',
                'user-agent': 'com.grofers.customerapp/280160033 (Linux; U; Android 7.1.2; en_US; ASUS_I001DA; Build/N2G47H; Cronet/138.0.7156.0)',
                'version_code': '80160033',
                'version_name': '16.3.3',
                'x-app-theme': 'default',
                'x-rider-installed': 'false',
                'x-zomato-installed': 'true',
            }

            params = {
                'identity': str(code),
                'merchant_id': str(store),
                'npr_flag': 'PRODUCT_RECOMMENDATION',
                'previous_page': 'search',
                'product_card_prefix_id': '',
                'product_id': str(code),
                'product_index': '5',
            }

            url = f"https://api2.grofers.com/v1/layout/product/{code}"

            max_retries = 5
            retry_wait = 3
            success = False

            for attempt in range(max_retries):
                try:
                    resp = requests.post(
                        url,
                        headers=headers,
                        params=params,
                        json={},
                        impersonate="chrome110",
                        timeout=10
                    )
                    print(f"[Attempt {attempt + 1}] Status: {resp.status_code}")
                    #print(resp.text)
                    data = resp.json()
                    success = True
                    break
                except Exception as e:
                    print(f"[Attempt {attempt + 1}] Error fetching {code} for store {store}: {e}")
                    time.sleep(retry_wait)

            if not success:
                print(f"❌ Failed after {max_retries} attempts. Continuing with blank values.")
                data = {}

            try:
                data = resp.json()
                
            #data=resp.json()
            
                try:
                    pname= data['response']["snippets"][1]["tracking"]["widget_meta"]["child_widget_title"]
                except:
                    pname= ''
                try:
                    price= data['response']["snippets"][2]["tracking"]["common_attributes"]["price"]
                except:
                    price= ''

                if price==0:
                    price=''
                else:
                    price=price

                try:
                    mrp= data['response']["snippets"][2]["tracking"]["common_attributes"]["mrp"]
                except:
                    mrp= ''

                if mrp==0:
                    mrp=''
                else:
                    mrp=mrp

                try:
                    invent= data['response']['snippets'][2]['tracking']['common_attributes']['inventory']

                    if invent=='0' or invent==0:
                        status= 'Out of Stock -'+str(invent)
                    else:
                        status= 'Add to Cart - '+str(invent)

                except:
                    status=''

                try:
                    offers=data['response']["snippets"][8]["data"]["horizontal_item_list"][0]["data"]["offers"]["items"][0]["text"]["text"]
                except:
                    offers=''

                try:
                    rating_text = data['response']["snippets"][2]["data"]["rating"]["bar"]["title"]["text"]
                    
                    rating_match = re.search(r'\|([0-9.]+)\}', rating_text)
                    rating = rating_match.group(1) if rating_match else ''

                    count_match = re.search(r'\(([\d,]+)\s+rating[s]?\)', rating_text)
                    no_of_rating = count_match.group(1).replace(',', '') if count_match else ''

                except Exception as e:
                    print("Error extracting rating info:", e)
                    rating = no_of_rating = ''

                prod_url= f'https://blinkit.com/prn/x/prid/{code}'

            except:
                #print(f"Error decoding JSON or missing keys: {e}")
                pname = price = status = mrp = rating = offers = ''
                
            extracted_data={
                'time_stamp': time_stamp,
                'platform': 'Blinkit',
                'platform_code': code,
                'pname': pname,
                'sp': price,
                'mrp': mrp,
                'rating': rating,
                'no_of_ratings': no_of_rating,
                'deal': offers,
                'seller':store,
                'location': city,
                'status_text': status,
                'prod_url': prod_url
                }
            print(extracted_data)
            result.append(extracted_data)

    
    df=pd.DataFrame(result)
    df.to_excel(f"output_{time_file}.xlsx",index=False)
    print("Data Sucessfully Saved...")

    return df

