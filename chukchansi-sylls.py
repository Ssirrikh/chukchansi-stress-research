
import re

#### REGEX ####

MSG_ERR_INCOMPLETE_PARSE = 'ERROR_BAD_PARSE'

C = '[^aeiou\\s]' # {C}+ matches consonant cluster
V = '[aeiou]'
C_EXACT = re.compile(r'ch\'|ch|sh|[bcdfghjklmnpqrstvwxyz]\'|[bcdfghjklmnpqrstvwxyz]|ʔ', re.IGNORECASE)
V_EXACT = re.compile(r'[aeiou]', re.IGNORECASE)

RE_8SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_7SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_6SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_5SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_4SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_3SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_2SYLL = re.compile(f'^{C}*{V}+{C}+{V}+{C}*$', re.IGNORECASE)
RE_1SYLL = re.compile(f'^{C}*{V}+{C}*$', re.IGNORECASE)
RE_V_CLUSTER = re.compile(f'{V}+', re.IGNORECASE)
RE_CV_CHUNKS = re.compile(f'({C}+|{V}+)', re.IGNORECASE)
RE_SUB = re.compile(r'.+(_\d+)', re.IGNORECASE)

# RE_CV_CHUNKS = re.compile(f'({C_EXACT}|{V}+)', re.IGNORECASE)
RE_CLOSED = re.compile(f'.*VC$', re.IGNORECASE)
RE_SUPERHEAVY = re.compile('H')



################################################

#### USAGE INSTRUCTIONS ####

# Get a copy of the latest dataset from the online Chukchansi Speaking
# Dictionary and save it in the same directory as this python script.
# Set the variable INPUT_NAME to the name of the saved file.

# https://ssirrikh.github.io/chukchansi/speaking-dictionary

# Get the zero-indexed id of whatever column has Form 1 in it.
# Column A is 0, B is 1, etc. Set the variable FORM_START to this value.
# Set the variable NUM_FORMS to the highest form number in the spreadsheet.
# (ie 10, if Form 10 is the rightmost form)

# Set ACTIVE_CV_PATTERN to the regex for whatever number of syllables you want
# to filter for. For example, ACTIVE_CV_PATTERN = RE_4SYLL will run the script
# on only 4-syllable words.

# Then, open a terminal in the same directory as the script and run
# "python chukchansi-sylls.py"

INPUT_FILE = 'eng-chk-2026.tsv' # name of database file
FORM_START = 6 # column in tsv file of first form (zero-indexed)
NUM_FORMS = 10 # total number of forms

ACTIVE_CV_PATTERN = RE_2SYLL # which regex / syllable length to filter for



#### DEBUG ####

# test_words = ['abababa','abbaababa','baebabebe','eebabebeeb','ashasahall','agg','bababababa','had ababa']
# for word in test_words:
# 	print(word, RE_4SYLL.match(word))

#test_patterns = ['CV','CVC','CVCV','CVCVC','CVCCV','VCV']
# ['CV','CVC','CV.CV','CV.CVC','CVC.CV','V.CV']
# onset always >> coda
# suppose we parse "CVCV"
	# scan "C": no-op
	# scan "CV": potential syll
	# scan "CVC": potential syll
	# scan "CVCV": syll(CV), buffer(CV)

# test_pattern = 'CVCCVC'
# test_ptr = 3
# head = test_pattern[:test_ptr]
# peek = test_pattern[test_ptr]
# rest = test_pattern[test_ptr+1:]
# print(f'{head}|{peek}|{rest}')



#########################################

#### CORE FUNCTIONALITY ####

# index words into buckets for tracking and calculating statistics
buckets = {} # <catg, formNum> : [...4syllWords]
pattern_counts = {}
def addWord(catg,formNum,word,hl_pattern):
	# track words
	if catg not in buckets: buckets[catg] = {}
	if formNum not in buckets[catg]: buckets[catg][formNum] = {}
	buckets[catg][formNum][word] = True # use hash map as ghetto Set()
	# track CV patterns
	if catg not in pattern_counts: pattern_counts[catg] = {}
	if formNum not in pattern_counts[catg]: pattern_counts[catg][formNum] = {}
	if hl_pattern not in pattern_counts[catg][formNum]: pattern_counts[catg][formNum][hl_pattern] = 0
	pattern_counts[catg][formNum][hl_pattern] = pattern_counts[catg][formNum][hl_pattern] + 1

# word to consonant-vowel pattern (regex chunker)
def word2CV(word):
	res = ''
	matches = re.findall(RE_CV_CHUNKS,word)
	print(matches)
	for cluster in matches:
		if RE_V_CLUSTER.match(cluster):
			# any cluster of vowels is nucleus
			if len(cluster) > 1:
				res = res + 'VV'
			else:
				res = res + 'V'
		elif cluster == 'sh':
			# VshV is ambig "Vs.hV" or "Vsh.V"
			res = res + 'sh'
		else:
			consonant_matches = re.findall(C_EXACT,cluster)
			for c in consonant_matches:
				res = res + 'C'
	return res

