import json
import os

if not os.path.exists("./output"):
    os.makedirs("./output")

if not os.path.exists("./output/notification_usage_data"):
    os.makedirs("./output/notification_usage_data")

sw_results=open("./sw-results.log").readlines()
top_1m_raw = open("./top500k.csv").readlines()
top_1m={}
for line in top_1m_raw:
    if(line.strip()!=""):
        top_1m[line.strip().split(",")[1]]=int(line.strip().split(",")[0])

usage_bucket_100k=[]
usage_bucket_200k=[]
usage_bucket_300k=[]
usage_bucket_400k=[]
usage_bucket_500k=[]

custom_bucket_100k=[]
custom_bucket_200k=[]
custom_bucket_300k=[]
custom_bucket_400k=[]
custom_bucket_500k=[]

third_party_bucket_100k=[]
third_party_bucket_200k=[]
third_party_bucket_300k=[]
third_party_bucket_400k=[]
third_party_bucket_500k=[]

dynamic_bucket_100k=[]
dynamic_bucket_200k=[]
dynamic_bucket_300k=[]
dynamic_bucket_400k=[]
dynamic_bucket_500k=[]

websites={}

provider_map={"aimtell": "aimtell.com", "batch": "batch.com", "cleverpush": "cleverpush.com", "foxpush": "foxpush.com", "frizbit": "frizbit.com", "pushmonkey": "getpushmonkey.com", "gravitec": "gravitec.net", "izooto": "izooto.com", "jeeng": "jeeng.com", "killtarget": "killtarget.com", "letReach": "letreach.com", "magicbell": "magicbell.com", "najva": "najva.com", "notix": "notix.co", "oneSignal": "onesignal.com", "panneaupocket": "panneaupocket.com", "popify": "popify.app", "pushworld": "push.world", "push4site": "push4site.com", "pushalert": "pushalert.co", "pushbird": "pushbird.com", "pushe": "pushe.ru", "pushly": "pushly.com", "pushnami": "pushnami.com", "pushnews": "pushnews.eu", "pushpad": "pushpad.xyz", "pushpanda": "pushpanda.io", "pushpros": "pushpros.com", "pushpushgo": "pushpushgo.com", "pushtoast": "pushtoast.com", "pushwoosh": "pushwoosh.com", "quickblox": "quickblox.com", "subscribers": "subscribers.com", "titanpush": "titanpush.com", "truepush": "truepush.com", "vwo": "vwo.com", "webpushr": "webpushr.com", "wonderpush": "wonderpush.com", "pushengage": "pushengage.com"}

for line in sw_results:
    if line.strip()!="": # Load first measurement
        data=json.loads(line)
        websites[data["url"]]={}
        websites[data["url"]]["sw"]=data["sw"]
        websites[data["url"]]["dynamic"]=data["dynamic"]
        websites[data["url"]]["static"]=data["static"]
        websites[data["url"]]["url"]=data["url"]

third_party_results =open("./3p-measurement.part1.log").readlines()
third_party_results +=open("./3p-measurement.part2.log").readlines()
third_party_results +=open("./3p-measurement.part3.log").readlines()
third_party_results +=open("./3p-measurement.part4.log").readlines()
third_party_results +=open("./3p-measurement.part5.log").readlines()
for line in third_party_results: # Add third-party data
    if line.strip()!="":
        data=json.loads(line)
        if data["url"].rstrip("/") not in websites:
            print("Found website in 3p not in sw results")
            print(data["url"].rstrip("/"))
        else:
            websites[data["url"].rstrip("/")]["thirdParties"]=data["thirdParties"]

to_remove=[]
for url in websites.keys(): # Some websites may have been missed by either the static, dynamic, or third-party approach. We ignore those as the result is likely to be flawed
    if "thirdParties" not in websites[url] or "dynamic" not in websites[url] or "static" not in websites[url]:
        to_remove.append(url)

for url in to_remove:
    del websites[url]

