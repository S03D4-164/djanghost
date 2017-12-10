import os, sys, json, base64
from pprint import pprint
from ghost import Ghost
    
url = sys.argv[1]
result = {
    #"error":None,
    "page":{},
    "resources":[],
    "capture":None,
}

ghost = Ghost()
with ghost.start() as session:
    page, resources = session.open(url)
    if page:
        print(page.url.encode("utf-8"))
        #print(page.content)
        #content = session.content.encode("utf-8")
        result["page"] = {
            "url":page.url,
            "http_status":page.http_status,
            "headers":page.headers,
            "content":base64.b64encode(session.content.encode("utf-8")).decode("ascii"),
            "seq":0,
            #"error":page.error,
        }
        try:
            capture = "capture.png"
            session.capture_to(capture)
            if os.path.isfile(capture):
                with open(capture, 'rb') as c:
                    result["capture"] = base64.b64encode(c.read()).decode("ascii")
        except Exception as e:
            print(str(e))
    if resources:
        seq = 0
        for r in resources:
            print(r.url.encode("utf-8"))
            #print(r.content)
            seq += 1
            dict = {
                "url":r.url,
                "http_status":r.http_status,
                "headers":r.headers,
                "content":base64.b64encode(r.content).decode("ascii"),
                "seq":seq,
                #"error":r.error,
            }
            result["resources"].append(dict)

dump = "ghost.json"
with open(dump, 'w') as d:
    #pprint(result)
    json.dump(result, d)
