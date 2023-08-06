import tiktoken

price_per_token = {
    "gpt-3.5-turbo": 0.002 / 1000,
    "text-davinci": 0.02 / 1000,
}


def chat_count_tokens(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages.

    Copied from : https://platform.openai.com/docs/guides/chat/introduction.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"Not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md"
        )


def chat_estimate_price(messages, model="gpt-3.5-turbo-0301"):
    """Returns the estimated price of a list of messages."""
    model_short = "gpt-3.5-turbo" if model.startswith("gpt-3.5-turbo") else model
    return chat_count_tokens(messages, model) * price_per_token[model_short]


def complete_count_tokens(prompt, model="text-davinci-003"):
    """Returns the number of tokens used by a prompt."""
    return len(tiktoken.encoding_for_model(model).encode(prompt))


def complete_estimate_price(prompt, model="text-davinci-003"):
    """Returns the estimated price of a prompt."""
    model_short = "text-davinci" if model.startswith("text-davinci") else model
    return complete_count_tokens(prompt, model) * price_per_token[model_short]
