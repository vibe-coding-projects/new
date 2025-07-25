# Special Tokens Reference for 100K Tokenizer

This document defines and categorizes the special tokens used in a large-scale tokenizer for multilingual, code, reasoning, tool use, and multimodal inputs.

---

## 🔹 Core Structural Tokens

| Token | Description |
|-------|-------------|
| `<|begin_of_text|>` | Marks the start of input. Often prepended automatically. |
| `<|end_of_text|>`   | Signals the end of input or generation. Used during sampling/stopping. |
| `<|unk|>`           | Represents an unknown or out-of-vocabulary token. |

---

## 🔹 Function-In-Middle (FIM) Tokens

| Token | Description |
|-------|-------------|
| `<|fim_prefix|>`  | Start of the prefix portion in FIM tasks. |
| `<|fim_middle|>`  | Denotes where insertion should occur. |
| `<|fim_suffix|>`  | Start of suffix section to complete FIM context. |

---

## 🔹 Header Markers

| Token | Description |
|-------|-------------|
| `<|header_start|>` | Marks beginning of a metadata block or prompt header. |
| `<|header_end|>`   | Marks the end of that block. |

---

## 🔹 Training / Finetuning Tokens

| Token | Description |
|-------|-------------|
| `<|finetune_right_pad|>` | Used for models expecting right-padding. |
| `<|finetune_left_pad|>`  | Used for left-padding. |

---

## 🔹 Multi-Turn Reasoning / Conversation Tokens

| Token | Description |
|-------|-------------|
| `<think>`        | Marks the beginning of a reasoning or scratchpad block. |
| `</think>`       | Marks the end of the thinking block. |
| `<|step|>`       | Marks a logical reasoning step. |
| `<|eom|>`        | End-of-message in a chat sequence. |
| `<|eot|>`        | End-of-turn or tool invocation. |

---

## 🔹 Tool Use Tokens

| Token | Description |
|-------|-------------|
| `<tool_call>`        | Start of a tool invocation block. |
| `</tool_call>`       | End of tool call. |
| `<tool_response>`    | Start of tool's response block. |
| `</tool_response>`   | End of tool response. |

---

## 🔹 Code Delimiters

| Token | Description |
|-------|-------------|
| `<code>`     | Begins a code block. |
| `</code>`    | Ends the code block. |

---

## 🔹 Audio Tokens

| Token | Description |
|-------|-------------|
| `<|audio_start|>` | Start of audio segment. |
| `<|audio_end|>`   | End of audio segment. |
| `<|audio|>`       | Generic audio block. |
| `<|wave|>`        | Waveform segment. |
| `<|spectro|>`     | Spectrogram segment. |

---

## 🔹 Vision / Image Tokens

| Token | Description |
|-------|-------------|
| `<|sep_img|>`      | Separator between image segments. |
| `<|tile_x_sep|>`   | Separator for horizontal tiling. |
| `<|tile_y_sep|>`   | Separator for vertical tiling. |
| `<|vision_start|>` | Start of visual input. |
| `<|vision_end|>`   | End of visual input. |
| `<|image|>`        | Raw image block. |
| `<|patch|>`        | Visual patch or token chunk. |

---

## 🔹 Reserved Tokens

| Token | Description |
|-------|-------------|
| `<|reserved_token_0|>` → `<|reserved_token_24|>` | Placeholder tokens for future or custom use. |

---

## 🔹 Suggested Tokens to Consider

These are **potential additions** depending on future tasks or domain-specific extensions:

| Token | Description |
|-------|-------------|
| `<|table|>` / `</table>`       | Table block for structured data modeling. |
| `<|markdown|>` / `</markdown>` | Markdown text formatting segment. |
| `<|html|>` / `</html>`         | For web/html-aware tasks or scraping. |
| `<|latex|>` / `</latex>`       | Math equation formatting in LaTeX syntax. |
| `<|csv|>`                      | Indicates comma-separated data block. |
| `<|lang:xx|>`                  | Explicit language tag (e.g., `lang:en`, `lang:zh`). |
| `<|persona|>` / `</persona>`   | Persona block for instruction-tuned character modeling. |
| `<|task:xyz|>`                 | Task-specific instruction cue (e.g., `task:translate`, `task:summarize`). |
| `<|doc|>` / `</doc>`           | Document boundary marker for multi-doc inputs. |
| `<|section|>` / `</section>`   | For long-form content segmentation. |

---

Let me know if you want this exported as `.md`, converted to JSON/YAML, or integrated with a tokenizer class!
