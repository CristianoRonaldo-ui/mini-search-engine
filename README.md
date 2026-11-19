# Mini Search Engine

A command-line search engine that indexes local text files and ranks results using a **hand-built inverted index** and **TF-IDF scoring**, written in pure Python with no external ML libraries.

I built this to understand what libraries like scikit-learn's `TfidfVectorizer` do under the hood, after using it as a black box in my [SMS spam classifier](https://github.com/CristianoRonaldo-ui/sms-spam-classifier).

## Features

- **Tokenizer**: lowercases text, strips punctuation, and removes common stop words
- **Inverted index**: maps every word to the documents containing it, with per-document counts
- **TF-IDF ranking**: scores documents so that rare, specific words matter more than common ones
- **CLI**: search any folder of `.txt` files, with `--data` and `--top` options
- **11 pytest tests** covering tokenization, indexing, file loading, and ranking

## Getting Started

```bash
git clone https://github.com/CristianoRonaldo-ui/mini-search-engine.git
cd mini-search-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python src/cli.py "java code"
python src/cli.py "machine learning" --top 3
python src/cli.py python --data path/to/your/folder
```

Run the tests:

```bash
pytest -v
```

## Example Output

```
$ python src/cli.py "java code"
Top results for 'java code':
1. java.txt  (score: 6.949)
2. git.txt  (score: 0.511)
3. python.txt  (score: 0.511)
```

`java.txt` wins by a wide margin: "java" appears 4 times there **and** is rare across the collection (1 of 5 files), while "code" appears in 3 of 5 files, so it adds very little.

## How It Works

```
.txt files ──► tokenizer ──► inverted index ──► TF-IDF ranker ──► ranked results
```

1. **Tokenize**: `"The Cat, sat!"` → `["cat", "sat"]`
2. **Index**: build `{word: {document: count}}`, e.g. `"cat" → {"d1": 2, "d2": 1}`
3. **Score**: for each query word, add `TF × IDF` to every document that contains it

```
TF(word, doc) = number of times the word appears in the doc
IDF(word)     = log(total_documents / documents_containing_word)
```

A word found in every document gets IDF = log(1) = 0, so it adds nothing. A word found in only one document gets the highest IDF. **One rare word can outrank many common ones**, and this is verified by a test:

```python
# "bones" (rare) beats "cat" appearing twice (common)
search("cat bones", ...)  # → ["d3", "d1", "d2"]
```

## Complexity

| Operation | Time | Notes |
|---|---|---|
| Tokenize text | O(n) | n = number of characters |
| Build index | O(N) | N = total characters across all documents |
| Compute IDF | O(1) | dictionary lookup + `len()` |
| Search | O(P + k log k) | P = postings for query words, k = matching docs |

The key advantage of the inverted index: search **never scans documents that don't contain a query word**.

## Project Structure

```
mini-search-engine/
├── data/                 # sample .txt documents
├── src/
│   ├── tokenizer.py      # text → normalized words
│   ├── indexer.py        # load files + build inverted index
│   ├── ranker.py         # IDF + TF-IDF search
│   └── cli.py            # command-line entry point
├── tests/                # 11 pytest tests
├── pytest.ini
└── requirements.txt
```

## Known Limitations

- **No stemming**: "dogs" and "dog" are treated as different words, so searching `dog` misses documents that only say "dogs".
- **Apostrophes split words**: "It's" becomes `"it"` + `"s"`, leaving a meaningless `"s"` token. A test documents this on purpose.
- **Raw term counts**: TF is not normalized by document length, so very long documents can get an unfair advantage.
- **Index is rebuilt on every search**: fine for a small folder, slow for thousands of files.

## Future Improvements

- Add a simple stemmer (e.g. strip trailing "s", "ing", "ed")
- Normalize TF by document length, or switch to BM25
- Save the index to a JSON file so it is built only once
- Show a short snippet of matching text under each result

## What I Learned

- **How TF-IDF works from the inside.** I used `TfidfVectorizer` before without knowing why it worked. Writing IDF by hand showed me why a rare word like "bones" can outrank a common word that appears twice.
- **Why the inverted index matters.** Flipping "document → words" into "word → documents" turns search from scanning every file into a single dictionary lookup.
- **Edge cases find the real behavior.** Testing `tokenize("It's fast")` revealed a limitation I would never have noticed with clean example sentences.
- **Fail loudly, not silently.** Without the `is_dir()` check, a mistyped folder name would quietly return zero results. Raising `FileNotFoundError` and catching it in the CLI gives a clear one-line error instead.
- **Python's `sorted()` is stable.** When two documents tie in score, they keep their original order, which keeps results predictable and testable.
- **Floats need approximate comparison.** `pytest.approx` avoids false failures caused by tiny rounding errors.
- **Pasting multiple lines into the Python 3.13+ REPL** runs them as one block and only shows the last result, so I tested functions one line at a time.