#!/usr/bin/env python3

from collections import OrderedDict

def var(prefix, rest, last_pattern):
    if len(rest) == 0:
        yield prefix

    for suffix in fenglishize(rest, last_pattern):
        yield prefix + suffix

alef = 'ا'
kolahdar = 'آ'
ye = 'ی'
vav = 'و'
consonants = 'بپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
vowels = 'اوی'
banned_cc = ['bp', 'bm', 'bv', 'by',
             'pb', 'pm', 'pv', 'py',
             'tj', 'tch', 'tj', 'tzh', 'tsh', 't', 'th', 'ty',
             'jp', 'jch', 'chkh', 'chsh', 'ch', 'chgh', 'chg', 'chhf', 'chy',
             'chp', 'chj', 'chkh', 'chsh', 'ch', 'chv', 'chh', 'chy',
             'sz', 'ssh', 'sh', 'sy',
             'dr']

def is_vowel(c):
    return c in vowels

def is_consonant(c):
    return c in consonants

def convert_consonant(c):
    m = [['b'], ['p'], ['t'], ['s'], ['j'], ['ch'], ['h'],
         ['kh'], ['d'], ['z'], ['r'], ['z'], ['zh', 'j'], ['s'],
         ['sh'], ['s'], ['z'], ['t'], ['z'], [''], ['gh', 'q'], ['f'],
         ['gh', 'q'], ['k'], ['g'], ['l'], ['m'], ['n'], ['v'], ['h'],
         ['y']]
    return dict(zip(consonants, m))[c]

def convert_vowel(v):
    m = [['a'], ['oo', 'o', 'ou'], ['i', 'ee']]
    return dict(zip(vowels, m))[v]

def remove_dups(l):
    return list(OrderedDict.fromkeys(l))

def match(pattern, word):
    def check(p, w):
        if p == 'v':
            return is_vowel(w)
        elif p == 'c':
            return is_consonant(w)
        else:
            raise ValueError('Invalid pattern.')
    return all(check(p, w) for p, w in zip(pattern, word))

def fenglishize(word, last_pattern=''):
    if len(word) == 0:
        return

    # v
    if word[0] in (alef, kolahdar):
        if not last_pattern.endswith('v'):
            yield from var('a', word[1:], 'v')
            yield from var('e', word[1:], 'v')
            yield from var('o', word[1:], 'v')

    # c
    if is_consonant(word[0]):
        if len(word) == 1:
            if last_pattern == '':
                for c in convert_consonant(word[0]):
                    yield c
        elif is_consonant(word[1]):
            if word[0] != alef or (word[0] == alef and not last_pattern.endswith('v')):
                for c in convert_consonant(word[0]):
                    yield from var(c + 'a', word[1:], 'cv')
                    yield from var(c + 'e', word[1:], 'cv')
                    yield from var(c + 'o', word[1:], 'cv')

    if len(word) < 2:
        return

    # v
    if word[0] == alef and word[1] == ye and not last_pattern.endswith('v'):
        yield from var('i', word[2:], 'v')
        yield from var('ee', word[2:], 'v')
    elif word[0] == alef and word[1] == vav and not last_pattern.endswith('v'):
        yield from var('u', word[2:], 'v')
        yield from var('oo', word[2:], 'v')
        yield from var('ou', word[2:], 'v')

    # vc
    if word[0] == alef and is_consonant(word[1]):
        for c in convert_consonant(word[1]):
            yield from var('a' + c, word[2:], 'vc')

    # cv
    if match('cv', word[:2]):
        for c in convert_consonant(word[0]):
            for v in convert_vowel(word[1]):
                yield from var(c + v, word[2:], 'vc')

    # cc
    if match('cc', word[:2]):
        for c1 in convert_consonant(word[0]):
            for c2 in convert_consonant(word[1]):
                yield from var(c1 + 'a' + c2, word[2:], 'cvc')
                yield from var(c1 + 'e' + c2, word[2:], 'cvc')
                yield from var(c1 + 'o' + c2, word[2:], 'cvc')

    if len(word) < 3:
        return

    # cvc
    if match('cvc', word[:3]):
        for c1 in convert_consonant(word[0]):
            for v in convert_vowel(word[1]):
                for c2 in convert_consonant(word[2]):
                    yield from var(c1 + v + c2, word[3:], 'cvc')

    # ccc
    if match('ccc', word[:3]):
        for c1 in convert_consonant(word[0]):
            for v in 'aeo':
                for c2 in convert_consonant(word[1]):
                    for c3 in convert_consonant(word[2]):
                        if c2 != c3 and c2 + c3 not in banned_cc:
                            yield from var(c1 + v + c2 + c3, word[3:], 'cvcc')

    if len(word) < 4:
        return

    # cvcc
    if match('cvcc', word[:4]):
        for c1 in convert_consonant(word[0]):
            for v in convert_vowel(word[1]):
                for c2 in convert_consonant(word[2]):
                    for c3 in convert_consonant(word[3]):
                        if c2 != c3 and c2 + c3 not in banned_cc:
                            yield from var(c1 + v + c2 + c3, word[4:], 'cvcc')

def main():
    print('persian> ', end='')
    per = input()
    print(remove_dups(list(fenglishize(per))))

if __name__ == '__main__':
    main()
