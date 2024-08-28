from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from llmsherpa.readers import LayoutPDFReader

# TODO env
LLMSHERPA_API_URL = "http://localhost:5010/api/parseDocument?renderFormat=all"

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sections": []}
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    form = await request.form()
    file = form["file"]
    print(file.filename)

    contents = await file.read()

    pdf_reader = LayoutPDFReader(LLMSHERPA_API_URL)
    doc = pdf_reader.read_pdf(path_or_url=file.filename, contents=contents)

    sections = doc.sections()

    sections_content = [
        section.to_text(include_children=True, recurse=True) for section in sections
    ]

    # TODO sections_contentをDBに保存する

    return templates.TemplateResponse(
        request=request,
        name="sections.html",
        context={"sections": sections_content},
    )
