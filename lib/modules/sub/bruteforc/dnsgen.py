#!/usr/bin/env python
# -- coding:utf-8
"""
前言：切勿将本工具和技术用于网络犯罪，三思而后行！
文件描述： https://github.com/ProjectAnte/dnsgen
"""
import itertools
import re

WORDS = None
NUM_COUNT = 3

def create_registrar():
	'''
	Create function registration decorator
	'''

	registry = []
	def registrar(func):
		registry.append(func)
		return func

	registrar.members = registry
	return registrar

# Create two types of permutator classes
# PERMUTATOR -> used as basic class, includes every possible permutator
# FAST_PERMUTATOR -> used for quick enumerations, mainly for huge scopes
PERMUTATOR = create_registrar()
FAST_PERMUTATOR = create_registrar()

def partiate_domain(subdomain: str, root_domain):
	'''
	Split domain base on subdomain levels.
	Root+TLD is taken as one part, regardless of its levels (example.co.uk, example.com, ...)
	'''

	# test.1.foo.example.com -> [test, 1, foo, example.com]
	# test.2.foo.example.com.cn -> [test, 2, foo, example.com.cn]
	# test.example.co.uk -> [test, example.co.uk]
	domain = subdomain.lower().rstrip(f".{root_domain}")
	parts = domain.split('.')
	parts.append(root_domain)
	return parts

@PERMUTATOR
def insert_word_every_index(parts):
	'''
	Create new subdomain levels by inserting the words between existing levels
	'''

	# test.1.foo.example.com -> WORD.test.1.foo.example.com, test.WORD.1.foo.example.com, 
	#                           test.1.WORD.foo.example.com, test.1.foo.WORD.example.com, ...

	domains = []

	for w in WORDS:
		for i in range(len(parts)):
			tmp_parts = parts[:-1]
			tmp_parts.insert(i, w)
			domains.append('.'.join(tmp_parts + [parts[-1]]))

	return domains

@FAST_PERMUTATOR
@PERMUTATOR
def increase_num_found(parts):
	'''
	If number is found in existing subdomain, increase this number without any other alteration.
	'''

	# test.1.foo.example.com -> test.2.foo.example.com, test.3.foo.example.com, ...
	# test1.example.com -> test2.example.com, test3.example.com, ...
	# test01.example.com -> test02.example.com, test03.example.com, ...

	domains = []
	parts_joined = '.'.join(parts[:-1])
	digits = re.findall(r'\d{1,3}', parts_joined)

	for d in digits:
		for m in range(NUM_COUNT):
			replacement = str(int(d) + 1 + m).zfill(len(d))
			tmp_domain = parts_joined.replace(d, replacement)
			domains.append('{}.{}'.format(tmp_domain, parts[-1]))
   
	return domains

@FAST_PERMUTATOR
@PERMUTATOR
def decrease_num_found(parts):
	'''
	If number is found in existing subdomain, decrease this number without any other alteration.
	'''

	# test.4.foo.example.com -> test.3.foo.example.com, test.2.foo.example.com, ...
	# test4.example.com -> test3.example.com, test2.example.com, ...
	# test04.example.com -> test03.example.com, test02.example.com, ...

	domains = []
	parts_joined = '.'.join(parts[:-1])
	digits = re.findall(r'\d{1,3}', parts_joined)

	for d in digits:
		for m in range(NUM_COUNT):
			new_digit = (int(d) - 1 - m)
			if new_digit < 0:
				break

			replacement = str(new_digit).zfill(len(d))
			tmp_domain = parts_joined.replace(d, replacement)
			domains.append('{}.{}'.format(tmp_domain, parts[-1]))
   
	return domains

