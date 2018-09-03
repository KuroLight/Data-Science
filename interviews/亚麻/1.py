import re


class Solution:
    def mostFrequentWordsNotInExclude(self, s, ex):
        new_s = []
        for ch in s:
            if ch != ch.lower():
                new_s.append(ch.lower())
            else:
                new_s.append(ch)
        new_s = ''.join(new_s)
        words = re.split(r'[\s\'\.]', new_s)

        # print(words)
        ex = set([exx.lower() for exx in ex])

        maxCount = 0
        count = {}
        for word in words:
            if word == ' ' or word == '' or word in ex:
                continue
            if word in count.keys():
                count[word] += 1
            else:
                count[word] = 1

            maxCount = max(maxCount, count[word])

        # print(count)

        result = []
        # find the largest
        for key, value in count.items():
            if value == maxCount:
                result.append(key)

        return result


s = Solution()
string = "Jack and Jill went to the market to buy bread and cheese. Cheese is Jack's and Jill's favorite food."
exclude = ['and', 'he', 'the', 'to', 'is', 'Jack', 'Jill']
print(s.mostFrequentWordsNotInExclude(string, exclude))
