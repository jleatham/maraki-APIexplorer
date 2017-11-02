from meraki import meraki as m
from vars import apikey, org
from pprint import pprint
import pandas as pd
from tabulate import tabulate


def explore_next(apikey,apidata,headers,selector="none",column_name="none",justPrint=False):
    #print(len(apidata))
    if '[' in str(apidata): #quick check if there are multiple 'rows' in json, starts with '[{data},{data}]'
        df = pd.DataFrame(apidata)
    else:
        df = pd.DataFrame(apidata, index=[0]) #pandas is weird for JSON w/ only 1 'row' : '{data}'
    df.index.names = ['Selection']
    try:
        df = df[headers]
    except:
        "Can't set headers, showing all"
    print (tabulate(df, headers='keys',tablefmt="fancy_grid"))

    if not justPrint:
        user_input = input("Select the row number which contains the "+selector +" you with to explore  :  ")
        #print("Org ID = "+ str(df.iloc[1]['id']))
        data = str(df.iloc[int(user_input)][column_name])
        return data
    else:
        return "nada"

x = '1'
while (x == '1'):
    apidata = m.myorgaccess(apikey,suppressprint=True)
    # id|name|samlConsumerUrl|samlConsumerUrls
    selectedOrg = explore_next(apikey,apidata,['id','name'],"Organization","id")

    print("please select:\n1: Get List of Networks\n2: Get Licenses\n3: Get Inventory\n4: Get Templates\n5: Get SNMP Settings")
    user_input = input("##:  ")
    if user_input == '1':
        apidata = m.getnetworklist(apikey, selectedOrg, suppressprint=True)
        #configTemplateId|id|name|organizationId|tags|timeZone|type
        selectedNetwork = explore_next(apikey,apidata,['name','id','tags','timeZone','type'],"Network","id")

        apidata = m.getnetworkdetail(apikey,selectedNetwork,suppressprint=True)
        dummy = explore_next(apikey,apidata,['name','id','tags','timeZone','type'],justPrint=True)

        print("please select:\n1: Get Network Devices\n2: Update Network")
        user_input = input("##:  ")    
        if user_input =="1":
            apidata = m.getnetworkdevices(apikey,selectedNetwork,suppressprint=True)
            # Selection │ address│lanIp│lat│lng│mac │ model│ name│ networkId│serial│tags│wan1Ip│wan2Ip
            selectedDevice = explore_next(apikey,apidata,['address','lanIp','mac','model','name','serial','tags'],"Device","serial")


            apidata = m.getdevicedetail(apikey,selectedNetwork,selectedDevice,suppressprint=True)
            dummy = explore_next(apikey,apidata,['address','lanIp','mac','model','name','serial','tags'],justPrint=True)


            apidata = m.getclients(apikey,selectedDevice,suppressprint=True)
            #Selection │ description│ dhcpHostname│ id│ ip │ mac│ mdnsName │ usage │  vlan 
            selectedMac = explore_next(apikey,apidata,['description','dhcpHostname','ip','mac','usage','vlan'],"Client","mac")


            apidata = m.getclientpolicy(apikey,selectedNetwork,selectedMac,suppressprint=True)
            dummy = explore_next(apikey,apidata,['description','dhcpHostname','ip','mac','usage','vlan'],justPrint=True)
                            
        elif user_input == "2":
            user_input = input("change name? yes or no:  ")
            if user_input == "yes":
                name = input("New name: ")
                if name:
                    tz=''
                    tags=''
                    result = m.updatenetwork(apikey, selectedNetwork, name,tz,tags, suppressprint=True)
                    print(result)
            user_input = input("change TimeZone? yes or no:  ")
            if user_input == "yes":
                for item in m.tzlist:
                    print(item)
                tz = input("Copy Paste Time Zone: ")
                if tz:
                    name=''
                    tags=''
                    result = m.updatenetwork(apikey, selectedNetwork, name,tz,tags, suppressprint=True)
                    print(result)          
            user_input = input("change tags? yes or no:  ")
            if user_input == "yes":
                user_input = "1"
                tags =[]
                while (user_input is not "0"):
                    user_input = input("Enter 1 tag at a time, type 0 when done: ")
                    if user_input is not "0":
                        tags.append(user_input)
                if tags:
                    name=''
                    tz=''
                    result = m.updatenetwork(apikey, selectedNetwork, name,tz,tags, suppressprint=True)
                    print(result)

    elif user_input == '2':
        print("soon")
    elif user_input == '3':
        print("soon")
    elif user_input == '4':
        print("soon")
    elif user_input == '5':
        print("soon")
                


#top level get APIs
#   myorgaccess
#Drill down level 1
#   getnetworklist
#   gettemplates
#   getlicensestate
#   getorginventory
#   getsnmpsettings
#Drill down level 2
#   getnetworkdevices
#   getgrouppolicies
#   getnetworktrafficstats
#   getaccesspolicies
#   getairmarshal
#   getssids
#   getvlans
#Drill down level 3
#   getclients
#   getmxl3fwrules
#   getmxperf
#   getswitchports
#Drill down level 4
#   getclientpolicy