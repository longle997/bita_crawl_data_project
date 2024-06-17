from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Product
from contextlib import asynccontextmanager
from crawl_data_service import CrawlDataService

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # crawl data
    crawl_data_products = CrawlDataService.crawl_data_from_target_lazada_page()
    session = SessionLocal()
    product_object_list = [Product(**crawl_data_product) for crawl_data_product in crawl_data_products]
    session.bulk_save_objects(product_object_list)
    session.commit()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return templates.TemplateResponse(
        request=request, name="item.html", context={"items": products, 'title': 'Lazada crawl data table'}
    )
