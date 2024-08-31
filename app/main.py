import logging
from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from llmsherpa.readers import LayoutPDFReader

from database import get_db
from model.book import Book
from model.page import Page
from sqlalchemy.orm import Session
from sqlalchemy import text

# TODO env
LLMSHERPA_API_URL = "http://nlm-ingestor:5001/api/parseDocument?renderFormat=all"

logger = logging.getLogger("uvicorn")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sections": []}
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    try:
        form = await request.form()
        file = form["file"]
        print(file.filename)

        contents = await file.read()

        pdf_reader = LayoutPDFReader(LLMSHERPA_API_URL)
        doc = pdf_reader.read_pdf(path_or_url=file.filename, contents=contents)

        sections = doc.sections()

        sections_content = [
            section.to_html(include_children=True, recurse=True) for section in sections
        ]

        # file.filenameから.pdfを取り除いたものをtitleとして使う
        title = file.filename.split(".")[0]
        # TODO titleをサニタイズする

        # データベースセッションの取得と管理
        db: Session = next(get_db())
        try:
            # BookをDBに保存
            book = Book(title=title)
            db.add(book)
            db.flush()  # IDを取得するためにflush

            # PageをDBに保存
            pages = [
                Page(book_id=book.id, content=section, page_number=i)
                for i, section in enumerate(sections_content)
            ]
            db.bulk_save_objects(pages)

            db.commit()

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

        return templates.TemplateResponse(
            request=request,
            name="sections.html",
            context={"sections": sections_content},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, keyword: str = Query(...)):
    logger.info(f"Searching for: {keyword}")
    print(keyword)

    db = next(get_db())
    try:
        # PGroongaを使用した全文検索クエリ
        query = text(
            """
        SELECT p.id, p.content, p.page_number, b.title
        FROM pages p
        JOIN books b ON p.book_id = b.id
        WHERE p.content &@ :keyword
        LIMIT 10;
        """
        )

        # クエリをログに出力
        logger.info(f"Executing query: {query}")
        logger.info(f"With parameters: keyword={keyword}")

        results = db.execute(query, {"keyword": keyword}).fetchall()

        # 結果の数をログに出力
        logger.info(f"Number of results: {len(results)}")

        # 検索結果をテンプレートに渡す
        return templates.TemplateResponse(
            "search_results.html",
            {"request": request, "results": results, "keyword": keyword},
        )
    finally:
        db.close()


@app.get("/page/{page_id}", response_class=HTMLResponse)
async def get_page_detail(request: Request, page_id: int):
    db: Session = next(get_db())
    try:
        page = db.query(Page).filter(Page.id == page_id).first()
        if page is None:
            raise HTTPException(status_code=404, detail="Page not found")

        return templates.TemplateResponse(
            "page_detail.html", {"request": request, "page": page}
        )
    finally:
        db.close()
