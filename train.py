from tokenizers import Tokenizer, models, pre_tokenizers, trainers, decoders, processors, Regex
from datasets import load_dataset
from huggingface_hub import login, HfApi
import json
import os

# Login to Hugging Face Hub
login(token="hf_525252fgfgfgfg525252fgfgfgf")

# Constants
SPLIT_PATTERN = r"'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"
FINAL_VOCAB_SIZE = 100000
HF_REPO_ID = "AIGym/my_tokenizer_100K"

HF_DATASETS_FOR_TRAINING = [
    ("AIGym/long-context-reasoning-v1", None, "train", "input"),
    ("AIGym/tokenizer-training-v2", None, "train", "text"),
    ("open-r1/OpenR1-Math-220k", "extended", "train", "solution"),
    ("AIGym/pretrain-data-v1", None, "train", "chosen"),
]

TOKENIZER_CONFIG_CONTENT = {
    "bos_token": "<|begin_of_text|>",
    "eos_token": "<|eot|>",
    "pad_token": "<|finetune_right_pad|>",
    "clean_up_tokenization_spaces": False,
    "model_input_names": ["input_ids", "attention_mask"],
    "chat_template": "{{- bos_token -}}\n{#-\n    To enable thinking, include '/think' in the system prompt.\n    To disable it, include '/no_think'. If neither is present, thinking is enabled by default.\n#}\\{%- set DUMMY_TOOL_RESPONSE = '[{\"role\": \"tool\", \"content\": \"\"}]' -%}\\{%- if custom_tools is defined %}\\{%- set tools = custom_tools %}\\{%- endif %}\\{%- if not tools_in_user_message is defined %}\\{%- set tools_in_user_message = true %}\\{%- endif %}\\{%- if not date_string is defined %}\\{%- if strftime_now is defined %}\\{%- set date_string = strftime_now(\"%d %b %Y\") %}\\{%- else %}\\{%- set date_string = \"26 Jul 2024\" %}\\{%- endif %}\\{%- endif %}\\{%- if not tools is defined %}\\{%- set tools = none %}\\{%- endif %}\n\n{#- This block extracts the system message and sets the reasoning mode. #}\\{%- set reasoning_mode = '/think' -%} {#- Default to thinking enabled #}\\{%- if messages[0]['role'] == 'system' %}\\{%- set system_message_text = messages[0]['content'] | trim -%}\\{%- if '/no_think' in system_message_text -%}\\{%- set reasoning_mode = '/no_think' -%}\\{%- set system_message_text = system_message_text.replace('/no_think', '') | trim -%}\\{%- elif '/think' in system_message_text -%}\\{%- set reasoning_mode = '/think' -%}\\{%- set system_message_text = system_message_text.replace('/think', '') | trim -%}\\{%- endif -%}\\{%- set messages = messages[1:] %}\\{%- else %}\\{%- set system_message_text = \"\" %}\\{%- endif %}\n\n{#- System message block #}\n{{- \"<|start_header_id|>system<|end_header_id|>\\n\\n\" -}}\\{%- if tools is not none -%}\\{{- \"Environment: ipython\\n\" -}}\\{%- endif -%}\\{{- \"Cutting Knowledge Date: December 2023\\n\" -}}\\{{- \"Today Date: \" + date_string + \"\\n\" -}}\\{{- \"Reasoning Mode: \" + reasoning_mode + \"\\n\\n\" -}}\n\n{#- Add specific instructions based on reasoning mode #}\n{%- if reasoning_mode == '/think' -%}\\{{- \"You are a helpful AI assistant. Your role is to explore questions through a systematic thinking process before providing the final precise and accurate solution. Structure your response into two sections: Thought and the final answer. Use the specified format: <think>My thought process is...</think>Here is the final answer. In the <think> section, detail your reasoning, analysis, and any steps you take. The final answer should be a direct and concise response to the user's query.\" -}}\\{%- else -%}\\{{- \"You are a helpful AI assistant. Provide a direct, concise, and accurate response to the user's query.\" -}}\\{%- endif -%}\\{{- \"\\n\\n\" -}}\n\n{#- Add user's custom instructions if they exist #}\n{%- if system_message_text is not none and system_message_text|length > 0 -%}\\{{- \"## Custom Instructions\\n\" -}}\\{{- system_message_text -}}\\{{- \"\\n\\n\" -}}\\{%- endif -%}\n\n{#- Tool definitions, if they exist and are not in the user message #}\n{%- if tools is not none and not tools_in_user_message -%}\\{{- \"You have access to the following functions. To call a function, please respond with JSON for a function call.\" -}}\\{{- ' Respond in the format {\"name\": function name, \"parameters\": dictionary of argument name and its value}.' -}}\\{{- \" Do not use variables.\\n\\n\" -}}\\{%- for t in tools -%}\\{{- t | tojson(indent=4) -}}\\{{- \"\\n\\n\" -}}\\{%- endfor -%}\\{%- endif -%}\\{{- \"<|eot|>\" -}}\n\n{#- This block handles the first user message if tools are meant to be injected there. #}\n{%- if tools_in_user_message and not tools is none %}\\{%- if messages | length != 0 %}\\{%- set first_user_message = messages[0]['content']|trim %}\\{%- set messages = messages[1:] %}\\{%- else %}\\{{- raise_exception(\"Cannot put tools in the first user message when there's no first user message!\") %}}\\{%- endif %}\\{{- '<|start_header_id|>user<|end_header_id|>\\n\\n' -}}\\{{- \"Given the following functions, please respond with a JSON for a function call \" -}}\\{{- \"with its proper arguments that best answers the given prompt.\\n\\n\" -}}\\{{- 'Respond in the format {\"name\": function name, \"parameters\": dictionary of argument name and its value}.' -}}\\{{- \" Do not use variables.\\n\\n\" -}}\\{%- for t in tools -%}\\{{- t | tojson(indent=4) -}}\\{{- \"\\n\\n\" -}}\\{%- endfor -%}\\{{- first_user_message + \"<|eot|>\"}}\\{%- endif %}\n\n{#- Main message loop #}\n{%- for message in messages %}\\{%- if not (message.role == 'ipython' or message.role == 'tool' or 'tool_calls' in message) %}\\{{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\\n\\n'+ message['content'] | trim + '<|eot|>' }}\\{%- elif 'tool_calls' in message %}\\{%- if not message.tool_calls|length == 1 %}\\{{- raise_exception(\"This model only supports single tool-calls at once!\") %}}\\{%- endif %}\\{%- set tool_call = message.tool_calls[0].function %}\\{{- '<|start_header_id|>assistant<|end_header_id|>\\n\\n<think>I should call the tool `' + tool_call.name + '` to answer the user request. The arguments are: ' + (tool_call.arguments | tojson) + '</think><tool_call>' -}}\\{{- '{\"name\": \"' + tool_call.name + '\", ' -}}\\{{- '\"parameters\": ' -}}\\{{- tool_call.arguments | tojson -}}\\{{- \"}</tool_call>\" -}}\\{{- \"<|eot|>\" }}\\{%- elif message.role == \"tool\" or message.role == \"ipython\" %}\\{{- \"<|start_header_id|>ipython<|end_header_id|>\\n\\n\" -}}\\{{- \"<tool_response>\" -}}\\{%- if message.content is mapping or message.content is iterable %}\\{{- message.content | tojson -}}\\{%- else %}\\{{- message.content -}}\\{%- endif -%}\\{{- \"</tool_response>\" -}}\\{{- \"<|eot|>\" }}\\{%- endif %}\\{%- endfor %}\n\n{#- Generation prompt #}\n{%- if add_generation_prompt %}\\{{- '<|start_header_id|>assistant<|end_header_id|>\\n\\n' -}}\\{%- if reasoning_mode == '/think' -%}\\{{- '<think>' -}}\\{%- endif -%}\\{%- endif %}\n"  # Use the full chat template string you provided earlier here.
}

