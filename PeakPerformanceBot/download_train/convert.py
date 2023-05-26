import json, re

def add_to_dic(dic, train_info, train_type):
    train = {}
    train['Mon'] = train_info[1]
    train['Tue'] = train_info[2]
    train['Wed'] = train_info[3]
    train['Thu'] = train_info[4]
    train['Fri'] = train_info[5]
    train['Sat'] = train_info[6]
    train['Sun'] = train_info[7]
    dic[train_type].append(train)
    return dic

file = open('./AI_Chatbot/PeakPerformanceBot/download_train/data.txt', 'r', encoding='utf-8')
text = file.read();
file.close()

train_dic = {}
train_dic['easy'] = []
train_dic['moderate'] = []
train_dic['hard'] = []
for train in re.findall(r"(.+)\n. - (.+)\n. - (.+)\n. - (.+)\n. - (.+)\n. - (.+)\n. - (.+)\n. - (.+)\n", text):
    train_info = re.search(r"(.+?) h.+?[,-] (.+?) km", train[0])
    train_hours = float(train_info[1])
    train_distance = float(train_info[2])

    # Easy - <10h ou <100km; Moderate - 10h-12h ou 100km-120km; # Hard - >12h ou >120km
    # print(train[0])
    if train_hours<10 or train_distance<100:
        # print(f"Easy: {train_hours}h - {train_distance}km")
        train_dic = add_to_dic(train_dic, train, 'easy')
    elif train_hours<12 or train_distance<120:
        # print(f"Moderate: {train_hours}h - {train_distance}km")
        train_dic = add_to_dic(train_dic, train, 'moderate')
    else:
        # print(f"Hard: {train_hours}h - {train_distance}km")
        train_dic = add_to_dic(train_dic, train, 'hard')
    

print(f"Easy: {len(train_dic['easy'])}; Moderate: {len(train_dic['moderate'])}; Hard: {len(train_dic['hard'])}")
file = open('./AI_Chatbot/PeakPerformanceBot/download_train/db.json', 'w', encoding='utf-8')
json.dump(train_dic, file, ensure_ascii=False, indent=4)
file.close()