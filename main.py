#!/usr/bin/env python
# coding: utf-8

# In[159]:


import csv
import requests
import json
from bs4 import BeautifulSoup


# In[160]:


f = csv.reader(open('raw_data.csv'))
out_file = open('result.csv', 'w')
out = csv.writer(out_file)
af = csv.reader(open('auxil.csv'))


# In[161]:


url = 'http://gs.cyscc.org/Student.aspx?Aid=51&Rid=51&Cid='
def name_url(name):
    return url+name
def get_info(table):
    s = {}
    a = table.find_all('td')
    s['name'] = a[0].string
    s['school'] = a[1].string
    s['province'] = a[2].string
    s['award'] = a[3].string
    return s

def get_award_list_same_in_name(name):
    r = requests.get(name_url(name))
    soup = BeautifulSoup(r.text)
    try:
        list = soup.find_all(id="ctl00_main_DataList1")[0].find_all('tr')
    except:
        return []
    ret_list = []
    for row in list:
        ret_list.append(get_info(row))
    return ret_list
    


# In[162]:


s = {}
for row in af:
    this_name = row[1]
    s[this_name] = row[3]


# In[163]:


number_list = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零']

def is_number(charr):
    for num in number_list:
        if(charr == num):
            return 1
    return 0

def first_number_id(str):
    for id in range(len(str)):
        if(is_number(str[id])):
            return id
    return len

def last_number_id(str):
    for id in range(len(str)):
        if(is_number(str[id])):
            if(str[id+1] == '中'):
                return id+1
    return len

def exists_number(str):
    for num in number_list:
        if(num in str):
            return 1
    return 0

def complete_string(str):
    if(not '第' in str):
        if(exists_number(str)):
            try:
                return str[0:first_number_id(str)] + '第' + str[first_number_id(str):last_number_id(str)] + '中学'
    return str
    
        
    
def cmp(str1, str2):
    s1 = complete_string(str1)
    s2 = complete_string(str2)
    str1, str2 = s1, s2
    #print(str1, str2)
    if(len(str1) < len(str2)):
        str1, str2 = str2, str1
    return str2 in str1


# In[164]:


for row in f:
    this_name = row[1]
    award_list = get_award_list_same_in_name(this_name)
    ret_list = row
    try:
        ret_list.append(s[this_name])
    except:
        ret_list.append('N/A')
    award_ret_list = []
    if(len(award_list)):
        for award in award_list:
            if(cmp(award['school'], row[5])):
                award_ret_list.append(award['award'])
    if(len(award_ret_list) == 0):
        ret_list.append("N/A")
    else:
        ret_list.append(award_ret_list)
    out.writerow(ret_list)


# In[ ]:





# In[ ]:




