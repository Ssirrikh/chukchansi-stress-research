# Chukchansi Stress Research
Thomas Lee Collard originally described Chukchansi Yokuts as expressing penultimate primary stress, with secondary stress on all other closed syllables with raised pitch (Collard 1968). A recent paper by Jason Peed analyzed acoustic data in 2 and 3-syllable words to investigate this claim. Peed found that stress is generally a function of pitch and intensity, and acoustically verified a pitch and intensity difference between Lσσ and Hσσ words, which he analyzed as L(ˈσσ) and (ˌH)(ˈσσ) footing. He then generalized these findings to claim quantity-insensative penultimate primary stress, with secondary stress on all pre-penult heavy syllables (Peed 2019).

This paper applied similar acoustic analysis techniques to 4 and 5-syllable words recorded since that publication, in an attempt to verify Peed's generalization. An automated heavy-light analysis script was developed and used to identify eighty-five 4-syllable words for acoustic analysis. From this data, the acoustic analysis then found consistent .xX. stress across 4-syllable words, regardless of syllable weight.

Notably, this indicates a H(ˌH)(ˈσσ) pattern of stress in HHσσ words, instead of the (ˌH)(ˌH)(ˈσσ) pattern expected from a literal interpretation of prior theories, or the (ˌH)H(ˈσσ) pattern that might be expected from stress-clash avoidance. Statistical analysis of heavy-light patterns from words of all lengths was used to determine the most frequent syllable weight at each position to produce the following table:

| Most Common | Expected Footing | Extended Feet |
|------------:|-----------------:|--------------:|
|           H |              (H) |           (H) |
|          HH |             (H)H |          (H)H |
|         LHH |            L(H)H |         (LH)H |
|        LHLH |         L(H)(L)H |      (LH)(L)H |
|       LHσLH |        L(H)σ(L)H |     (LH)(σL)H |
|      LHLHLH |     L(H)L(H)(L)H |  (LH)(LH)(L)H |

> Note: σ indicates a syllable with roughly equal probability of carrying L (light) or H (heavy) weight.

Between the acoustic analysis of the 4-syllable words and the high prevalence of LH pairs in longer words, an iambic parse begins to seems like a serious possibility if the final syllable can be explained away, perhaps as an extra-metrical attachment. However, the resulting (.x)(.x)(X) pattern is indicative of right-aligned iambs, which current optimality theory does not have a method of exactly formalizing.

As ever, more data is needed. At time of writing, only two 5-syllable Chukchansi words have been recorded, and zero 6-syllable words (no words longer than six syllables have yet been attested). If more recordings are produced in the future, 5-syllable acoustic analysis in a similar vein will hopefully lead to a more accurate and concrete generalization of stress in Chukchansi Yokuts and either support or debunk the possibility of such an iambic parse.

## Repository Contents

You can read the paper as a [PDF](/Ling%20242%20Term%20Paper%20-%20Automated%20Light-Heavy%20Detection%20&%20Stress%20Analysis%20in%20Longer%20Chukchansi%20Words.docx) or [Word Doc](/Ling%20242%20Term%20Paper%20-%20Automated%20Light-Heavy%20Detection%20&%20Stress%20Analysis%20in%20Longer%20Chukchansi%20Words.pdf) directly from this repo. Citation:
> Adisasmito-Smith, N. (2026). Automated Light-Heavy Detection & Stress Analysis in Longer Chukchansi Words.

Both the [dataset](/Ling%20242%20Term%20Paper%20-%20Dataset.xlsx) and the [code](/chukchansi-sylls.py) are free to use under the [MIT Liscence](https://choosealicense.com/licenses/mit/).

## Running the Python Script for Yourself
Before running the code, grab the most recent version of the Chukchansi database as a .tsv file from the [Chukchansi Speaking Dictionary repo](https://github.com/Ssirrikh/chukchansi/tree/main/data). This paper was originally produced with the v14 dataset.

### Setting Up the Script
Place the .tsv database in the same folder as the `chukchansi-sylls.py` script. Inside the script, set the variable `INPUT_FILE` to the name of the database file, file extension included.

Columns are occasionally added to the database, so you may need to adjust some variables if you're using a more recent version than v14. If not, you can skip the rest of this section.

Open the .tsv file in MS Excel or Google Sheets, and find the first column of Chukchansi words. Back in the python script, set the variable `FORM_START` to the zero-indexed id of this column. (Column A is 0, column B is 1, and so on.) Next, find the last column of Chukchansi words, right before the sentence data begins (not every row has this form, so you may see blank cells). Count the number of consecutive columns with wordform data, then set the variable `NUM_FORMS` to this number.

### Running the Script

Change the variable `ACTIVE_CV_PATTERN` to whichever regex pattern you want to use, from RE_1SYLL to RE_8SYLL, then open a terminal and run
```
python chukchansi-sylls.py
```

To those unfamiliar with the command line, you can also pipe the output to a text file directly, instead of copy-pasting out of the terminal. However, Chukchansi uses special characters that will cause an encoding error if your operating system doesn't use UTF-8 by default. To fix that, you must toggle on `PYTHONUTF8` with one of the following:

Mac/Linux Terminal:
```
PYTHONUTF8=1 python chukchansi-sylls.py > output.txt
```

Windows Powershell:
```
$env:PYTHONUTF8=1
python chukchansi-sylls.py > output.txt
```

### Reading the Results

The first section of output prints the consonant-vowel chunking of each word, followed by the transformation process `word > consonant-vowel pattern > syllabification > heavy-light pattern`.

The second and third section tally up all scanned words by catg (part of speech) and wordform.

The final two sections count up the occurrences of each raw pattern and each masked pattern, as described in the paper. Occurences marked "ERROR_BAD_PARSE" are mostly word-medial "CVshV" sequences with ambiguous syllabification, but also include genuine bad parses due to typos in the data.
 
## References
Adisasmito-Smith, N., Wyatt, H., Wyatt, J., (2023). Chukchansi dictionary 6th edition.

Adisasmito-Smith, N., Adisasmito-Smith, N., Wyatt, H., Wyatt, J., (2026). Online Chukchansi
Speaking Dictionary. https://ssirrikh.github.io/chukchansi/speaking-dictionary

Alber, B. (2005). Clash, Lapse and Directionality. *Natural Language & Linguistic Theory*, *23*(3),
485–542.

Collord, T. L. (1968). Yokuts Grammar: Chukchansi. UC Berkeley.

Peed, J. G. (2019). *A Study of Acoustic Correlates of Syllable Stress in Chukchansi Yokuts*.
ProQuest Dissertations & Theses.