# syllabifier-parser (consonant-vowel pattern to syllables)
def syllabify(cv_pattern):
	buf = cv_pattern
	res = ''
	while buf != '':
		if len(buf) < 2:
			# string too short
			return MSG_ERR_INCOMPLETE_PARSE
		elif len(buf) == 2:
			# light syll "CV", else fail
			if buf == 'CV':
				res = res + '.CV'
				buf = ''
			else:
				return MSG_ERR_INCOMPLETE_PARSE
		elif len(buf) == 3:
			# heavy syll "CVC", else fail
			if buf == 'CVC':
				res = res + '.CVC'
				buf = ''
			elif buf == 'CVV':
				res = res + '.CVV'
				buf = ''
			else:
				return MSG_ERR_INCOMPLETE_PARSE
		else:
			# scan window of len 5 to check for superheavy sylls
			if len(buf) > 4:
				if buf[:5] == 'CVVCC':
					# found superheavy syllable "CVVC"
					res = res + '.CVVC'
					buf = buf[4:]
					continue # if len5 check succeeded, short-circuit len4 checks
				elif buf[:5] == 'CVVCV':
					# found heavy syllable "CVV"
					res = res + '.CVV'
					buf = buf[3:]
					continue # if len5 check succeeded, short-circuit len4 checks
			# scan window of len 4 to check for heavy sylls
			if buf[:4] == 'CVCC':
				# found heavy syllable "CVC"
				res = res + '.CVC'
				buf = buf[3:]
			elif buf[:4] == 'CVCV':
				# found light syllable "CV"
				res = res + '.CV'
				buf = buf[2:]
			else:
				return MSG_ERR_INCOMPLETE_PARSE
	# if we haven't failed, parse is good
	return res[1:] # trim unnecessary leading '.'

# syllables to heavy-light pattern
def cv2hl(sylls):
	# superheavy sylls
	res = re.sub('CVVC','H',sylls)
	# heavy sylls
	res = re.sub('CVV','H',res)
	res = re.sub('CVC','H',res)
	# light sylls
	res = re.sub('CV','L',res)
	return re.sub(r'\.','',res)

# alternate version of cv2hl() for flagging superheavy sylls (shouldn't occur)
# def cv2hl(sylls):
# 	# superheavy sylls
# 	res = re.sub('CVVC','H',sylls)
# 	# heavy sylls
# 	res = re.sub('CVV','h',res)
# 	res = re.sub('CVC','h',res)
# 	# light sylls
# 	res = re.sub('CV','l',res)
# 	return re.sub(r'\.','',res)



##############################################

#### MAIN ####

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
	lines = f.readlines()
	exit = 10
	for line in lines:
		cells = line.split('\t')
		catg = cells[1]
		for i in range(0,NUM_FORMS):
			formNum = FORM_START + i
			if cells[formNum] == '':
				continue # skip blank cells
			word = re.sub(r'_\d+','',cells[formNum]) # strip subscript
			if not ACTIVE_CV_PATTERN.match(word):
				continue # check number of sylls
			cv_pattern = word2CV(word)
			sylls = syllabify(cv_pattern)
			hl_pattern = cv2hl(sylls)
			# if RE_SUPERHEAVY.match(hl_pattern):
			# 	print(f'!!!! SUPERHEAVY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			print(f'{word} => {cv_pattern} => {sylls} => {hl_pattern}')
			addWord(catg,formNum,word,hl_pattern)
		# exit = exit - 1
		# if exit <= 0: break

	print('\n==== WORD COUNTS ====\n')
	for catg in buckets:
		print(f'CATG "{catg}":')
		for formNum in buckets[catg]:
			print(f'    form {formNum - FORM_START + 1}: {len(buckets[catg][formNum])} words matched pattern')

	print('\n==== HL PATTERNS BY CATG ====\n')
	pattern_totals = {}
	for catg in pattern_counts:
		print(f'CATG "{catg}":')
		for formNum in pattern_counts[catg]:
			print(f'    FORM "{formNum - FORM_START + 1}":')
			for hl_pattern in pattern_counts[catg][formNum]:
				print(f'        {hl_pattern} x{pattern_counts[catg][formNum][hl_pattern]}')
				if hl_pattern not in pattern_totals:
					pattern_totals[hl_pattern] = 0
				pattern_totals[hl_pattern] = pattern_totals[hl_pattern] + pattern_counts[catg][formNum][hl_pattern]

	print('\n==== HL PATTERN TOTALS ====\n')
	for hl_pattern in pattern_totals:
		print(f'{hl_pattern} x{pattern_totals[hl_pattern]}')

	print('\n==== HL PATTERN RATIOS ====\n')
	template_totals = {}
	total_valid = 0
	for hl_pattern in pattern_totals:
		if hl_pattern == MSG_ERR_INCOMPLETE_PARSE: continue
		key = f'{hl_pattern[:-2]}ss'
		if key not in template_totals: template_totals[key] = 0
		template_totals[key] += pattern_totals[hl_pattern]
		total_valid += pattern_totals[hl_pattern]
	for template in template_totals:
		print(f'{template}: {template_totals[template]} / {total_valid} ({round(100*template_totals[template]/total_valid, 1)}%)')



