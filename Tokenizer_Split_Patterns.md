# Tokenizer Split Patterns for Multilingual, Code, Math, and Tool Use (100K Vocab)

Below are 10 regex split patterns, each tailored for different domains—natural language, code, math, reasoning, and structured tool use.

---

### 1. **Base GPT-like Unicode Split**
Splits on contractions, letters, numbers, punctuation, and whitespace—good general-purpose baseline.
```python
SPLIT_PATTERN = r"'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"
```

---

### 2. **Code-Oriented Pattern**
Designed for parsing source code: variables, symbols, literals, and operators.
```python
SPLIT_PATTERN = r"[_a-zA-Z]+|[0-9]+|==|!=|<=|>=|->|[-+*/%&|^~<>]=?|[.,;:()\[\]{}]|\"[^\"]*\"|'[^']*'|\s+"
```

---

### 3. **Math-Aware Split**
Captures math expressions, symbols, and standard language units.
```python
SPLIT_PATTERN = r"\b\p{L}+\b|\b\p{N}+\b|[=<>±×÷^√π∑∫∞≈≠→←→←↔∈∉∪∩∅]|[^\p{L}\p{N}\s]+|\s+"
```

---

### 4. **Reasoning/Language Bias**
Keeps logical phrases like "don't", while splitting common punctuation and delimiters.
```python
SPLIT_PATTERN = r"\b\p{L}+'\p{L}+|\b\p{L}+\b|\p{N}+|[.,!?;:\"'`(){}\[\]]|\s+"
```

---

### 5. **CamelCase & Snake_Case Aware**
Handles typical programming identifier formats like `CamelCase`, `snake_case`, and `CONSTANTS`.
```python
SPLIT_PATTERN = r"[A-Z]?[a-z]+(?:[A-Z][a-z]+)*|[A-Z]+(?![a-z])|[a-z]+|[0-9]+|[_]+|[^\w\s]+|\s+"
```

---

### 6. **Multilingual Natural Language Focus**
Unicode-aware split pattern for global languages and basic contractions.
```python
SPLIT_PATTERN = r"\p{L}+('\p{L}+)?|\p{N}+|[^\p{L}\p{N}\s]+|\s+"
```

---

### 7. **Tool-Use & JSON Parsing**
Captures structural elements like brackets, booleans, and numbers for config files or tool outputs.
```python
SPLIT_PATTERN = r'"(?:\\.|[^"\\])*"|[\[\]{}:,]|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null|[^\s\p{L}\p{N}]+|\s+'
```

---

### 8. **Aggressive Punctuation Split**
Very simple and aggressive—breaks punctuation and spacing separately.
```python
SPLIT_PATTERN = r"\p{L}+|\p{N}+|[^\w\s]|[\s]+"
```

---

### 9. **Math + Code Hybrid**
Balances math and code logic, capturing operators, brackets, and numeric literals.
```python
SPLIT_PATTERN = r"[a-zA-Z_][a-zA-Z_0-9]*|[0-9]+(?:\.[0-9]+)?|==|!=|<=|>=|[-+*/=<>^%]|[\(\)\[\]{}]|[.,:;\"']|\s+"
```

---

### 10. **Unicode Category Split (Language-Agnostic)**
Relies on Unicode classes: letters (`\p{L}`), numbers (`\p{N}`), symbols (`\p{S}`), and punctuation (`\p{P}`).
```python
SPLIT_PATTERN = r"\p{L}+|\p{N}+|[\p{S}\p{P}]+|\s+"
```

---
