import requests, base64

class Keys():
    mlb = "aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9qZXQvbWxiLnR4dA=="
    nhl = "eyJhbGciOiJIUzI1NiJ9.eyJpcGlkIjoibmhsR2F0ZXdheUlkOjExNzA5MjYiLCJjbGllbnRJZCI6ImFjdGl2YXRpb25fbmhsLXYxLjAuMCIsInBjX21heF9yYXRpbmdfbW92aWUiOiIiLCJjb250ZXh0Ijp7fSwidmVyaWZpY2F0aW9uTGV2ZWwiOjIsImV4cCI6MTY0MjM2NTEzOSwidHlwZSI6IlVzZXIiLCJpYXQiOjE2MTA4MjkxMzksInVzZXJpZCI6IjQ1NDMxNzgiLCJ2ZXJzaW9uIjoidjEuMCIsInBjX21heF9yYXRpbmdfdHYiOiIiLCJlbWFpbCI6Ind4cm9ja3NAaG90bWFpbC5jb20ifQ.T5Q4p0-uv4SXxfGCbpgCb_X_OCiqdNxBd1R1y_zX93Q%3B+mediaAuth_v2%3D6455209108eaa22507b1b305ff7466270d11c4e1da95b073ba26d541692f17958e14d998bccdb0ff894ab8c391f2d6c04731a6f9e44677eeb83e5954d55de84cb2d7237673b095912322638d51adc29cbacd7b916d134d189fc52f50e8cf80a84852ceed0184232d496115c60623404a9765769741c17a54ae65e65c5629044627fd2dd5fe8047cf1d02f43d669490e917a7d9029f6d6ff2ce3845d061305d98ada84952605713e2fe0d565d60707cad679dc7a365027b81c2e59a7779180e90037e1f676008ba203da8875db3e6086e7e321efadaa5a20a5938a601c93d0c964ad5cc2dd1f50ec40b80c3572466809f1bdde78f81c794435eae9029e4b548c58b7cef60aa16dec27e030cbbfabcb64796fd2b5aa3e459b2505a8f366f3bbb032597a1fa89b3bb18431dc81b9b1985314dfdf3dbdf074dd6da803f807cc567c7773fe724a439cf7221cb6c8aa24e5916cc7fc5a9e3678a1eb7426f75d5eac8e090da208fe2e0d0365ee4b5b4ba8492777c73b0063fd9e30d6df7db8a8c15bfa0010b4120c5f0b7376299744b21d70925ebd98f6395362a1ef31654af3611a445c722d0ae37797a23"
    # locast = ""
    sling = "aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9NQURfVElUQU5fU1BPUlRTL0xJVkVUVi90dmsuanNvbg=="

    def get_key(key):
        key = base64.b64decode(key).decode('utf-8')
        if key.startswith("http"):
            if key.endswith(".json"):
                key = requests.get(key).json()
            else:
                key = requests.get(key).text
        if type(key) == str:
            key = key.strip()
        return key