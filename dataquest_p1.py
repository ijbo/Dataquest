def read_csv(file_name_csv):
    file_list = open(file_name_csv).read().split("\n")
    string_list = file_list[1:len(file_list)]
    final_list = []
    string_fields = []
    for stringL in string_list:
        string_fields.append(stringL.split(","))
    for each_list in string_fields:
        int_fields = []
        for each in each_list:
            int_fields.append(int(each))
        final_list.append(int_fields)
    return final_list

def month_births(cdc_list):
    births_per_month = {}
    month = []
    birth = []
    for val in cdc_list:
        month = val[1]
        birth = val[4]
        if month in births_per_month:
            births_per_month[month] += val[4]
        else:
            births_per_month[month] = val[4]
    return births_per_month

def calc_counts(cdc_list , column):
    births_per_month = {}
    for val in cdc_list:
        column_val = val[column]
        if column_val in births_per_month:
            births_per_month[column_val] += val[4]
        else:
            births_per_month[column_val] = val[4]
    return births_per_month


cdc_list = read_csv("US_births_1994-2003_CDC_NCHS.csv")
##print (cdc_list[0:10])
cdc_month_births = month_births(cdc_list)
##print (cdc_month_births)

cdc_year_births = calc_counts(cdc_list,0)
cdc_month_births = calc_counts(cdc_list,1)
cdc_dom_births = calc_counts(cdc_list,2)
cdc_dow_births = calc_counts(cdc_list,3)

# #print (cdc_year_births)
# #print (cdc_month_births)
# #print (cdc_dom_births)
# #print (cdc_dow_births)

#Write a function that can calculate the min and max values for any dictionary that's passed in.

def min_max_dict(dict,min = False):
    val = next(iter(dict.values()))

    for key in dict:
        if (dict[key] < val) and min:
            val_min = dict[key]
            key_min = key
            val = val_min
        if (dict[key] > val) and (min is False):
            val_max = dict[key]
            key_max = key
            val = val_max
    if min:
        val_min_d = {}
        val_min_d[key_min] = val_min
        return val_min_d
    else:
        val_max_d = {}
        val_max_d[key_max] = val_max
        return val_max_d


#birth_min = min_max_dict(cdc_year_births,True)

##print ("birth_min" , birth_min)

#Write a function that extracts the same values across years and calculates the differences
# between consecutive values to show if number of births is increasing or decreasing.
#For example, how did the number of births on Saturday change each year between 1994 and 2003?

#1. Across consecutive years.
#2. Across year .
#3. Across months.
#4. Across Week.
#5. Across Day.

#dict_val_1 first to End -1
#dict_val_2 Second to End

def diff_vals(cdc):
    dict_val_1 = {**cdc}
    del dict_val_1[list(dict_val_1.keys())[-1]]
    dict_val_2 = {**cdc}
    del dict_val_2[list(dict_val_1.keys())[0]]

    seq_dict = {}
    for key_1,key_2 in zip(dict_val_1,dict_val_2):
        if dict_val_1[key_1] > dict_val_2[key_2]:
            seq_dict[(key_1,key_2)] = "Decrease"
        elif dict_val_1[key_1] < dict_val_2[key_2]:
            seq_dict[(key_1,key_2)] = "Increase"
        elif dict_val_1[key_1] == dict_val_2[key_2]:
            seq_dict[(key_1, key_2)] = "Same"
    return seq_dict

# dict_val_1 = {**cdc_year_births}
# del dict_val_1[list(dict_val_1.keys())[-1]]
#
# dict_val_2 = {**cdc_year_births}
# del dict_val_2[list(dict_val_1.keys())[0]]

compare_dict = diff_vals(cdc_year_births)
# #print (compare_dict)

compare_dict_mnt = diff_vals(cdc_month_births)
# #print (compare_dict_mnt)


def dict_idx(cdc_list,idx,sum_col):
    dict_idx = {**idx}
    cdc_full = {}
    keep_str = []
    for val in cdc_list:
        val_Flag = 0
        key_val = []
        for key in dict_idx:
            key_val.append(val[key])
        # #print(key_val)
        str1 = ''.join(str(e) for e in key_val)
        # #print("results",str1)
        for key in dict_idx:
            #print("key",key)
            if (val[key] in key_val) :
                # #print ("match")
                val_Flag += 1
                if val_Flag == len(key_val):
                    # #print ("val_Flag",val_Flag)
                    # #print ("abc",str1,val[4])
                    cdc_full[str1] += val[sum_col]
                    # #print("cdc_full[(str1)]if", repr(cdc_full[(str1)]))
                else:
                    if str1 not in keep_str:
                        cdc_full[str1] = 0
                    keep_str.append(str1)
    return cdc_full


abc = dict_idx(cdc_list,{0:"year",1:"month",3:"week"},4)
print (abc)
