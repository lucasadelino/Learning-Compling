# To do:

- [x]  Create a regex that matches 500GB or more, [but not exactly 500GB](https://www.notion.so/Chapter-2-Regular-Expressions-Text-Normalization-Edit-Distance-4981f719dab04660bfa78ff1f740fa85)
- [ ]  Rewrite regex above using negative lookahead assertions
- [ ]  Review notes for grammar and clarity

# Notes

**Text Normalization:** basically preparing text into a form that's easier for a program to deal with. Involves:

- **Tokenization:** separating a body of text into **tokens** (words). Usually whitespace separates words from each other in languages like English, but that's not always enough: words like *New York,* for instance, might be regarded as a single token.
- **Lemmatization:** from *lemma;* figuring out which words share the same root. For instance, *sang, sung, singing* all relate to *sing*. **Stemming** is a simpler version of lemmatization which simply removes the suffixes from words. A **wordform** is the full version of a lemma (i.e. *cat* could be a lemma and *cats* a wordform)
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

1.
