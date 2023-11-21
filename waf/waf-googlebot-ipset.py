import json
import boto3
import urllib3

client = boto3.client('wafv2', region_name = 'ap-northeast-2')
ipsetName = 'google-special-crawlers'                               #ipset 명
ipsetId = 'ipset-guid'                                              #aws console 에서 확인
ipsetName_v6 = 'google-special-crawlers-ipv6'                       #ip v4 와 v6 는 별도 ipset을 통해 설정이 필요함
ipsetId_v6 = 'ip6set-guid'


def wafv2_update_ip_set(n,i,list):

    # ip가 포함되어 있는지 get_ip_set으로 확인
    response = client.get_ip_set(
            Name=n,
            Scope='REGIONAL',
            Id=i)
            
    for a in list:
        if a in response['IPSet']['Addresses']:
            # return 'exist ipaddress'
            ipset_ipaddrs = response['IPSet']['Addresses']
        else:
            # ip가 포함되어 있지 않으면 기존 IPset IP에 추가
            ipset_ipaddrs = response['IPSet']['Addresses']
            ipset_ipaddrs.append(a)
            print(a)
    
    # print(ipset_ipaddrs)        
    # #return ipset_ipaddrs
    response = client.update_ip_set(
            Name=n,
            Scope='REGIONAL',
            Id=i,
            Addresses=ipset_ipaddrs,             # list data
            LockToken=response['LockToken'])     # LockToken값은 get_ip_set에서 득한다.
            
    # 응답값 리턴 : 200 정상
    return response['ResponseMetadata']['HTTPStatusCode']
        
def lambda_handler(event, context):
    http = urllib3.PoolManager()
    #명시적 구글봇을 json 형태로 load
    url_googlebot = "https://developers.google.com/search/apis/ipranges/googlebot.json"
    response1 = http.request("GET", url_googlebot)
    data1 = json.loads(response1.data.decode("utf-8"))    
    prefixes1 = data1.get("prefixes", [])

    special_crawlers = "https://developers.google.com/search/apis/ipranges/special-crawlers.json"
    response2 = http.request("GET", special_crawlers)
    data2 = json.loads(response2.data.decode("utf-8"))    
    prefixes2 = data2.get("prefixes", [])

    user_triggered_fetchers = "https://developers.google.com/search/apis/ipranges/user-triggered-fetchers.json"
    response3 = http.request("GET", user_triggered_fetchers)
    data3 = json.loads(response3.data.decode("utf-8"))    
    prefixes3 = data3.get("prefixes", [])
    
    #3가지 명시적 봇을 가져온 json list를 combind 
    ipv4_combined_list = []        
    ipv4_prefixes1 = [entry['ipv4Prefix'] for entry in prefixes1 if 'ipv4Prefix' in entry]
    ipv4_prefixes2 = [entry['ipv4Prefix'] for entry in prefixes2 if 'ipv4Prefix' in entry]
    ipv4_prefixes3 = [entry['ipv4Prefix'] for entry in prefixes3 if 'ipv4Prefix' in entry]
    ipv4_combined_list = ipv4_prefixes1 + ipv4_prefixes2 + ipv4_prefixes3   

    #ip v4 waf update 
    wafv2_update_ip_set(ipsetName,ipsetId,ipv4_combined_list)

    ipv6_combined_list = []   
    ipv6_prefixes1 = [entry['ipv6Prefix'] for entry in prefixes1 if 'ipv6Prefix' in entry]
    ipv6_prefixes2 = [entry['ipv6Prefix'] for entry in prefixes2 if 'ipv6Prefix' in entry]
    ipv6_prefixes3 = [entry['ipv6Prefix'] for entry in prefixes3 if 'ipv6Prefix' in entry]
    ipv6_combined_list = ipv6_prefixes1 + ipv6_prefixes2 + ipv6_prefixes3    

    #ip v6 waf update
    wafv2_update_ip_set(ipsetName_v6,ipsetId_v6,ipv6_combined_list)