third_party_list=['najva', 'letReach', 'oneSignal', 'webpushr', 'izooto', 'gravitec', 'pushengage', 'cleverpush', 'pushly', 'truepush', 'vwo', 'pushnami', 'aimtell', 'subscribers', 'wonderpush', 'pushalert', 'notix', 'pushpushgo', 'foxpush', 'batch', 'jeeng', 'pushwoosh', 'pushworld', 'push4site', 'pushpad', 'pushe', 'pushpros', 'pushmonkey', 'frizbit', 'pushpanda', 'killtarget', 'pushnews', 'pushtoast', 'titanpush', 'pushbird', 'magicbell', 'popify', 'panneaupocket', 'quickblox']
iFrame_inclusion_third_party=["cleverpush", "letReach", "pushalert", "webpushr"]
third_party_list.sort()
tot_websites=0
tot_sw=0
tot_dynamic=0
tot_static=0
tot_third_party=0
tot_iframe=0
tot_cleverpush=0
tot_push=0
tot_third_party_buckets={}
static_not_dynamic=0
third_party_not_static=0

for provider in third_party_list:
    tot_third_party_buckets[provider_map[provider]]=0

inclusion_file=open("./output/inclusion.txt", "w")
cleverpush_file=open("./output/cleverpush.txt", "w")
for website in websites.keys():
    sw = websites[website]["sw"]
    dynamic = websites[website]["dynamic"]
    static = websites[website]["static"]
    domain=website.strip().replace("https://", "").replace("http://", "").replace("/", "")
    tot_websites+=1
    if(sw): # Installs a sw?
        tot_sw+=1
    if dynamic: # Dynamic approach true?
        tot_dynamic+=1
    if static: # Static approach true?
        tot_static+=1
    third_party=False
    if("thirdParties" in websites[website]): # Just for safety
        third_party = any([websites[website]["thirdParties"][provider] for provider in third_party_list])
        iFrame_inclusion = any([websites[website]["thirdParties"][provider] for provider in iFrame_inclusion_third_party])
        cleverpush = websites[website]["thirdParties"]["cleverpush"]
        if third_party: # Any third party?
            tot_third_party+=1
        if iFrame_inclusion: # vuln?
            tot_iframe+=1
            inclusion_file.write(website+" "+str(top_1m[domain])+"\n")
        if cleverpush: # vuln?
            tot_cleverpush+=1
            cleverpush_file.write(website+" "+str(top_1m[domain])+"\n")
        for provider in third_party_list:
            if websites[website]["thirdParties"][provider]:
                tot_third_party_buckets[provider_map[provider]]+=1 # Count each
    if(dynamic or static or third_party): # Bucket splitting
        if(dynamic):
            if(not static):
                static_not_dynamic+=1
        if(third_party):
            if(not static):
                third_party_not_static+=1
        
        if(domain not in top_1m):
            print(f"{domain} is missing")
        else:
            position=top_1m[domain] # Global buckets
            if(position<100000):
                usage_bucket_100k.append(domain)
            elif(position<200000):
                usage_bucket_200k.append(domain)
            elif(position<300000):
                usage_bucket_300k.append(domain)
            elif(position<400000):
                usage_bucket_400k.append(domain)
            elif(position<500000):
                usage_bucket_500k.append(domain)
        if(third_party): # Third-party implmentation
            domain=website.strip().replace("https://", "").replace("http://", "").replace("/", "")
            position=top_1m[domain]
            if(position<100000):
                third_party_bucket_100k.append(domain)
            elif(position<200000):
                third_party_bucket_200k.append(domain)
            elif(position<300000):
                third_party_bucket_300k.append(domain)
            elif(position<400000):
                third_party_bucket_400k.append(domain)
            elif(position<500000):
                third_party_bucket_500k.append(domain)
        elif(dynamic or static): # custom implementation
            domain=website.strip().replace("https://", "").replace("http://", "").replace("/", "")
            position=top_1m[domain]
            if(position<100000):
                custom_bucket_100k.append(domain)
            elif(position<200000):
                custom_bucket_200k.append(domain)
            elif(position<300000):
                custom_bucket_300k.append(domain)
            elif(position<400000):
                custom_bucket_400k.append(domain)
            elif(position<500000):
                custom_bucket_500k.append(domain)    
        if (dynamic): # No soft-ask
            domain=website.strip().replace("https://", "").replace("http://", "").replace("/", "")
            position=top_1m[domain]
            if(position<100000):
                dynamic_bucket_100k.append(domain)
            elif(position<200000):
                dynamic_bucket_200k.append(domain)
            elif(position<300000):
                dynamic_bucket_300k.append(domain)
            elif(position<400000):
                dynamic_bucket_400k.append(domain)
            elif(position<500000):
                dynamic_bucket_500k.append(domain)    
        tot_push+=1

