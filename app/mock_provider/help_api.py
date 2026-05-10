from fastapi import FastAPI, Request
from datetime import datetime
from middleware import RequestContextMiddleware
from fastapi.responses import JSONResponse
import json


app = FastAPI()

app.add_middleware(RequestContextMiddleware)

OUTPUT_FILE = "payloads.json"



@app.api_route("/webhook", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def inspect_request(context: RequestContext = Depends(get_context),):
    body_bytes = await request.body()

    try:
        body = json.loads(body_bytes)
        ctx = getattr(request.state, "context", None)
    except:
        body = body_bytes.decode("utf-8", errors="ignore")

    request_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "client": request.client.host if request.client else None,
        "body": body,
        "else": ctx
    }

    # save to file
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(request_data, ensure_ascii=False) + "\n")

    # console log
    print(json.dumps(request_data, indent=2, ensure_ascii=False))

    # return everything back
    return JSONResponse(content=request_data)