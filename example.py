import requests
# =====================================================================
# 1. USER'S ORIGINAL REQUEST CONFIGURATION (What you want to send)
# =====================================================================
# The target TikTok URL to scrape or request
tiktok_url = "https://api16-normal-useast5.tiktokv.us/passport/app/region/?device_platform=android&channel=googleplay&aid=1233&app_name=musical_ly&version_code=450703&version_name=45.7.3&sys_region=US&carrier_region=FR&iid=7628173836248319719&device_id=7531532388682745352&support_webview=1®_store_region=fr&cronet_version=58b89838_2026-05-26&ttnet_version=4.2.243.56-tiktok&use_store_region_cookie=1"
# The original HTTP headers the dev already has in their script
my_headers = {
    "tt-ticket-guard-public-key": "BM1GdMaCtr+CH28Cfh7r5+wSPfuvWhKmyEK3lrSB4AJPDz93xTZDI8PWmp3RSr6fZAdI659wPZEefWkuqxp9/DU=",
    "sdk-version": "2",
    "tt-ticket-guard-iteration-version": "0",
    "x-tt-dm-status": "login=0;ct=1;rt=8",
    "x-tt-bypass-dp": "1",
    "tt-ticket-guard-version": "3",
    "passport-sdk-version": "1",
    "x-vc-bdturing-sdk-version": "2.4.2.i18n",
    "tt-device-guard-iteration-version": "1",
    "tt-device-guard-client-data": "eyJkZXZpY2VfdG9rZW4iOiIxfHtcImFpZFwiOjEyMzMsXCJhvlwiOlwiNDUuNy4zXCIsXCJkaWRcIjpcIjc1MzE1MzIzODg2ODI3NDUzNjZcIixcImlpZFwiOlwiNzY1MzkyOTY1NzI0NzAwODUzNFwiLFwiZml0XCI6XCIxNzUzNTcyMzY5XCIsXCJzXCI6MSxcImlkY1wiOlwibm8xYVwiLFwidHNcIjpcIjE3ODIzMTY2MzJcIn0iLCJ0aW1lc3RhbXAiOjE3ODIzMTY2OTEsInJlcV9jb250ZW50IjoiZGV2aWNlX3Rva2VuLHBhdGgsdGltZXN0YW1wIiwiZHRva2VuX3NpZ24iOiJ0cy4xLk1FUUNJRllSbjFiMlBjOElPa3F0eEprRkdkU0dpYjhGajR4ZUtWOVwvMGxLb2onsWNDAiYWJJR0h1OW1mT2xyd3JJQ0dZcTd2NnVkMUdqNEdiWmpqQTBMVlFOSit1cHlRPT0iLCJkcmVxX3NpZ24iOiJNRVlDSVFEVEwwU2dOZWVIMmhhdG9KaFJhMkFUdkZ5MWhrUVg1cXJcL0d2UzJZUHFObVFJaEFPV1lTd1RlNzVWRFFRY21JeUJhZDhhMXMxa0R3QWJEeFZFVXFOQThPdDVzIn0=",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-ss-stub": "CB891AFA1E97B62F890391B9A1BF514D",
    "x-tt-request-tag": "s=-1;p=0",
    "x-tt-trace-id": "00-fa5a739b10688560cdc1c8c616d204d1-fa5a739b10688560-01",
    "user-agent": "com.zhiliaoapp.musically/2024507030 (Linux; U; Android 13; en; SM-G781B; Build/TP1A.220624.014; Cronet/TTNetVersion:58b89838 2026-05-26 QuicVersion:f9fda2ef 2026-03-10)",
    "accept-encoding": "gzip, deflate, br"
}
# The original cookies dictionary the dev already has in their script
my_cookies = {
    "store-country-code": "fr",
    "store-country-code-src": "did",
    "tt-target-idc": "eu-ttp2"
}
# =====================================================================
# 2. CALL THE RAPIDAPI SIGNER
# =====================================================================
signer_url = "https://tiktok-signer-working.p.rapidapi.com/sign"
signer_headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE",
    "X-RapidAPI-Host": "tiktok-signer-working.p.rapidapi.com",
    "Content-Type": "application/json"
}
# Building the object to send to RapidAPI
signer_payload = {
    "url": tiktok_url,
    "os_version": "15",
    "device_model": "SM-G782B",
    "device_id": "7531532388682745352",
    "install_id": "7628173836248319719",
    "headers": my_headers, # Directly passing the user's headers dictionary
    "cookies": my_cookies  # Directly passing the user's cookies dictionary
}
print("[*] Fetching signatures from RapidAPI...")
signer_response = requests.post(signer_url, json=signer_payload, headers=signer_headers)
if signer_response.status_code == 200:
    response_json = signer_response.json()
    # Extract the freshly generated cryptographic signatures dictionary
    generated_signatures = response_json.get("data", {})
    tiktok_version = response_json.get("Tiktok-version")
    print(f"[+] Signatures retrieved successfully! (Engine Version: {tiktok_version})")
    # =====================================================================
    # 3. MERGE SIGNATURES & EXECUTE THE FINAL REQUEST TO TIKTOK
    # =====================================================================
    # Python dict.update() injects X-Gorgon, X-Argus, etc., right into the user's header dictionary
    my_headers.update(generated_signatures)
    print("[*] Executing signed request to TikTok...")
    final_tiktok_response = requests.post(
        tiktok_url, 
        headers=my_headers, 
        cookies=my_cookies, 
    )
    print(f"[+] TikTok response code: {final_tiktok_response.status_code}")
    # print(final_tiktok_response.text)
else:
    print(f"[-] Failed to sign request. Status Code: {signer_response.status_code}")
    print(signer_response.text)
