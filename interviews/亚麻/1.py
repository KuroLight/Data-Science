import re


class Solution:
    def mostFrequentWords(self, s):
        new_s = []
        for ch in s:
            if ch != ch.lower():
                new_s.append(ch.lower())
            else:
                new_s.append(ch)
        new_s = ''.join(new_s)
        words = re.split(r'[\s\'\.]', new_s)

        print(words)

        maxCount = 0
        count = {}
        for word in words:
            if word == ' ' or word == '':
                continue
            if word in count.keys():
                count[word] += 1
            else:
                count[word] = 1

            maxCount = max(maxCount, count[word])

        print(count)

        result = []
        # find the largest
        for key, value in count.items():
            if value == maxCount:
                result.append(key)

        return result


s = Solution()
string = "I am Jack and my father is Jimmy. I like wearing Jack and Jone's. "

print(s.mostFrequentWords(string))
