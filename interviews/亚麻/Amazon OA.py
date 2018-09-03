# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 17:53:13 2018

@author: wu
"""

######## find most frequent word
def wordsToExclude(text, exclude):
    from collections import defaultdict    
    wordList = set()
    for word in exclude:
        if word: wordList.add(word.lower())
    idx = 0
    wordCnt = defaultdict(int)
    maxCnt = 0
    while idx < len(text):
        if text[idx].isalpha():
            tmp = idx
            while text[tmp].isalpha(): tmp += 1
            word = text[idx:tmp].lower()
            if word not in wordList:
                wordCnt[word] += 1
                maxCnt = max(maxCnt, wordCnt[word])
            idx = tmp + 1
        else: idx += 1
    ret = []
    for word in wordCnt:
        if wordCnt[word] == maxCnt: ret.append(word)
    return ret

text = "Jack and Jill went to the market to buy bread and cheese. Cheese is Jack's and Jill's favorite food."
exclude = ['and', 'he', 'the', 'to', 'is', 'Jack', 'Jill']
print(wordsToExclude(text, exclude))

######## reorder log file
def reorderLines(logFileSize, logLines):
    from functools import cmp_to_key
    def mySort(s1, s2):
        idx1 = s1.find(' ') 
        idx2 = s2.find(' ')
        prefix1 = s1[:idx1]
        prefix2 = s2[:idx2]
        log1 = ''.join(s1[idx1+1:].split(' ')).lower()
        log2 = ''.join(s2[idx2+1:].split(' ')).lower()
        if log1 == log2:
            # tmp1, tmp2 = 0, 0
            # if prefix1 == prefix2: return -1
            # while tmp1 < idx1 or tmp2 < idx2:
            #     if tmp1 == idx1: return -1
            #     if tmp2 == idx2: return 1
            #     if ord(prefix1[tmp1]) < ord(prefix2[tmp2]): return -1
            #     if ord(prefix1[tmp1]) > ord(prefix2[tmp2]): return 1
            #     tmp1 += 1
            #     tmp2 += 1
            if prefix1 < prefix2: return -1
            return 1
        elif log1 < log2: return -1
        return 1
    
    if logFileSize == 0: return logLines
    ret = [''] * logFileSize
    alphaLines = []
    idx = logFileSize-1
    for i in reversed(range(logFileSize)):
        start = logLines[i].find(' ') + 1
        if logLines[i][start].isdigit():
            ret[idx] = logLines[i]
            idx -= 1
        else: alphaLines.append(logLines[i])
    
    alphaLines.sort(key = cmp_to_key(mySort))
    for i in range(len(alphaLines)):
        ret[i] = alphaLines[i]
    return ret

logFileSize = 5
a = ["a1 9 2 3 1", "a1c Act car", "zo4 4 7", "ab1 off KEY dog", "a1b act car"]
b = ["mi2 jog mid pet", "wz3 34 54 398", "a1 alps cow bar", "x4 45 21 7"]
c = ["t2 13 121 98", "r1 box ape bit", "b4 xi me nu", "br8 eat nim did", "w1 has uni gry", "f3 52 54 31"]
print(reorderLines(logFileSize, a))


######## DIstance between 2 nodes in BST
def findDist(bstDistance, node1, node2):
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    def findLowestCommonAncestor(root, node1, node2):
        if node1 > node2: return findLowestCommonAncestor(root, node2, node1)
        while True:
            if root.val >= node1 and root.val <= node2: return root
            if root.val < node1: root = root.right
            else: root = root.left
    def calculateDist(root, node):
        ret =  0
        while root.val != node:
            if node > root.val: root = root.right
            else: root = root.left
            ret += 1
        return ret
    
    if node1 == node2 or not bstDistance: return 0
    root = TreeNode(bstDistance[0])
    for i in range(1, len(bstDistance)):
        node = root
        while True:
            if bstDistance[i] > node.val:
                if not node.right: 
                    node.right = TreeNode(bstDistance[i])
                    break
                node = node.right
            else:
                if not node.left:
                    node.left = TreeNode(bstDistance[i])
                    break
                node = node.left
    node = findLowestCommonAncestor(root, node1, node2)
    dist1 = calculateDist(node, node1)
    dist2 = calculateDist(node, node2)
    return dist1 + dist2
    
bstDistance = [2,0,3,5,6,4,7,8,1]
node1 = 1
node2 = 4    
print(findDist(bstDistance, node1, node2))

####### Find substring with k distict characters
def findStringLengthK(input, k):
    if k == 0 or not input: return []
    exist = {}
    ret = []
    lo = 0
    for i in range(len(input)):
        if input[i] in exist:
            idx = exist[input[i]]
            for j in range(lo, idx): exist.pop(input[j])
            lo = idx+1
        else: 
            if i - lo + 1 > k: 
                exist.pop(input[lo])
                lo += 1
        exist[input[i]] = i
        if i-lo+1 == k: ret.append(input[lo:i+1])    
    return ret

input = "barfoothefoobarman"
k = 4
print(findStringLengthK(input, k))

####### Find max shipping distance with a sum not exceed  a preset value
def maxShippingDist(list1, list2, maxDist):
    if not list1 or not list1[0] or not list2 or not list2[0]: return []
    ret = []
    objectDist = 0
    for item1 in list1:
        for item2 in list2:
            if len(item1) == 2 and len(item2) == 2: 
                if item1[1] + item2[1] <= maxDist:
                    objectDist = max(objectDist, item1[1] + item2[1])
    for item1 in list1:
        for item2 in list2:
            if len(item1) == 2 and len(item2) == 2:
                if item1[1] + item2[1] == objectDist: ret.append([item1[0], item2[0]])
    return ret

list1 = [[1,3000], [2, 5000], [3, 7000], [4, 10000]]
list2 = [[1,2000], [2, 3000], [3, 4000], [4, 5000]]
maxDist = 10000
print(maxShippingDist(list1, list2, maxDist))