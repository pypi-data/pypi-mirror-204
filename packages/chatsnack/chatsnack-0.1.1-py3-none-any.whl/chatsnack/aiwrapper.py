import asyncio
import openai
import os
import json
from loguru import logger
from functools import wraps

openai.api_key = os.getenv("OPENAI_API_KEY")

async def set_api_key(api_key):
    openai.api_key = api_key

# decorator to retry API calls
def retryAPI(exception, tries=4, delay=3, backoff=2):
    """Retry calling the decorated function using an exponential backoff.
    :param Exception exception: the exception to check. may be a tuple of
        exceptions to check
    :param int tries: number of times to try (not retry) before giving up
    :param int delay: initial delay between retries in seconds
    :param int backoff: backoff multiplier e.g. value of 2 will double the
        delay each retry
    :raises Exception: the last exception raised
    """
    def deco_retry(f):
        @wraps(f)
        async def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return await f(*args, **kwargs)
                except exception as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    logger.debug(msg)
                    await asyncio.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return await f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry

# openai
async def _chatcompletion(prompt, engine="gpt-3.5-turbo", max_tokens=None, temperature=0.7, top_p=1, stop=None, presence_penalty=0, frequency_penalty=0, n=1, stream=False, user=None):
    if user is None:
        user = "_not_set"
    # prompt will be in JSON format, let us translate it to a python list
    # if the prompt is a list already, we will just use it as is
    if isinstance(prompt, list):
        messages = prompt
    else:
        messages = json.loads(prompt)
    logger.debug("""Chat Query:
    Prompt: {0}
    Model: {2}, Max Tokens: {3}, Stop: {5}, Temperature: {1}, Top-P: {4}, Presence Penalty {6}, Frequency Penalty: {7}, N: {8}, Stream: {9}, User: {10}
    """,prompt, temperature, engine, max_tokens, top_p, stop, presence_penalty, frequency_penalty, n, stream, user)
    response = await openai.ChatCompletion.acreate(model=engine,
                                            messages=messages,
                                            max_tokens=max_tokens,
                                            temperature=temperature,
                                            top_p=top_p,
                                            presence_penalty=presence_penalty,
                                            frequency_penalty=frequency_penalty,
                                            stop=stop,
                                            n=n,
                                            stream=stream,
                                            user=user)
    logger.trace("OpenAI Completion Result: {0}".format(response))
    return response

def _trimmed_fetch_chat_response(resp, n):
    if n == 1:
        return resp.choices[0].message.content.strip()
    else:
        logger.trace('_trimmed_fetch_response :: returning {0} responses from ChatGPT'.format(n))
        texts = []
        for idx in range(0, n):
            texts.append(resp.choices[idx].message.content.strip())
        return texts

# ChatGPT
@retryAPI(openai.error.RateLimitError, tries=3, delay=2, backoff=2)
async def cleaned_chat_completion(prompt, engine="gpt-3.5-turbo", max_tokens=None, temperature=0.7, top_p=1, stop=None, presence_penalty=0, frequency_penalty=0, n=1, stream=False, user=None, **ignored):
    '''
    Wrapper for OpenAI API chat completion. Returns whitespace trimmed result from ChatGPT.
    '''
    resp = await _chatcompletion(prompt,
                            engine=engine,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            presence_penalty=presence_penalty,
                            frequency_penalty=frequency_penalty,
                            stop=stop,
                            n=n,
                            stream=stream,
                            user=user)

    return _trimmed_fetch_chat_response(resp, n)