#################################################################

#### RESULTS ####

# 78 one-syllable words
	# H x74
	# L x1 ("xi", meaning indefinite demonstrative "that")
	# remaining 3 had bad parse (likely a typo)
# 2656 two-syllable words
	# HH x1623
	# HL x282
	# LH x454
	# LL x17
	# remaining 280 had bad parse, or ambiguous word-medial CVshV (CVs.hV or CV.shV)
# 3729 three-syll words
	# HHH x459

	# HHL x107
	# LHH x1304
	# HLH x836

	# LLH x123
	# LHL x266
	# HLL x103

	# LLL x15
	# remaining 516 had bad parse or ambig CVshV
# 1046 four-syll words
	# HHHH x7

	# LHHH x40
	# HLHH x21
	# HHLH x143
	# HHHL x0

	# LLHH x15
	# HLLH x53
	# HHLL x11
	# LHLH x516
	# LHHL x16
	# HLHL x9

	# LLLH x7
	# LLHL x2
	# LHLL x41
	# HLLL x1

	# LLLL x3
	# remaining x161 had bad parse or ambig CVshV
# 55 five-syll words
	# HHHLH x13
	# HHHLL x4

	# LHHLH x4
	# LHHLL x1
	# HHLLH x3

	# LHLHH x3
	# LHLHL x1
	# LHLLH x13
	# LLHLH x3
	# remaining x10 had bad parse or ambig CVshV
# 16 six-syll words
	# LHHHHH x1
	# HLHHLH x1
	# HHLHHL x1

	# LHLHLH x3
	# HLLHLL x1
	# LHLHLL x1

	# LHLLHL x2
	# remaining x6 had bad parse or ambig CVshV



# Hss: 1505 / 3198 (47.1%)
# Lss: 1693 / 3198 (52.9%)

# HHss: 161 / 885 (18.2%)
# LHss: 613 / 885 (69.3%)
# HLss: 84 / 885 (9.5%)
# LLss: 27 / 885 (3.1%)

# LHLss: 17 / 45 (37.8%)
# HHHss: 17 / 45 (37.8%)
# LLHss:  3 / 45 ( 6.7%)
# LHHss:  5 / 45 (11.1%)
# HHLss:  3 / 45 ( 6.7%)

# HLLHss: 1 / 10 (10.0%)
# LHLLss: 2 / 10 (20.0%)
# HHLHss: 1 / 10 (10.0%)
# LHLHss: 4 / 10 (40.0%)
# HLHHss: 1 / 10 (10.0%)
# LHHHss: 1 / 10 (10.0%)

# [no 7 or 8 syllable words]


# https://www.geeksforgeeks.org/maths/chi-square-test/
	# X2 = sum( (O-E)^2 / E )
	# df = (number of rows - 1) × (number of columns - 1)

# 3-syll:
	# E = 3198 / 2 = 1599
	# X2 = (1505-1599)^2 / 1599 + (1693-1599)^2 / 1599 = 5.526 + 5.526 = 11.012
	# df = 1
	# crit val (p=0.05) @ 1 df is 3.841
	# 11.012 > 3.841 => X2 > crit val => p < 0.05 => distribution not even
	# there is statistically significant evidence that Chukchansi prefs prepenult L over prepenult H

# 4-syll:
	# E = 885 / 4 = 221.25
	# X2 = (158-221.25)^2 / 221.25 + (80-221.25)^2 / 221.25 + (604-221.25)^2 / 221.25 + (26-221.25)^2 / 221.25 = like 1000 or smt, way over crit val
	# df = (2-1)*(2-1) = 1
	# crit val (p=0.05) @ 1 df is 3.841
	# Chukchansi has extreme bias in favor of LH, and against LL

# 5-syll and 6-syll:
	# low number of data points, and since many possibilities aren't attested at all, a X2 test would show similar extreme bias

# borrowed words:
	# LHLH sabaaduʔun from spanish "sabado"
	# LHLH ʔorinjiʔin from english "orange"
	# HHLH ʔustuubaʔan from spanish "estufa"

# related pairs:
	# HLHL leelilaych'i
	# HLHH leelilayich'
	# HHLH gosneenotaʔ
	# HHLH gosneenoʔon