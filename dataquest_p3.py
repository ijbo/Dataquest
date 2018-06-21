import pandas as pd
import numpy as np
import operator

# Use the pandas.read_csv() function to read the thanksgiving.csv file in.
# Make sure to specify the keyword argument encoding="Latin-1", as the CSV file isn't encoded normally.
# Assign the result to the variable data.
# Display the first few rows of data to see what the columns and rows look like.
# In a separate notebook cell, display all of the column names to get a sense of what the data consists of.
# You can use the pandas.DataFrame.columns property to display the column names.

data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")

# print (data.head(10))
# print (data.columns)

# Use the pandas.Series.value_counts() method to display counts of how many times each
# category occurs in the Do you celebrate Thanksgiving? column.
# Filter out any rows in data where the response to Do you celebrate Thanksgiving? is not Yes.
# At the end, all of the values in the Do you celebrate Thanksgiving? column of data should be Yes.

val_do = data["Do you celebrate Thanksgiving?"]
#print(val_do)
#print(val_do.value_counts())

series_val = pd.Series(val_do)

#print(series_val)
#print(series_val.value_counts())

series_val_yes = series_val[series_val=='Yes']
# print(series_val_yes)

# Use the pandas.Series.value_counts() method to display counts of how many times each category occurs
# in the What is typically the main dish at your Thanksgiving dinner? column.
# Display the Do you typically have gravy? column for any rows from data where the
# What is typically the main dish at your Thanksgiving dinner? column equals Tofurkey.
# Create a filter that only selects rows from data where What is typically the main dish
# at your Thanksgiving dinner? equals Tofurkey.
# Select the Do you typically have gravy? column, and display it.

series_val = pd.Series(data["What is typically the main dish at your Thanksgiving dinner?"])

#print (series_val.value_counts())
series_val_turkey = data[series_val=="Turkey"]
#print(series_val_turkey[["What is typically the main dish at your Thanksgiving dinner?","Do you typically have gravy?"]])


# Generate a Boolean Series indicating where the Which type of pie is typically served at your
# Thanksgiving dinner? Please select all that apply. - Apple column is null. Assign to the apple_isnull variable.
# Generate a Boolean Series indicating where the Which type of pie is typically served at your
# Thanksgiving dinner? Please select all that apply. - Pumpkin column is null. Assign to the pumpkin_isnull variable.
# Generate a Boolean Series indicating where the Which type of pie is typically served at your
# Thanksgiving dinner? Please select all that apply. - Pecan column is null. Assign to the pecan_isnull variable.
# Join all three Series using the & operator, and assign the result to no_pies.
# Display the unique values and how many times each occurs in the no_pies column.

apple_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"].isnull()
#print (apple_isnull)

pumpkin_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"].isnull()
#print (pumpkin_isnull)

pecan_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"].isnull()
#print (pecan_isnull)

no_pies = (apple_isnull & pumpkin_isnull & pecan_isnull)
#print(no_pies.value_counts())


#print (data["Age"].value_counts())

def age_str_int(age):
    if pd.isnull(age):
        return None
    age = age.split(" ")[0]
    age = age.replace("+"," ")
    return int(age)

data["int_age"] = data["Age"].apply(age_str_int)
#print(data["int_age"].describe())

#print (data["int_age"])

#print(data["How much total combined money did all members of your HOUSEHOLD earn last year?"].value_counts())

def extract_amount(earn):
    if pd.isnull(earn):
        return None
    earn_1 = earn.split(" ")[0]
    if earn_1 == 'Prefer':
        return None
    earn_2 = (earn_1.replace("$","")).replace(",","")
    return int(earn_2)

data["int_earning"] = data["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(extract_amount)

#print(data["int_earning"].describe())

#data_1 = data["int_earning"] < 150000
#print (data["How far will you travel for Thanksgiving?"][data["int_earning"] < 150000].value_counts())

#It appears that people who are younger are more likely to attend a Friendsgiving, and try to meet up with friends on Thanksgiving.
# relation between age and income wrt thanks giving

data.pivot_table(index="Have you ever tried to meet up with hometown friends on Thanksgiving night?",
                         columns='Have you ever attended a "Friendsgiving?"'
                         ,values="int_age")

# print (data.pivot_table(index="Have you ever tried to meet up with hometown friends on Thanksgiving night?",
#                         columns='Have you ever attended a "Friendsgiving?"'
#                         ,values="int_age"))
data.pivot_table(index="Have you ever tried to meet up with hometown friends on Thanksgiving night?",
                         columns='Have you ever attended a "Friendsgiving?"'
                         ,values="int_earning")
# print (data.pivot_table(index="Have you ever tried to meet up with hometown friends on Thanksgiving night?",
#                         columns='Have you ever attended a "Friendsgiving?"'
#                         ,values="int_earning"))

#Figure out the most common dessert people eat.

desert = data.loc[:,'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   ' \
                    '- Apple cobbler':'Which of these desserts do you typically have at Thanksgiving dinner? ' \
                                      'Please select all that apply.   - Other (please specify).1']
dessert_dic = dict()
#SOl:1
def common_dessert(desert):
    for val in desert.values:
        for i in val:
            if pd.notnull(i):
                # print(i)
                if i in dessert_dic:
                    dessert_dic[i] += 1
                else:
                    dessert_dic[i] = 1
    return sorted(dessert_dic.items(), key=operator.itemgetter(1), reverse=True)

print (common_dessert(desert))

#SOl:2
val_T = desert.values[pd.notnull(desert.values)]
unique, counts = np.unique(val_T, return_counts=True)
dessert = dict(zip(unique, counts))
dessert_sorted_x = sorted(dessert.items(), key=operator.itemgetter(1), reverse=True)
print(dessert_sorted_x)


#Find age, gender, and income based patterns in dinner menus.


#What is your gender
print(data["What is your gender?"])

data_val = data[pd.notnull(data["What is typically the main dish at your Thanksgiving dinner?"])]
def convert_gender_boolen(gender):
    if pd.isnull(gender):
        return None
    return 1 if gender =='Male' else 0

data_val["Gender_boolean"]= data_val["What is your gender?"].apply(convert_gender_boolen)

print(data_val)

print(data_val.pivot_table(columns="What is your gender?",
                           index="What is typically the main dish at your Thanksgiving dinner?",
                           values="Gender_boolean",
                           aggfunc=lambda x:  x.count()
                    ))

print(data_val.pivot_table(index="What is typically the main dish at your Thanksgiving dinner?",
                            columns="What is your gender?",
                            values="int_earning",
                            aggfunc= lambda  a : round(np.sum(a)/np.alen(a))

                    ))


