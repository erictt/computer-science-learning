#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:27:36 2018

@author: eric
"""
def test_string(s):
    if not s:
        return ""
    count = 1
    currentLetter = s[0]
    result = ""
    for i in range(1, len(s)):
        if s[i] == currentLetter:
            count += 1
        else:
            result += currentLetter + str(count)
            currentLetter = s[i]
            count = 1
    result += currentLetter + str(count)
    print(result)
    return result

assert test_string("aaaabbbccd") == "a4b3c2d1"