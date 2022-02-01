import pandas as pd
from itertools import combinations


# creating function to pass arguments
def calculate_combinations(itemset, num_combinations):
   
    list_of_combination = []
   
    for comb in combinations(itemset, num_combinations):
        
        list_of_combination.append(comb)
    return list_of_combination


# function to calculate the bound value
def calc_value(st, itemset, dictionary, n):
    value = 0.0
    for num in range(n - 1, 0, -1):
        subsets = calculate_combinations(itemset, num)
        for comb in subsets:
            ck = all(item in comb for item in st)
            if ck or st == ():
                i = int(dictionary[comb]) * pow(-1.0, (n + 1) - num)
                value += i
    if st == ():
        empty = 0
        for dict_value in dictionary.values():
            empty += int(dict_value)
        value += empty * pow(-1.0, (n + 1))

    return value


# function to obtain upper and lower bounds
def evaluate_bounds(itemset, dictionary):
    upper_bounds = []
    lower_bounds = []
    lower_bound = 0
    upper_bound = 0
    n = len(itemset)

    for index in range(len(itemset)):
        subsets = calculate_combinations(itemset, index)
        boolean_Odd = (n - len(subsets[0])) % 2
        for comb in subsets:
            if boolean_Odd:
                upper_bounds.append(calc_value(comb, itemset, dictionary, n))
            else:
                lower_bounds.append(calc_value(comb, itemset, dictionary, n))

    if max(lower_bounds) < 0:
        lower_bound = 0
    # if maxium number is 0 or greater, set lower bound to that number
    else:
        lower_bound = max(lower_bounds)

    upper_bound = min(upper_bounds)

    if lower_bound == upper_bound:
        bound = 'This Itemset is derivable'
    else:
        bound = 'This Itemset is non-derivable'

    return '{}: [{}, {}] {}'.format(itemset, lower_bound, upper_bound, bound)


# main function for exercise three
def main():
    itemset_df = pd.read_csv('itemsets.txt', header=None)
    ndi_df = pd.read_csv('ndi.txt', header=None)

    itemset_dict = {}
    for i, itemset_support in enumerate(itemset_df[0]):
        set_support_list = []
        for val in itemset_support.split(' '):
            if val == '-':
                continue
            else:
                set_support_list.append(val)
        itemset_dict[tuple(set_support_list[:-1])] = set_support_list[-1]
    ndi_dict = {}
    for i, itemset in enumerate(ndi_df[0]):
        ndi_dict[i] = itemset.split(' ')
    for itemset in ndi_dict.values():
        print(evaluate_bounds(itemset, itemset_dict))


if __name__ == '__main__':
    # calling function inside try blck to catch the eror
    try:
        main()
    except Exception as exception:
        print('exception')
        traceback.print_exc()
        print('An exception of type {0} occurred.  Arguments:\n{1!r}'.format(type(exception).__name__, exception.args));
    finally:
        print(" block is executed whether exception is handled or not')
