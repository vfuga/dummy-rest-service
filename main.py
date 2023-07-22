import sys
import numpy as np
import uvicorn
import datetime
import uuid
import json
import urllib3

urllib3.util.connection.HAS_IPV6 = False

import asyncio  # noqa


sys.path.append(".")


from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from faker import Faker


load_dotenv()
fapp = FastAPI()
fake = Faker("ru_RU")


def generate_row(fake: Faker = fake) -> dict:
    """
        Процедура генерации рандомной записи
    """
    gender = np.random.choice(["M", "F"])
    if gender == "M":
        first_name = fake.first_name_male()
        middle_name = fake.middle_name_male()
        last_name = fake.last_name_male()
    else:
        first_name = fake.first_name_female()
        middle_name = fake.middle_name_female()
        last_name = fake.last_name_female()
    if np.random.randint(1, 1_000_000) % 5:
        inn = fake.businesses_inn()
        snils = str(uuid.uuid4())
    else:
        inn = None
        snils = None

    if np.random.randint(100) < 85:
        doc_issuing_date = str(fake.date_between(datetime.date(2000, 1, 1), datetime.date.today()))
        doc_issuing_authority = fake.address()
        doc_issuer_code = str(np.random.randint(4100, 5999))
        doc_no = str(np.random.randint(100100, 799999))
        doc_ser = str(np.random.randint(1000, 6999))
        doc_type = 1
        doc_exp_date = None
    else:
        doc_issuing_date = None
        doc_issuing_authority = None
        doc_issuer_code = None
        doc_no = None
        doc_ser = None
        doc_type = None
        doc_exp_date = None

    if np.random.randint(100) < 5:
        is_deleted = True
    else:
        is_deleted = False

    if np.random.randint(100) < 95:
        enrich = True
    else:
        enrich = False

    row = {
        "id": np.random.randint(1, 1_000_000),               # { name = 'id', type = 'number' },
        "source_id": np.random.randint(1, 6),                # { name = 'source_id', type = 'number', foreign_key = {space = 'mdm___source', field = 'id'}},
        "source_rec_id": np.random.randint(1, 1_000_000),    # { name = 'source_rec_id', type = 'string' },
        "rec_mod_date": str(
            datetime.datetime.now() - datetime.timedelta(seconds=np.random.randint(60, 3600 * 24))
        ),  # { name = 'rec_mod_date', type = 'unsigned' },
        "pr_state_id": np.random.randint(1, 3),  # { name = 'pr_state_id', type = 'number', foreign_key = {space = 'mdm___pr_state', field = 'id'}},
        "last_name": last_name,  # { name = 'last_name', type = 'string', is_nullable = true},
        "given_name": first_name,  # { name = 'given_name', type = 'string' , is_nullable = true},
        "middle_name": middle_name,  # { name = 'middle_name', type = 'string' , is_nullable = true},
        "birth_date": str(fake.date_between(datetime.date(1920, 1, 1), datetime.date(2008, 12, 31))),  # { name = 'birth_date', type = 'unsigned', is_nullable = true },
        "place_of_birth": fake.administrative_unit(),  # { name = 'place_of_birth', type = 'string', is_nullable = true },
        "gender": gender,  # { name = 'gender', type = 'string', is_nullable = true },
        "nationality": None,  # { name = 'nationality', type = 'string', is_nullable = true },
        "inn": inn,  # { name = 'inn', type = 'string', is_nullable = true },
        "snils": snils,  # { name = 'snils', type = 'string', is_nullable = true },
        "doc_issuing_date": doc_issuing_date,  # { name = 'doc_issuing_date', type = 'unsigned', is_nullable = true },
        "doc_issuing_authority": doc_issuing_authority,  # { name = 'doc_issuing_authority', type = 'string', is_nullable = true },
        "doc_issuer_code": doc_issuer_code,   # { name = 'doc_issuer_code', type = 'string', is_nullable = true },
        "doc_no": doc_no,  # { name = 'doc_no', type = 'string', is_nullable = true },
        "doc_ser": doc_ser,  # { name = 'doc_ser', type = 'string', is_nullable = true },
        "doc_type": doc_type,  # { name = 'doc_type', type = 'number', is_nullable = true },
        "doc_exp_date": doc_exp_date,  # { name = 'doc_exp_date', type = 'unsigned', is_nullable = true },
        "update_ts": str(datetime.datetime.now() - datetime.timedelta(seconds=np.random.randint(1000000))),  # { name = 'update_ts', type = 'unsigned'},
        "is_deleted": is_deleted,  # "is_deleted": is_deleted,  # { name = 'is_deleted', type = 'boolean', is_nullable = true },
        "enrich": enrich,  # "enrich": enrich,  # { name = 'enrich', type = 'boolean', is_nullable = true},
        # { name = 'bucket_id', type = 'unsigned' }
    }
    return row


@fapp.get("/")
async def many_rows() -> list:
    n = np.random.randint(0, 100)
    data = []
    for _ in range(n):
        data.append(generate_row())
    # if np.random.randint(1000) % 13 == 0:
    #     await asyncio.sleep(20)
    return data


@fapp.get("/one")
async def one_row() -> dict:
    # if np.random.randint(1000) % 11 == 0:
    #     raise HTTPException(status_code=404, detail="Not Found")
    # if np.random.randint(1000) % 13 == 0:
    #     await asyncio.sleep(20)
    return generate_row()


@fapp.post("/")
async def receive_some_data(request: Request) -> dict:
    # if np.random.randint(1000) % 13 == 0:
    #     await asyncio.sleep(20)
    try:
        js_data = await request.json()
        if js_data.get("id") is not None:
            id_ = int(js_data.get("id"))
            Faker.seed(id_)
            np.random.seed(id_)
            faker = Faker("ru_RU")
            row = generate_row(fake=faker)
            row["id"] = id_
            return row
        print(json.dumps(js_data, ensure_ascii=False, indent=2))

    except Exception as ex:
        raise HTTPException(detail=f"Expected any json: {ex}", status_code=404)

    return generate_row()


if __name__ == "__main__":
    """
        uvicorn main:fapp --host 0.0.0.0 --port 8800 --workers 5
        Example: curl -X POST http://192.168.1.67:8800 -d '{"a": "a"}' -H "Content-Type: application/json"
        в качестве payload можно использовать произвольный json
    """
    uvicorn.run(app=fapp, host="0.0.0.0", port=8800, access_log=True, backlog=False)