# Special tokens
special_tokens = [
    '<|begin_of_text|>', '<|end_of_text|>', '<|fim_prefix|>', '<|fim_middle|>', '<|fim_suffix|>',
    '<|header_start|>', '<|header_end|>', '<|eom|>', '<|eot|>', '<|step|>',
    '<|finetune_right_pad|>', '<|finetune_left_pad|>', '<|unk|>',
    '<think>', '</think>', '<tool_call>', '</tool_call>', '<tool_response>', '</tool_response>',
    '<code>', '</code>', '<|metadata_start|>', '<|metadata_end|>', '<|audio_start|>', '<|audio_end|>', '<|audio|>', '<|wave|>', '<|spectro|>',
    '<|sep_img|>', '<|tile_x_sep|>', '<|tile_y_sep|>', '<|vision_start|>', '<|vision_end|>', '<|image|>', '<|patch|>'
]

special_tokens += [f"<|reserved_token_{i}|>" for i in range(50)]

# Step 1: Load dataset texts
def yield_training_corpus():
    for dataset_name, config_name, split, field in HF_DATASETS_FOR_TRAINING:
        dataset = load_dataset(dataset_name, name=config_name, split=split)
        for record in dataset:
            if field in record and isinstance(record[field], str):
                yield record[field]

# Step 2: Initialize a tokenizer
tokenizer = Tokenizer(models.BPE(unk_token="<|unk|>"))
tokenizer.pre_tokenizer = pre_tokenizers.Split(Regex(SPLIT_PATTERN), behavior="isolated")

trainer = trainers.BpeTrainer(vocab_size=FINAL_VOCAB_SIZE, special_tokens=special_tokens)

# Train tokenizer
tokenizer.train_from_iterator(yield_training_corpus(), trainer=trainer)

# Post-processing (optional)
tokenizer.post_processor = processors.TemplateProcessing(
    single=f"<|begin_of_text|> $A <|eot|>",
    pair=f"<|begin_of_text|> $A <|eot|> $B:1 <|eot|>:1",
    special_tokens=[
        ("<|begin_of_text|>", tokenizer.token_to_id("<|begin_of_text|>")),
        ("<|eot|>", tokenizer.token_to_id("<|eot|>")),
    ],
)

tokenizer.decoder = decoders.BPEDecoder()

# Save locally
tokenizer.save("tokenizer.json")

# Save tokenizer config
with open("tokenizer_config.json", "w") as f:
    json.dump(TOKENIZER_CONFIG_CONTENT, f, indent=2)

# Push to Hugging Face Hub
from transformers import PreTrainedTokenizerFast

fast_tokenizer = PreTrainedTokenizerFast(
    tokenizer_file="tokenizer.json",
    **TOKENIZER_CONFIG_CONTENT
)

fast_tokenizer.save_pretrained(HF_REPO_ID, push_to_hub=True)
