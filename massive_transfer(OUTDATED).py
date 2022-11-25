print("Created by: Mrakobes1337 & FeZillo")

import asyncio
import json
import uuid
import base64
import hmac
from hashlib import sha1
from time import time as timestamp
import aiohttp
import asyncio
from os import urandom
from binascii import hexlify



def device_gen():
    HEX_KEY = "76b4a156aaccade137b8b1e77b435a81971fbd3e"
    uid: str = str(uuid.uuid4())
    mac: hmac.HMAC = hmac.new(bytes.fromhex(HEX_KEY), "2".encode() + sha1(uid.encode()).digest(), sha1)
    uniqueId: str = "32" + sha1(uid.encode()).digest().hex()
    device: str = (uniqueId + mac.hexdigest()).upper()
    return device

def signature(data):
    return base64.b64encode(bytes.fromhex("32") + hmac.new(bytes.fromhex("fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2"), data.encode("utf-8"), sha1).digest()).decode("utf-8")

async def coins(comId,userId,session):
    trans=str(uuid.UUID(hexlify(urandom(16)).decode("ascii")))
    data = json.dumps({
        "paymentContext": {
            "transactionId": trans,
            "isAutoRenew": False
        },
        "timestamp": int(timestamp() * 1000)})
    sig = signature(data)
    headers["NDC-MSG-SIG"]=sig
    async with session.post(f"{api}/x{comId}/s/influencer/{userId}/subscribe",data=data,headers=headers) as res:
        if res.status !=200:
            await coins(comId,userId,session)

device = device_gen()
api="https://service.narvii.com/api/v1"
headers={
    "NDCLANG": "en", 
    "NDCDEVICEID": device, 
    "SMDEVICEID": "b89d9a00-f78e-46a3-bd54-6507d68b343c", 
    "Accept-Language": "en-US", 
    "Content-Type": "application/json; charset=utf-8", 
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)", 
    "Host": "service.narvii.com", 
    "Connection": "Keep-Alive", 
    "Accept-Encoding": "gzip"}

async def main():
    session = aiohttp.ClientSession()
    email=str(input("Mail: "))
    password=str(input("Password: "))

    data = json.dumps({
        "email": email,
        "secret": f"0 {password}",
        "deviceID": device,
        "clientType": 100,
        "action": "normal",
        "timestamp": int(timestamp() * 1000)})
    signature = base64.b64encode(bytes.fromhex("32") + hmac.new(bytes.fromhex("fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2"), data.encode("utf-8"), sha1).digest()).decode("utf-8")
    headers["NDC-MSG-SIG"]=signature
    async with session.post(f"{api}/g/s/auth/login", data=data, headers=headers) as res:
        res=json.loads(await res.text())
        headers["NDCAUTH"]=f"sid={res['sid']}"
        uid=res["auid"]
    headers.pop("NDC-MSG-SIG")
    code = input("Profile link: ")
    async with session.get(f"{api}/g/s/link-resolution?q={code}", headers=headers) as res:
        res=json.loads(await res.text())
        id = res["linkInfoV2"]["extensions"]["linkInfo"]["objectId"]
        comId = res["linkInfoV2"]["extensions"]["linkInfo"]["ndcId"]
    async with session.get(f"{api}/x{comId}/s/user-profile/{id}", headers=headers) as res:
        res=json.loads(await res.text())
        price=res["userProfile"]["influencerInfo"]["monthlyFee"]
    async with session.get(f"{api}/g/s/wallet", headers=headers) as res:
        bal=json.loads(await res.text())["wallet"]["totalCoins"]
    print(f"Balance: {int(bal)}")
    
    count = int(input("How many coins to transfer: "))
    if count <= price:
        count = 1
    else:
        if count % price != 0:
            count=count // price + 1
        else:
            count=count // price
    await asyncio.gather(*[asyncio.create_task(coins(comId=comId, userId=id, session=session)) for gay in range(count)])

asyncio.get_event_loop().run_until_complete(main())