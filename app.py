from fastapi import FastAPI, Response
from typing import Dict, List

app = FastAPI()

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
          body {{ font-family: system-ui, sans-serif; margin: 3rem; max-width: 720px; line-height: 1.5; }}
          h1 {{ font-size: 1.8rem; margin-bottom: .5rem; }}
          p {{ margin: .5rem 0 1rem; }}
          ul {{ padding-left: 1rem; }}
          a {{ text-decoration: none; }}
          a:hover {{ text-decoration: underline; }}
          .footer {{ color:#666; font-size:.8rem; margin-top:2rem; }}
        </style>
      </head>
      <body>
        <h1>{title}</h1>
        <p>{text}</p>
        <ul>{links}</ul>
        <div class="footer">Text Adventure demo • FastAPI on Azure App Service</div>
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
