from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from typing import Dict, List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

StoryNode = Dict[str, object]
STORY: Dict[str, StoryNode] = {
    "start": {
        "title": "The Fork in the Forest",
        "text": "You wake in a moonlit forest. A path splits: left toward drums, right toward a distant glow.",
        "choices": [
            {"label": "Go left (drums)", "to": "drums"},
            {"label": "Go right (glow)", "to": "glow"}
        ],
    },
    "drums": {
        "title": "Drums",
        "text": "The drums grow louder. A traveler offers a wooden charm for luck.",
        "choices": [
            {"label": "Accept the charm", "to": "charm"},
            {"label": "Refuse and press on", "to": "river"}
        ],
    },
    "glow": {
        "title": "Glow",
        "text": "A lantern hangs from an old gate. Beyond it, a quiet village sleeps.",
        "choices": [
            {"label": "Enter the village", "to": "village"},
            {"label": "Turn back to the fork", "to": "start"}
        ],
    },
    "charm": {
        "title": "Charm",
        "text": "Warmth tingles in your palm. The trees part, revealing a safe footbridge.",
        "choices": [
            {"label": "Cross the bridge", "to": "village"},
            {"label": "Return to the fork", "to": "start"}
        ],
    },
    "river": {
        "title": "River",
        "text": "You reach a rushing river with slippery stones.",
        "choices": [
            {"label": "Risk crossing", "to": "ending_brave"},
            {"label": "Head back", "to": "drums"}
        ],
    },
    "village": {
        "title": "Village",
        "text": "You find an inn and a warm meal. For tonight, you’re safe.",
        "choices": [
            {"label": "Play again", "to": "start"}
        ],
    },
    "ending_brave": {
        "title": "Brave Crossing",
        "text": "You leap from stone to stone—splash! You make it, soaked but laughing.",
        "choices": [
            {"label": "Play again", "to": "start"}
        ],
    }
}


def render(node_id: str) -> str:
    node = STORY.get(node_id, STORY["start"])
    title = node["title"]
    text = node["text"]
    choices: List[Dict[str, str]] = node["choices"]  # type: ignore
    links = "".join(
        f"<li><a href='/go/{c['to']}'>{c['label']}</a></li>" for c in choices
    )
    return f"""
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>{title}</title>
        <style>
          body {{
            background-color: #0d0d0d;
            color: #e0e0e0;
            font-family: monospace, monospace;
            margin: 2rem auto;
            max-width: 720px;
            line-height: 1.6;
            text-align: center;
          }}
          h1 {{
            font-size: 1.5rem;
            margin: 1rem 0;
            color: #ffd369;
          }}
          p {{
            margin: 1rem 0;
          }}
          ul {{
            list-style: none;
            padding: 0;
          }}
          li {{
            margin: .5rem 0;
          }}
          a {{
            color: #80dfff;
            text-decoration: none;
            font-weight: bold;
          }}
          a:hover {{
            color: #ffd369;
          }}
          img {{
            max-width: 100%;
            margin-bottom: 1rem;
            border: 3px solid #333;
            border-radius: 8px;
          }}
        </style>
      </head>
      <body>
        <img src='/static/cover.png' alt='Azure Text Adventure Cover'>
        <h1>{title}</h1>
        <p>{text}</p>
        <ul>{links}</ul>
        <div class="footer">Azure Text Adventure • FastAPI on Azure</div>
      </body>
    </html>
    """



@app.get("/")
def home():
    return Response(render("start"), media_type="text/html")


@app.get("/go/{node_id}")
def go(node_id: str):
    return Response(render(node_id), media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}
