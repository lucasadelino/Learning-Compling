# To do:

- [x]  Create a regex that matches 500GB or more, [but not exactly 500GB](https://www.notion.so/Chapter-2-Regular-Expressions-Text-Normalization-Edit-Distance-4981f719dab04660bfa78ff1f740fa85)
- [ ]  Rewrite regex above using negative lookahead assertions
- [ ]  Review BPE algorithm
- [ ]  Document everything I did to learn the minimum edit distance algorithm (including YouTube videos, pptx slides, hand-written notes, and spreadsheet)
- [ ]  Review notes for grammar and clarity

# Notes

**Text Normalization:** basically preparing text into a form that's easier for a program to deal with. Involves:

- **Tokenization:** separating a body of text into **tokens** (words). Usually whitespace separates words from each other in languages like English, but that's not always enough: words like *New York,* for instance, might be regarded as a single token.
- **Lemmatization:** from *lemma;* figuring out which words share the same root. For instance, *sang, sung, singing* all relate to *sing*. **Stemming** is a simpler version of lemmatization which simply removes the suffixes from words. A **wordform** is the full version of a lemma (i.e. *cat* could be a lemma and *cats* a wordform).
    - The most sophisticated ways to lemmatize a corpus involve full morphological parsing (e.g. breaking down *recomeçarem* into something resembling *re-, começar-, -em;* this might also return morphological information such as *3rd person* or *future subjunctive*)
- **Sentence segmentation**

---

**Corpus**: a body of text. For instance, if you Control-F a page, you're looking for a match (of whatever you want to search) in a Corpus, which would be the entire page or document.

In the context of a corpus, there are a few different ways we can refer to words:

- **Types** are all unique words
- **Tokens** are all words, including repetitions.

So for instance, the sentence "*the quick brown fox jumps over the lazy dog"* has 8 types and 9 tokens.

---

Some new regex stuff I've learned:

- The * (zero or more) and + (one or more) symbols are called **Kleene** (pronounced *cleany*) stars and plusses, respectively.
- \b matches a word boundary; \B matches a non-boundary
- There is an order of precedence for operators. From highest to lowest precedence:
    1. Parenthesis: **( )**
    2. Counters: *** + ? { }**
    3. Sequences and anchors: **abc, ^beg, end$**
    4. Disjunction: **|**
- When you define a group using parenthesis, you can refer to that group with \n, where n is the order in which the group appeared. This is called a **capture group** (now I know why the [Pythex](https://pythex.org/) group list is called 'capture groups'!). If you don't want a group to be captured, you can use the following syntax: (:? )

---

Fixing errors in language and speech processing usually involves minimizing false positives (increasing p**recision**) ****and minimizing false negatives (increasing **recall**)

# Exercises

### Non-numbered:

**p. 8: Modify the "gigabytes" regex to only match more than 500 GB:**

In my first try, I wrote this:

```python
/\b([5-9]\d\d|[1-9]\d{3,})(\.[0-9]+)? *(GB|[Gg]igabytes?)\b/
```

However, this code will match *exactly 500GB*, which, I believe, would not be allowed. I then came up with the regex below, which will match, for instance, 500.000001GB (any fractional with a last digit ≥ 1) or greater:

```python
/((^(50[1-9]|5[1-9]\d|[6-9]\d\d|[1-9]\d{3,})(\.[0-9]+)?)|(500\.\d*[1-9]0*)) *(GB|[Gg]igabytes?)/
```

### Numbered:

1. Write regular expressions for the following languages.
    1. the set of all alphabetic strings;

        ```python
        /\b[A-Za-z]+\b/
        ```

    2. the set of all lower case alphabetic strings ending in a b;

        ```python
        /\b[a-z]*b\b/
        ```

    3. the set of all strings from the alphabet a,b such that each a is immediately preceded by and immediately followed by a b;

        I unsure how to interpret the prompt. Is it necessary for an 'a' to appear at least once? (i.e. should the regex match 'b' or only something like 'bab')? If the 'a' is not required, then the regex is as follows:

        ```python
        /\b(b+(ab)*b*)+\b/
        ```

        If the 'a' is required, then the regex is as follows:

        ```python
        /\b(b+(ab)+b*)+\b/
        ```

2. Write regular expressions for the following languages. By “word”, we mean an alphabetic string separated from other words by whitespace, any relevant punctuation, line breaks, and so forth.
    1. the set of all strings with two consecutive repeated words (e.g., “Humbert Humbert” and “the the” but not “the bug” or “the big bug”);

        ```python
        /([A-Za-z]+)[.,?!;:]*[\s\n]\1/
        ```

    2. all strings that start at the beginning of the line with an integer and that end at the end of the line with a word;

        ```python
        /^\d(.*)[A-Za-z]$/
        ```

    3. all strings that have both the word grotto and the word raven in them (but not, e.g., words like grottos that merely contain the word grotto);

        ```python
        /(.*(grotto).*(raven).*)|(.*(raven).*(grotto).*)/
        ```

    4. write a pattern that places the first word of an English sentence in a register. Deal with punctuation.

        ```python
        //
        ```

3. Implement an ELIZA-like program, using substitutions such as those described on page 10. You might want to choose a different domain than a Rogerian psychologist, although keep in mind that you would need a domain in which your program can legitimately engage in a lot of simple repetition.
4. Compute the edit distance (using insertion cost 1, deletion cost 1, substitution cost 1) of “leda” to “deal”. Show your work (using the edit distance grid).

    $\begin{array}{|c|c|c|c|c|c|}
    \hline
     & '' & D & E & A & L \\
    \hline
    '' & 0 & 1 & 2 & 3 & 4 \\
    \hline
    L & 1 & 1 & 2 & 3 & 3 \\
    \hline
    E & 2 & 2 & 1 & 2 & 3 \\
    \hline
    D & 3 & 2 & 2 & 2 & 3 \\
    \hline
    A & 4 & 3 & 3 & 2 & 3 \\
    \hline
    \end{array}$

    Edit distance = 3

5. Figure out whether drive is closer to brief or to divers and what the edit distance is to each. You may use any version of distance that you like.
6. Now implement a minimum edit distance algorithm and use your hand-computed results to check your code.

    [mineditdist.py](https://github.com/lucasadelino/Learning-Compling/blob/main/Textbooks/Speech%20and%20Language%20Processing%20(Jurafsky%2C%20Martin)/Chapter%202%20-%20Regular%20Expressions%2C%20Text%20Normalization%2C%20Edit%20Distance/mineditdist.py)

7. Augment the minimum edit distance algorithm to output an alignment; you will need to store pointers and add a stage to compute the backtrace.

    [mineditbacktrace.py](https://github.com/lucasadelino/Learning-Compling/blob/main/Textbooks/Speech%20and%20Language%20Processing%20(Jurafsky%2C%20Martin)/Chapter%202%20-%20Regular%20Expressions%2C%20Text%20Normalization%2C%20Edit%20Distance/mineditbacktrace.py)