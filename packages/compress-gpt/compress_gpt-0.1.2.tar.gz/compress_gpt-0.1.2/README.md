# CompressGPT
## Self-extracting GPT prompts for ~70% token savings

Check out the accompanying blog post [here](https://musings.yasyf.com/compressgpt-decrease-token-usage-by-70/).

### Installation

```shell
$ pip install compress-gpt
```

### Usage

Simply change your existing imports of `langchain.PromptTemplate` to `compress_gpt.langchain.CompressTemplate` (to compress prompts before populating variables) or `compress_gpt.langchain.CompressPrompt` (to compress prompts after populating variables).

```diff
-from langchain import PromptTemplate
+from compress_gpt.langchain import CompressPrompt as PromptTemplate
```

For very simple prompts, use `CompressSimplePrompt` and `CompressSimpleTemplate` instead.

If compression ever fails or results in extra tokens, the original prompt will be used. Each compression result is aggressively cached, but the first run can take a hot sec.

#### Clearing the cache

```python
import compress_gpt

compress_gpt.clear_cache()
```

### Demo

[![asciicast](https://asciinema.org/a/578285.svg)](https://asciinema.org/a/578285)


### How CompressGPT Works

My [blog post](https://musings.yasyf.com/compressgpt-decrease-token-usage-by-70/) helps explain the below image.

![CompressGPT Pipeline](assets/pipeline.svg)
