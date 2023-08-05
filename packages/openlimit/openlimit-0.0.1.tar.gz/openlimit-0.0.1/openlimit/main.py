# Standard library
import asyncio

# Local
from rate_limiters import ChatRateLimiter
from redis_rate_limiters import ChatRateLimiterWithRedis


#########
# TESTING
#########


import openai

openai.api_key = "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"
# rate_limiter = ChatRateLimiterWithRedis(request_limit=200, token_limit=40000, redis_url="redis://default:rpvYYcxxKVBA0UyKqrft@containers-us-west-180.railway.app:6089")
rate_limiter = ChatRateLimiter(request_limit=200, token_limit=40000)


@rate_limiter.is_limited()
async def make_request(messages):
    response = await openai.ChatCompletion.acreate(model="gpt-4-0314", messages=messages)
    response = response["choices"][0]["message"]["content"]

    print(response)


async def main():
    tasks = [make_request(messages=[{"role": "user", "content": "Say hi"}]) for i in range(500)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())