inclusion_file.close()
cleverpush_file.close()

print(f"Got {tot_websites} in total")
print(f"{tot_sw} websites installed a sw ({tot_sw*100/tot_websites}%)")
print(f"{tot_dynamic} websites directly asked for permission ({tot_dynamic*100/tot_websites}%)")
print(f"{tot_static} websites detected by the static approach ({tot_static*100/tot_websites}%)")
print(f"{tot_third_party} websites detected using a third-party provider ({tot_third_party*100/tot_websites}%)")
print(f"{tot_iframe} websites potentially vulnerable to the iFrame inclusion vulnerability ({tot_iframe*100/tot_websites}%)")
print(f"{tot_cleverpush} websites using vulnerable cleverpush ({tot_cleverpush*100/tot_websites}%)")
print(f"{tot_push} websites potentially use push notifications ({tot_push*100/tot_websites}%)")
print(f"Static approach false negatives (dynamic but not static): {static_not_dynamic}")
print(f"Static approach false negatives (third-party but not static): {third_party_not_static}")

for provider in third_party_list:
    print(f"{provider}: {tot_third_party_buckets[provider_map[provider]]} ({tot_third_party_buckets[provider_map[provider]]*100/tot_websites})")

with open("./output/notification_usage_data/usage.dat", "w") as f:
    f.write(f'index label cnt\n')
    f.write(f'0 "1-100k" {len(usage_bucket_100k)}\n')
    f.write(f'1 "100k-200k" {len(usage_bucket_200k)}\n')
    f.write(f'2 "200k-300k" {len(usage_bucket_300k)}\n')
    f.write(f'3 "300k-400k" {len(usage_bucket_400k)}\n')
    f.write(f'4 "400k-500k" {len(usage_bucket_500k)}\n')

with open("./output/notification_usage_data/usage2.dat", "w") as f:
    f.write(f'index label "Custom implementation" "Third-party implementation"\n')
    f.write(f'0 "1-100k" {len(custom_bucket_100k)} {len(third_party_bucket_100k)}\n')
    f.write(f'0 "100k-200k" {len(custom_bucket_200k)} {len(third_party_bucket_200k)}\n')
    f.write(f'0 "200k-300k" {len(custom_bucket_300k)} {len(third_party_bucket_300k)}\n')
    f.write(f'0 "300k-400k" {len(custom_bucket_400k)} {len(third_party_bucket_400k)}\n')
    f.write(f'0 "400k-500k" {len(custom_bucket_500k)} {len(third_party_bucket_500k)}\n')

with open("./output/notification_usage_data/dynamic.dat", "w") as f:
    f.write(f'index label cnt\n')
    f.write(f'0 "1-100k" {len(dynamic_bucket_100k)}\n')
    f.write(f'1 "100k-200k" {len(dynamic_bucket_200k)}\n')
    f.write(f'2 "200k-300k" {len(dynamic_bucket_300k)}\n')
    f.write(f'3 "300k-400k" {len(dynamic_bucket_400k)}\n')
    f.write(f'4 "400k-500k" {len(dynamic_bucket_500k)}\n')

sorted_providers=list(provider_map.values())
sorted_providers.sort()

with open("./output/notification_usage_data/third_party_table.tex", "w") as f:
    f.write("""\\begin{table}[t]
  \\centering
  % Use .5\\textwidth to only have the table fill half the page,
  % and \\textwidth for the full page
  \\resizebox{\\textwidth}{!}{
    \\begin{tabular}{ l|l }
      \\toprule
        Third-party provider &
        Number of websites \\\\
      \\midrule

 """)
    for provider in sorted_providers:
        f.write(f"        {provider} & {tot_third_party_buckets[provider]} \\\\\n")
    f.write("""     \\bottomrule
    \\end{tabular}
  }
  \\caption{Third party provider usage.}
  \\label{table:third_party_amount}
\\end{table}
""")


with open("./output/dataset.log", "w") as f:
    for website in websites.keys():
        f.write(json.dumps(websites[website])+"\n")