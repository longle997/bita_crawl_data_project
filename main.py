from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Product
from contextlib import asynccontextmanager
from crawl_data_service import CrawlDataService

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
    product_records = session.query(Product).all()
    product_name_list = [product.product_name for product in product_records]
    product_object_list = [Product(**crawl_data_product) for crawl_data_product in crawl_data_products 
                           if crawl_data_product['product_name'] not in product_name_list]
    session.bulk_save_objects(product_object_list)
    session.commit()
    session.close()
    yield

# crawl data when start app
# app = FastAPI(lifespan=lifespan)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return templates.TemplateResponse(
        request=request, name="item.html", context={"items": products, 'title': 'Lazada crawl data table'}
    )
