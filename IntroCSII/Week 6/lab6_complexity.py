################################################
# Lab 6 - Algorithm Performance Analysis
# This lab is designed to help you understand time complexities:
# 
#    O(N), O(N log N), and O(N^2).
#
# Instructions:
# 1) Run the code and observe the output. Note: The last two columns should be
#    approximately the same initially.
# 2) Modify the function `duplicateSearchSorted()` so that its time complexity is O(N).
# 3) Re-run the code. The last column values should now be significantly smaller than the
#    third column.
# 4) Modify the outer loop to include larger values of `numElements` (you can increment
#    by larger steps than 2000). Continue increasing until the last row takes at least a
#    minute to run. (This threshold may vary depending on processor speed.)
# 5) In your group, determine the time complexity of sections 2, 3, 4, and 5.
#    Are they O(N), O(N log N), or O(N^2)?
# 6) Write a short report and upload it. The report should include:
#     A) Your modified `duplicateSearchSorted()` function.
#     B) Output showing performance after modification, with `numElements` set high
#        enough that the sum of all four columns in the last row is at least one minute.
#     C) Explanation of the time complexity of the algorithms in sections 2, 3, 4, and 5,
#        with justification.
################################################

import random
import time

def linearSearch(elementList, item):
    ''' 
    Performs a linear search to find the index of "item" in "elementList".
    
    Process:
    - Start at the first element of the list.
    - Compare each element to "item".
    - If a match is found, return the index of the matched element.
    - If the end of the list is reached without a match, return False.
    '''

    i = 0
    found = False
    while not found and i < len(elementList):
        if elementList[i] == item:
            found = True
        i += 1

    if not found:
        return False
    else:
        return i - 1


def binarySearch(arr, x):
    ''' 
    Performs a binary search to find the index of "x" in a sorted list "arr".
    
    NOTE: This function requires "arr" to be sorted.

    Process:
    - Define a search range with "low" and "high" indices.
    - Find the middle index of the current range.
    - If the middle element matches "x", return the index.
    - If the middle element is greater than "x", continue searching in the left half.
    - If the middle element is smaller than "x", continue searching in the right half.
    - If "x" is not found, return False.
    '''

    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:  # Search in the right half
            low = mid + 1
        else:  # Search in the left half
            high = mid - 1
    return False  # "x" is not in "arr"


def duplicateSearch(elementList):
    ''' 
    Searches for duplicate values in "elementList" and return True if found.

    Process:
    - Compare every pair of elements in the list using a nested loop.
    - The inner loop starts at "i+1" to avoid redundant comparisons.
    - If a duplicate is found, print the duplicate value and its indices.
    - If no duplicates are found, print a corresponding message.
    '''

    duplicateFound = False
    for i in range(len(elementList)):
        for j in range(i + 1, len(elementList)):  # Start at i+1 to avoid redundant checks
            if elementList[i] == elementList[j]: 
                duplicateFound = True
    
    return duplicateFound


def duplicateSearchSorted(elementList):
    ''' 
    IMPORTANT: This function currently performs an inefficient O(N^2) duplicate search. 
    Modify it to take advantage of the fact that "elementList" is sorted, allowing an O(N) solution.
    Again for emphasis: assume that "elementList" passed into this function is already sorted.

    HINT:
    - In a sorted list, any duplicate values will always appear at consecutive indices (i) and (i+1).
    '''

    duplicateFound = False
    for i in range(len(elementList)-1):
     if elementList[i] == elementList[i+1]: 
                duplicateFound = True
    
    return duplicateFound


######################## Code Execution: Running the Experiments ########################
# The outer loop runs the entire experiment for increasing values of N (numElements).
# Inside the outer loop, the code is divided into five sections:

# Section 1: Create a list of random integers.
#            - The range of generated numbers is 10,000 times the number of elements.
#            - This ensures relatively few duplicate values in the list.
# Section 2: Perform 'numElements' linear searches.
# Section 3: Perform 'numElements' binary searches.
# Section 4: Run duplicateSearch() to find duplicates in the unsorted list.
# Section 5: Run duplicateSearchSorted() to find duplicates in the sorted list.
#            - This function needs to be optimized to take advantage of sorting.
#            - Currently, it performs the same as duplicateSearch() and must be improved.
########################################################################################

print("    N\t\t Linear Search \t Binary Search \t Duplicate Search \t Sorted Dup Search")

for numElements in [5000, 10000, 15000, 35000]:

    # SECTION 1: Create and Populate Lists
    # Generate a list of 'numElements' random integers.
    # Also, create a sorted version of this list for binary search and sorted duplicate search.

    aList = []
    for i in range(numElements):
        newNum = random.randint(1, numElements * 10000)
        if i % 97 == 0:  # Save a number that exists in the list for searching later
            tempNum = newNum
        aList.append(newNum)
    
    sortedList = sorted(aList)  # Create a sorted version of aList

    # SECTION 2: Linear Search Performance Test
    # A linear search examines each element in the list one by one.
    # - If the target is found, its position is returned.
    # - If not found, False is returned.

    startTime = time.perf_counter()
    for _ in range(numElements):  # Perform 'numElements' linear searches
        searchNum = random.randint(1, numElements * 10000)
        rVal = linearSearch(aList, tempNum)
    stopTime = time.perf_counter()
    timeLinearSearch = stopTime - startTime

    # SECTION 3: Binary Search Performance Test
    # A binary search is performed on the sorted list.
    # - If the target exists, its index is returned.
    # - Otherwise, False is returned.

    startTime = time.perf_counter()
    for _ in range(numElements):  # Perform 'numElements' binary searches
        searchNum = random.randint(1, numElements * 10000)
        rVal = binarySearch(sortedList, tempNum)
    stopTime = time.perf_counter()
    timeBinarySearch = stopTime - startTime

    # SECTION 4: Duplicate Search in an Unsorted List
    # This function identifies and prints duplicate values in 'aList'.

    startTime = time.perf_counter()
    duplicateSearch(aList)
    stopTime = time.perf_counter()
    timeDupSearch = stopTime - startTime

    # SECTION 5: Optimized Duplicate Search in a Sorted List
    # This function must be optimized to leverage the sorted property of the list.
    # Specifically, when checking for duplicates, you only need to compare element i with i+1.

    startTime = time.perf_counter()
    duplicateSearchSorted(sortedList)
    stopTime = time.perf_counter()
    timeDupSearchSorted = stopTime - startTime

    # Print the results in a tabular format
    print(f"{numElements:8} \t {timeLinearSearch:8.4f} \t {timeBinarySearch:8.4f} \t {timeDupSearch:8.5f} \t {timeDupSearchSorted:8.5f}")
