def pr1():
    print(""" 

public class test {

// bit wise operation 

    public static void main(String args[]) {
        int a = 60;
        int b = 13;
        int c = 0;

        c = a & b;
        System.out.println("a & b = " + c );

        c = a | b;
        System.out.println("a | b = " + c );

        c = a ^ b;
        System.out.println("a ^ b = " + c );

        c = ~a;
        System.out.println("~a = " + c );

        c = a << 2;
        System.out.println("a << 2 = " + c );

        c = a >> 2;
        System.out.println("a >> 2  = " + c );

        c = a >>> 2;      /* 15 = 0000 1111 */
        System.out.println("a >>> 2 = " + c );
    }
}
  
    
    """)

def pr2():
    print(""" 

    #Page rank algorithm

import numpy as np
import scipy as sc
import pandas as pd
from fractions import Fraction
def display_format(my_vector, my_decimal):
    return np.round((my_vector).astype(np.float), decimals=my_decimal)
my_dp = Fraction(1,3)
Mat = np.matrix([[0,0,1],
[Fraction(1,2),0,0],
[Fraction(1,2),1,0]])
Ex = np.zeros((3,3))
Ex[:] = my_dp
beta = 0.7
Al = beta * Mat + ((1-beta) * Ex)
r = np.matrix([my_dp, my_dp, my_dp])
r = np.transpose(r)
previous_r = r
for i in range(1,100):
    r = Al * r
    print (display_format(r,3))
    if (previous_r==r).all():
        break
previous_r = r
print ("Final:\n", display_format(r,3))
print ("sum", np.sum(r))
    
    """)

def pr3():
    print(""" 
#editDistance
    
def editDistance(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    if str1[m-1]== str2[n-1]:
        return editDistance(str1, str2, m-1, n-1)
    return 1 + min(editDistance(str1, str2, m, n-1),editDistance(str1, str2, m-1, n),editDistance(str1, str2, m-1, n-1) )
str1 = "aaa"
str2 = "acb"
print (editDistance(str1, str2, len(str1), len(str2)) )   
    
    """)

def pr4():
    print("""
#similarity of two documents

from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
X = input("Enter first string: ").lower()
Y = input("Enter second string: ").lower()
#X =open('file1.txt','r').read()
#Y =open('file2.txt','r').read()
# tokenization
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)
# sw contains the list of stopwords
sw = stopwords.words('english')
l1 =[];l2 =[]
# remove stop words from string
X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}
# form a set containing keywords of both strings
rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set: l1.append(1) # create a vector
    else: l1.append(0)
    if w in Y_set: l2.append(1)
    else: l2.append(0) 
c = 0
# cosine formula
for i in range(len(rvector)):
    c+= l1[i]*l2[i]
cosine = c / float((sum(l1)*sum(l2))**0.5)
print("similarity: ", cosine)

        
            """)
    
def pr5():
    print("""
#map reduce
    
Text="" "MapReduce is a processing technique and a program model for distributed
computing based on java. The MapReduce algorithm contains two important tasks, namely
Map and Reduce.
"" "
# Cleaning text and lower casing all words
for char in '-.,"\n"':
        Text=Text.replace(char,' ')
Text = Text.lower()
# split returns a list of words delimited by sequences of whitespace(including tabs, newlines, etc, like re's \s)
word_list = Text.split()
from collections import Counter
Counter(word_list).most_common()
# Initializing Dictionary
d = {}
# counting number of times each word comes up in list of words (in dictionary)
for word in word_list:
    d[word] = d.get(word, 0) + 1
#reverse the key and values so they can be sorted using tuples.
word_freq = []
for key, value in d.items():
    word_freq.append((value, key))
word_freq.sort(reverse=True)
print(word_freq)

        
            """)
    
def pr7():
    print("""  
#Web crawler
    
import requests
from bs4 import BeautifulSoup
URL = "https://en.wikipedia.org/wiki/States_and_union_territories_of_India"
res = requests.get(URL).text
soup = BeautifulSoup(res,'lxml')
states=[]
for items in soup.find('table', class_='wikitable').find_all('tr')[1::1]:
    data = items.find_all(['th','td'])
    #print(data[0].text)
    states.append(data[0].text)
    print(states)
    
""")

def pr10():
    print(""" 
#parse xml text

xml file code :
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<root testAttr="testValue">
The Tree
<children>
<child name="Jack">First</child>
<child name="Rose">Second</child>
<child name="Blue Ivy">Third<grandchildren>
<data>One</data>
<data>Two</data>
<unique>Twins</unique>
</grandchildren>
</child>
<child name="Jane">Fourth</child>
</children>
</root>

program code :

import xml.etree.ElementTree as ET
tree = ET.parse('items.xml')
root = tree.getroot()
# all items data
print('Expertise Data:')
for elem in root:
    for subelem in elem:
        print(subelem.text)

    
    """)

def pr8():
    print(""" 
#add two number
    
import tkinter as tk
 
def add():
    num1 = float(num1_entry.get())
    num2 = float(num2_entry.get())
    result = num1 + num2
    result_label.config(text=result)
 
# create the main window
root = tk.Tk()
root.title("Add Two Numbers")
 
# create the widgets
num1_label = tk.Label(root, text="Number 1:")
num1_entry = tk.Entry(root)
num2_label = tk.Label(root, text="Number 2:")
num2_entry = tk.Entry(root)
add_button = tk.Button(root, text="Add", command=add)
result_label = tk.Label(root, text="Result:")
 
# layout the widgets
num1_label.grid(row=0, column=0, sticky="e")
num1_entry.grid(row=0, column=1)
num2_label.grid(row=1, column=0, sticky="e")
num2_entry.grid(row=1, column=1)
add_button.grid(row=2, column=0, columnspan=2, pady=10)
result_label.grid(row=3, column=0, columnspan=2)
 
# run the main loop
root.mainloop()
    
    """)