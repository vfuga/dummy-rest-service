import aiohttp  # noqa
import sys
import asyncio
import requests  # noqa
import urllib3
import json      # noqa
import datetime


urllib3.util.connection.HAS_IPV6 = False


async def test(n: int):
    print(f"Started: => {n}")
    success_cnt = 0
    failure_cnt = 0
    async with aiohttp.ClientSession(
            # ###  !!!!!! если ставить большой total timeout - работает ну очень плохо!!!!
            # ### возможо это особенность реализации в докере
            # возможно связано с работой GC/OS
            timeout=aiohttp.ClientTimeout(total=3.0)) as session:

        url = 'http://localhost:8800/one'
        for _ in range(1000):
            try:
                async with session.get(url) as resp:
                    try:
                        if (resp.status == 200):
                            _ = await resp.text()
                            success_cnt += 1
                        else:
                            failure_cnt += 1
                            print(resp.status)
                    except Exception as ex1:  # noqa
                        failure_cnt += 1
                        print(f"ex1 => {ex1}")
                    finally:
                        pass
            except Exception as ex2:  # noqa
                failure_cnt += 1
                print(f"ex2({n}) => {ex2}, " + str(type(ex2)))

    print(f"Done => {n}, success: {success_cnt}, failure: {failure_cnt}")


async def main():
    await asyncio.gather(*[test(i) for i in range(100)])


# if __name__ == "__main__":
#     start_ts = datetime.datetime.now()
#     asyncio.run(main())
#     print(datetime.datetime.now() - start_ts)
#     print("-" * 60)
#     sys.exit(0)


if __name__ == "__main__":
    success_cnt = 0
    failure_cnt = 0
    start_ts = datetime.datetime.now()
    results = []
    for _ in range(1000):
        try:
            res = requests.get(url="http://localhost:8800/one", timeout=5.0)
            if res.status_code == 200:
                success_cnt += 1
                results.append(res.json())
                # print(res.json())
                continue
                print(json.dumps(res.json(), ensure_ascii=False, indent=2))
            else:
                res.close()
                failure_cnt += 1
                print(res.status_code)
                continue
        except Exception as ex:
            print(ex)
            failure_cnt += 1
    print(datetime.datetime.now() - start_ts, f"success: {success_cnt}, failure: {failure_cnt}")
