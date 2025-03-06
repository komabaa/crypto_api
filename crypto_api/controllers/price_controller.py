from aiohttp import web, ClientSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select, delete
from models.currency import Currency
from config import DATABASE_URL
import datetime

engine = create_async_engine(DATABASE_URL, echo=True)

async def get_price(request):
    currency = request.match_info['currency'].upper()
    
    try:
        symbol = f"{currency}-USDT"
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
        
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return web.Response(status=400, text="Currency not found")
                
                data = await response.json()
                if not data.get('data') or not data['data'].get('price'):
                    return web.Response(status=400, text="Price not available")
                
                bid_price = float(data['data']['price'])
        
        async with engine.begin() as conn:
            await conn.execute(
                Currency.__table__.insert().values(
                    currency=currency,
                    date_=datetime.datetime.now().replace(microsecond=0),
                    price=bid_price
                )
            )
        
        return web.json_response({
            'currency': currency,
            'price': bid_price,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        return web.Response(status=400, text=str(e))

async def get_price_history(request):
    page = int(request.query.get('page', 1))
    page_size = 10
    offset = (page - 1) * page_size
    
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Currency)
            .order_by(Currency.date_.desc())
            .offset(offset)
            .limit(page_size)
        )
        records = result.all()
        
        return web.json_response([{
            'id': record.id,
            'currency': record.currency,
            'price': str(record.price),
            'date': record.date_.isoformat()
        } for record in records])

async def delete_price_history(request):
    async with engine.begin() as conn:
        await conn.execute(delete(Currency))
        return web.Response(status=200) 