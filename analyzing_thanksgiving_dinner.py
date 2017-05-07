"""
This script is used to understand and analyze data in a survey about
Thanksgiving dinners accross the US
data compiled by Fivethirtyeight
https://github.com/fivethirtyeight/data/tree/master/thanksgiving-2015
"""

__author__ = 'Tamby Kaghdo'

import pandas as pd
import numpy as np
import sys

def convert_age(age_str):
    """
    transforms an string age range to an int
    :param age_str: a string representing an age range. example "30 - 44"
    :return: an int for the age. ex 30
    """
    if pd.isnull(age_str):
        return None

    # split by space and get the first element
    age = age_str.split(" ")[0]
    if "+" in age:
        age = age.replace("+", "")

    return int(age)

def convert_income(income_str):
    """
    transforms an income range to an int
    :param income_str: a string income range. ex, $100,000 to $124,999
    :return: an int income. ex, 100000
    """
    if pd.isnull(income_str):
        return None

    # split by space and get the first element
    income = income_str.split(" ")[0]

    if income == "Prefer":
        return None

    if "$" in income:
        income = income.replace("$", "")

    if "," in income:
        income = income.replace(",", "")

    return int(income)



def analyze_thanksgiving(data):
    # look at a sample of the data
    print("\n*** SAMPLE DATA ***")
    print(data.head())

    print("\n*** NUMBER OF ROWS ***")
    print(len(data))

    # display column names
    print("*** COLUMNS NAMES ***")
    print(data.columns)

    # remove any responses from people who don't celebrate thanksgiving
    print("*** Do you celebrate Thanksgiving? ***")
    print(data["Do you celebrate Thanksgiving?"].value_counts())
    data = data[data["Do you celebrate Thanksgiving?"] == "Yes"]

    print(" *** NUMBER OF REMANING ROWS ***")
    print(len(data))

    print("*** Do you celebrate Thanksgiving? ***")
    print(data["Do you celebrate Thanksgiving?"].value_counts())


    # Let's explore what main dishes people tend to eat during Thanksgiving dinner
    print("*** What is typically the main dish at your Thanksgiving dinner? ***")
    print(data["What is typically the main dish at your Thanksgiving dinner?"].value_counts())

    # Do you typically have gravy on Tofurkey?
    print("*** Do you typically have gravy on Tofurkey? ***")

    Tofurkey_df = data[data["What is typically the main dish at your Thanksgiving dinner?"] == "Tofurkey"]
    Tofurkey_df = Tofurkey_df[Tofurkey_df["Do you typically have gravy?"] == "Yes"]
    print(Tofurkey_df)
    print("Gravy on Tofurkey: ", len(Tofurkey_df))

    # lets look at desserts
    print("Apple pie:")
    print(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"].value_counts())

    print("Pumpkin pie:")
    print(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"].value_counts())

    print("Pecan pie:")
    print(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"].value_counts())

    print("People and pies:")
    ate_pies = (pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"])
    &
    pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"])
     &
     pd.isnull(data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"])
    )

    print(ate_pies.value_counts())

    # lets look at age
    print("\n*** AGE ***")
    print(data["Age"].value_counts())
    # convert age range to an int age. we are just getting the first age in the range.
    # for "45 - 59" return 45
    data["int_age"] = data["Age"].apply(convert_age)
    print(data["int_age"].describe())

    # lets look at income
    print("\n*** Income ***")
    print(data["How much total combined money did all members of your HOUSEHOLD earn last year?"].value_counts())

    data["income_int"] = data["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(convert_income)
    print(data["income_int"].describe())

    # Correlating Travel Distance And Income

    # how far people earning under 150000 will travel
    print("\n*** Income less than 150000. How far will you travel for Thanksgiving? ***")
    income_less_150000_df = data[data["income_int"] < 150000]
    print(income_less_150000_df["How far will you travel for Thanksgiving?"].value_counts())

    # how far people earning over 150000 will travel
    print("\n*** Income over  150000. How far will you travel for Thanksgiving? ***")
    income_less_150000_df = data[data["income_int"] > 150000]
    print(income_less_150000_df["How far will you travel for Thanksgiving?"].value_counts())

    # Linking Friendship And Age

    # Have you ever tried to meet up with hometown friends on Thanksgiving night?
    # and Have you ever attended a "Friendsgiving?
    print("*** AGE ***")
    friendship_pivot = pd.pivot_table(data, values="int_age", index=["Have you ever tried to meet up with hometown friends on Thanksgiving night?"], columns=['Have you ever attended a "Friendsgiving?"'], aggfunc=np.mean)
    print("\n",friendship_pivot)


    # average income of respondents for each category of Have you ever tried to meet up with
    # hometown friends on Thanksgiving night? and Have you ever attended a "Friendsgiving?
    print("*** INCOME ***")
    income_pivot = pd.pivot_table(data, values="income_int", index=["Have you ever tried to meet up with hometown friends on Thanksgiving night?"], columns=['Have you ever attended a "Friendsgiving?"'], aggfunc=np.mean)
    print("\n",income_pivot)

    # what is the most common dessert people eat?

def main():

    try:
        data_df = pd.read_csv("data/thanksgiving-2015-poll-data.csv", encoding="Latin-1")
        analyze_thanksgiving(data_df)
    except IOError as e:
        print("error loading file")
        print(e)
        sys.exit(e.errno)

if __name__ == "__main__":
    sys.exit(0 if main() else 1)