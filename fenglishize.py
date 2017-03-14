#!/usr/bin/env python3

import itertools
from collections import OrderedDict

def var(prefix, rest, last_pattern):
    if len(rest) == 0:
        yield prefix

    for suffix in fenglishize_word(rest, last_pattern):
        yield prefix + suffix

alef = 'ا'
kolahdar = 'آ'
ye = 'ی'
vav = 'و'
consonants = 'بپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
vowels = 'اوی'
banned_cc = ['bp', 'bm', 'bv', 'by',
             'pb', 'pm', 'pv', 'py',
             'td', 'tj', 'tch', 'tj', 'tzh', 'tsh', 't', 'th', 'ty',
             'jp', 'jch', 'chkh', 'chsh', 'ch', 'chgh', 'chq', 'chg', 'chhf', 'chy',
             'chp', 'chj', 'chkh', 'chsh', 'ch', 'chv', 'chh', 'chy',
             'khch', 'kh', 'khsh', 'khgh', 'khq', 'khk', 'khh', 'khy',
             'db', 'dp', 'dt', 'dj', 'dch', 'dsh', 'd', 'dm', 'dh', 'dy',
             'r', 'rv', 'rh', 'ry',
             'zs', 'zsh', 'z', 'zh',
             'sz', 'ssh', 'sh', 'sy',
             'shj', 'shch', 'shr', 'shz', 'shs', 'sh', 'ashy',
             'ghj', 'gh', 'ghk', 'ghg', 'ghh',
             'qj', 'q', 'qk', 'qg', 'qh',
             'kb', 'kp', 'kj', 'kch', 'kh', 'kgh', 'kq', 'kg', 'ky',
             'gb', 'gp', 'gj', 'gch', 'gkh', 'ggh', 'gq', 'gk', 'gh', 'gy',
             'lr', 'lh', 'ly',
             'mj', 'mch', 'm', 'mf', 'mk', 'mv', 'my',
             'nl', 'nm', 'ny',
             'vb', 'vp', 'vj', 'vch', 'v', 'vgh', 'vq', 'vk', 'vg', 'vh',
             'h', 'hy']

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

def fenglishize_word(word, last_pattern=''):
    if len(word) == 0:
        return

    # special case for 'va'
    if word == vav and last_pattern == '':
        yield 'va'
        yield 'o'
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
            yield from var('e' + c, word[2:], 'vc')
            yield from var('o' + c, word[2:], 'vc')

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

def fenglishize(phrase):
    result = [remove_dups(list(fenglishize_word(w))) for w in phrase.split()]
    yield from itertools.product(*result)

def main():
    print('persian> ', end='')
    persian = input()
    for variation in fenglishize(persian):
        print(' '.join(variation))

if __name__ == '__main__':
    main()
