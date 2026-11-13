# Scalar Phos Prompt Template & Chat Formatting Specification

Both **Scalar Phos Pro** (based on `Llama-3.1-8B-Instruct`) and **Scalar Phos Flash** (based on `Llama-3.2-3B-Instruct`) use the native **Llama 3 Instruct** chat template. Adhering strictly to these special control tokens is essential for maintaining instruction-following accuracy, preventing runaway generation, and ensuring consistent behavior across `transformers`, `vLLM`, and `llama.cpp` / Ollama.

## Special Control Tokens

<table>
  <thead>
    <tr>
      <th style="text-align: left;">Token</th>
      <th style="text-align: left;">Role / Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;"><code>&lt;|begin_of_text|&gt;</code></td>
      <td style="text-align: left;">Beginning-of-sequence (BOS) token placed once at the start of the conversation.</td>
    </tr>
    <tr>
      <td style="text-align: left;"><code>&lt;|start_header_id|&gt;</code></td>
      <td style="text-align: left;">Opens a role header block (<code>system</code>, <code>user</code>, or <code>assistant</code>).</td>
    </tr>
    <tr>
      <td style="text-align: left;"><code>&lt;|end_header_id|&gt;</code></td>
      <td style="text-align: left;">Closes a role header block; always followed by two newlines (<code>\n\n</code>).</td>
    </tr>
    <tr>
      <td style="text-align: left;"><code>&lt;|eot_id|&gt;</code></td>
      <td style="text-align: left;">End-of-turn token signaling that the current speaker has finished their message.</td>
    </tr>
    <tr>
      <td style="text-align: left;"><code>&lt;|end_of_text|&gt;</code></td>
      <td style="text-align: left;">End-of-sequence (EOS) token used as an auxiliary stop condition.</td>
    </tr>
  </tbody>
</table>


## Default System Prompts

While you can customize the system message for downstream applications, the models were fine-tuned and evaluated using the following canonical system personas:

* **Scalar Phos Flash (3.2B):**
  ```text
  You are Scalar Phos Flash, an efficient, high-performance edge language model developed by Scalar AI.
  ```

* **Scalar Phos Pro (8.0B):**
```text
You are Scalar Phos Pro, an advanced reasoning and instruction-following language model developed by Scalar AI.
```

## Single-Turn Chat Structure

When formatting raw strings manually for inference or SFT training (`training/data_prep.py`), follow this exact layout:

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are Scalar Phos Flash, an efficient, high-performance edge language model developed by Scalar AI.<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

*Note: Leave the trailing `\n\n` after `<|start_header_id|>assistant<|end_header_id|>` so the model immediately begins generating its response.*

## Multi-Turn Conversation Structure

For multi-turn sessions, append subsequent `user` and `assistant` blocks separated by `<|eot_id|>`:

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are Scalar Phos Pro, an advanced reasoning and instruction-following language model developed by Scalar AI.<|eot_id|><|start_header_id|>user<|end_header_id|>

What is QLoRA?<|eot_id|><|start_header_id|>assistant<|end_header_id|>

QLoRA (Quantized Low-Rank Adaptation) is a memory-efficient fine-tuning technique that backpropagates gradients through a frozen, 4-bit quantized pretrained language model into Low-Rank Adapters.<|eot_id|><|start_header_id|>user<|end_header_id|>

How much VRAM does it save compared to full fine-tuning?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

## Programmatic Formatting (`apply_chat_template`)

When using Hugging Face `transformers`, avoid manual string concatenation whenever possible and use the tokenizer's built-in chat template method:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

messages = [
    {
        "role": "system",
        "content": "You are Scalar Phos Flash, an efficient, high-performance edge language model developed by Scalar AI."
    },
    {
        "role": "user",
        "content": "Explain the difference between latency and throughput."
    }
]

formatted_prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
```

## Stop Token Configuration

Always configure both `<|eot_id|>` and `<|end_of_text|>` as stop tokens in your inference engine so the model does not hallucinate subsequent user turns:

* **Ollama (`Modelfile`):**
```dockerfile
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"
```

* **Hugging Face `transformers` (`model.generate`):**
```python
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]
outputs = model.generate(**inputs, eos_token_id=terminators)

```

## License

This documentation is licensed under the **Apache License 2.0**.
