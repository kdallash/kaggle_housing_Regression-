def main():
    prices =[2,4,1]
    print(maxProfit(prices))
def isSubsequence( s: str, t: str) -> bool:
        S,T =len(s) , len(t)
        j = 0
        if S > T:return False
        if S == 0 :return True
        for i  in t:
            if i == s[j]:
                if j >= S-1:
                    return True
                j += 1
        return True

def check(f):
    def helper(x):
        if type(x) == int and x > 0 and x:
            return f(x)
        else:print("╰(*°▽°*)╯")
    return helper   
def check2(ff):

    def game(f):
        print("game")
        
    return game
import time
import threading
from threading import Thread

def sleepMe(i):
    print("Thread %i will sleep." % i)
    time.sleep(5)
    print("Thread %i is awake" % i)


@check2
def factorial(number):
    if number == 1: return 1
    return number * factorial(number - 1)
def mergeAlternately( word1: str, word2: str) -> str:
        merged = []
        i = 0 
        while i >= len(word1) or i >= len(word2):
            merged.append(word1[i]) 
            merged.append(word2[i])
            i += 1
            
        if i >= len(word1):
            merged.apend(word2[i:])
        else:
            merged.append(word1[i:])
            
        return merged 
def a():
    print ("in a")

def maxProfit(prices):
        buy_price = sell_price = prices[0]
        n = len(prices)
        for i  in range(n - 1):
            if prices[i + 1]  < buy_price and i != n - 2:
                buy_price = prices[i + 1]
                sell_price = prices[i + 1]
            if prices[i + 1] > sell_price:
                sell_price = prices[i + 1]
        if sell_price == buy_price:
            return 0 
        return sell_price - buy_price 
if __name__=="__main__":
    main() 
