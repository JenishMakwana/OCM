from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import re
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class Tyre(BaseModel):
    id: Optional[str] = None
    brand: str
    size: str
    type: str
    pattern: str
    stock: int = 0
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TyreCreate(BaseModel):
    brand: str
    size: str
    type: str
    pattern: str
    stock: int = 0
    price: float

class TyreUpdate(BaseModel):
    stock: Optional[int] = None
    price: Optional[float] = None


# Routes
@api_router.get("/")
async def root():
    return {"message": "Tyre Inventory API"}

@api_router.get("/tyres", response_model=List[Tyre])
async def get_all_tyres():
    """Get all tyres from inventory"""
    tyres = await db.tyres.find().to_list(1000)
    result = []
    for tyre in tyres:
        tyre['id'] = str(tyre['_id'])
        del tyre['_id']
        result.append(Tyre(**tyre))
    return result

@api_router.get("/tyres/search")
async def search_tyres(brand: Optional[str] = None, size: Optional[str] = None):
    """Search tyres by brand or size"""
    query = {}
    if brand:
        # Escape regex metacharacters for brand search
        escaped_brand = re.escape(brand)
        query['brand'] = {'$regex': escaped_brand, '$options': 'i'}
    if size:
        # Escape regex metacharacters for size search
        escaped_size = re.escape(size)
        query['size'] = {'$regex': escaped_size, '$options': 'i'}
    
    tyres = await db.tyres.find(query).to_list(1000)
    result = []
    for tyre in tyres:
        tyre['id'] = str(tyre['_id'])
        del tyre['_id']
        result.append(Tyre(**tyre))
    return result

@api_router.post("/tyres", response_model=Tyre)
async def create_tyre(tyre: TyreCreate):
    """Add a new tyre to inventory"""
    tyre_dict = tyre.dict()
    tyre_dict['created_at'] = datetime.utcnow()
    tyre_dict['updated_at'] = datetime.utcnow()
    
    result = await db.tyres.insert_one(tyre_dict)
    tyre_dict['id'] = str(result.inserted_id)
    return Tyre(**tyre_dict)

@api_router.put("/tyres/{tyre_id}", response_model=Tyre)
async def update_tyre(tyre_id: str, update: TyreUpdate):
    """Update stock or price of a tyre"""
    try:
        # Build update dict
        update_dict = {}
        if update.stock is not None:
            update_dict['stock'] = update.stock
        if update.price is not None:
            update_dict['price'] = update.price
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_dict['updated_at'] = datetime.utcnow()
        
        # Update in database
        result = await db.tyres.find_one_and_update(
            {'_id': ObjectId(tyre_id)},
            {'$set': update_dict},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Tyre not found")
        
        result['id'] = str(result['_id'])
        del result['_id']
        return Tyre(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.delete("/tyres/{tyre_id}")
async def delete_tyre(tyre_id: str):
    """Delete a tyre from inventory"""
    try:
        result = await db.tyres.delete_one({'_id': ObjectId(tyre_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tyre not found")
        return {"message": "Tyre deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/tyres/brands")
async def get_brands():
    """Get list of all brands"""
    brands = await db.tyres.distinct('brand')
    return {"brands": sorted(brands)}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