@PERMUTATOR
def prepend_word_every_index(parts):
	'''
	On every subdomain level, prepend existing content with `WORD` and `WORD-`
	'''

	# test.1.foo.example.com -> WORDtest.1.foo.example.com, test.WORD1.foo.example.com, 
	#                           test.1.WORDfoo.example.com, WORD-test.1.foo.example.com, 
	#                           test.WORD-1.foo.example.com, test.1.WORD-foo.example.com, ...

	domains = []

	for w in WORDS:
		for i in range(len(parts[:-1])):
			# Prepend normal
			tmp_parts = parts[:-1]
			tmp_parts[i] = '{}{}'.format(w, tmp_parts[i])
			domains.append('.'.join(tmp_parts + [parts[-1]]))

			# Prepend with `-`
			tmp_parts = parts[:-1]
			tmp_parts[i] = '{}-{}'.format(w, tmp_parts[i])
			domains.append('.'.join(tmp_parts + [parts[-1]]))

	return domains

@PERMUTATOR
def append_word_every_index(parts):
	'''
	On every subdomain level, append existing content with `WORD` and `WORD-`
	'''

	# test.1.foo.example.com -> testWORD.1.foo.example.com, test.1WORD.foo.example.com, 
	#                           test.1.fooWORD.example.com, test-WORD.1.foo.example.com, 
	#                           test.1-WORD.foo.example.com, test.1.foo-WORD.example.com, ...

	domains = []

	for w in WORDS:
		for i in range(len(parts[:-1])):
			# Append Normal
			tmp_parts = parts[:-1]
			tmp_parts[i] = '{}{}'.format(tmp_parts[i], w)
			domains.append('.'.join(tmp_parts + [parts[-1]]))

			# Append with `-`
			tmp_parts = parts[:-1]
			tmp_parts[i] = '{}-{}'.format(tmp_parts[i], w)
			domains.append('.'.join(tmp_parts + [parts[-1]]))

	return domains

@FAST_PERMUTATOR
@PERMUTATOR
def replace_word_with_word(parts):
	'''
	If word longer than 3 is found in existing subdomain,
	replace it with other words from the dictionary
	'''

	# WORD1.1.foo.example.com -> WORD2.1.foo.example.com, WORD3.1.foo.example.com, 
	#                            WORD4.1.foo.example.com, ...

	# TODO: consider if the same word is found multiple times in one string

	domains = []

	for w in WORDS:
		if w in '.'.join(parts[:-1]):
			for w_alt in WORDS:
				if w == w_alt:
					continue

				domains.append('{}.{}'.format('.'.join(parts[:-1]).replace(w, w_alt), parts[-1]))

	return domains


def extract_custom_words(domains, wordlen, root_domain):
	'''
	Extend the dictionary based on target's domain naming conventions
	'''

	valid_tokens = set()

	for domain in domains:
		partition = partiate_domain(domain, root_domain)[:-1]
		tokens = set(itertools.chain(*[word.lower().split('-') for word in partition]))
		tokens = tokens.union({word.lower() for word in partition})
		for t in tokens:
			if len(t) >= wordlen:
				valid_tokens.add(t)

	return valid_tokens


def init_words(domains: list, wordlist, wordlen, fast, root_domain):
	"""
	读取置换字典
	"""

	global WORDS

	WORDS = wordlist

	if fast:
		WORDS = WORDS[:10]

	WORDS = list(set(WORDS).union(extract_custom_words(domains, wordlen, root_domain)))


def generate(domain_list, wordlist, root_domain, wordlen=5, fast=False, skip_init=False):
	"""生成器，从提供的域生成排列

	:param domain_list:
	:param wordlist:
	:param root_domain:
	:param wordlen:
	:param fast:
	:param skip_init:
	:return:
	"""
	if not skip_init:
		init_words(domain_list, wordlist, wordlen, fast, root_domain)

	for domain in set(domain_list):
		parts = partiate_domain(domain, root_domain)

		for perm in (FAST_PERMUTATOR.members if fast else PERMUTATOR.members):
			for possible_domain in perm(parts):
				yield possible_domain


def run(subdomain_list: list, wordlist: list, root_domain: str):
	"""
	执行入口
	:param root_domain: 根域名
	:param wordlist: 置换用的字典
	:param subdomain_list: 接手已存在的子域名列表
	:return: 返回生成好的 fuzz域名列表
	"""
	return generate(subdomain_list, wordlist, root_domain)
