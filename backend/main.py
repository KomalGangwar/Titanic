from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from query_handler import handle_query

app = FastAPI()

# Enable CORS for all origins (for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
def query_bot(q: str = Query(..., title="User Query")):
    response, isIMG = handle_query(q)

    if isIMG:
        # Ensure `response` is a BytesIO object before sending
        return StreamingResponse(response, media_type="image/png")

    # Return JSON response for text queries
    return Response(content=json.dumps({"response": response}), media_type="application/json")
