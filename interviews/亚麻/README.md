# YAMA

## 1

> 给你一个String （I am Jack and my father is Jimmy. I like wearing Jack and Jone's. ）， 一个exclude list， 让你给出出现频率最高或者并列高的词(不Case sensitive, Jack和jack算一个词，都出现的话等于算jack出现两次). (而不是大家之前说的给一个k，然后求出出现频率最高的k个）, 比如Jack和Jone都是频率最高且出现三次，那么return [Jack, Jone]。这里有个很tricky的地方就是Jone's是两个词，Jone和s。 这个题很崩溃，在ide运行都是没错的，一上机就是nullpointer，最后只能含着泪提交了，最后出错的代码我贴出来，大家可以参考一下。我是把string切好然后放到hashmap里，一边加一边去除在exclude的词，然后用一个max来记录最大的频率，最后  for (Map.Entry<String, Integer> entry : map.entrySet()) {
                        if (entry.getValue() == max). more info on 1point3acres
                                ans.add(entry.getKey());
                } 来获得所有在这个map里有最大频率的词加到result list 里。. 
给了一个string，和一个要排除的list，返回频率最高的词的list，题目不难，用Map就能做，但是一定要看仔细题目。 
这题有两个版本，大小写敏感和不敏感。如果你的test case 23只能过22个的话，仔细看一下题干, 看看有没有一句话说：除了英文字母以外其他的全部算作空格，所以split string的时候记得把数字也去掉。
most frequency words
>   - 把text 都转小写， 注意记得要把不是字母的替换掉
>   - 根据空格split 字
>   - 数一遍，记录每个字的次数
>   - 找到最大的都放进vector
> 注意输入为0的edge case

## 2

