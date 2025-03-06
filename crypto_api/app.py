from aiohttp import web
from controllers.price_controller import get_price, get_price_history, delete_price_history
from middleware.error_handling import handle_error
from config import DATABASE_URL
import asyncpg
import asyncio

app = web.Application(middlewares=[handle_error])

app.router.add_get('/price/{currency}', get_price)
app.router.add_get('/price/history', get_price_history)
app.router.add_delete('/price/history', delete_price_history)

async def init_db():
    db_url = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(db_url)
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS currencies (
                id SERIAL PRIMARY KEY,
                currency VARCHAR(10) NOT NULL,
                date_ TIMESTAMP DEFAULT date_trunc('second', CURRENT_TIMESTAMP),
                price DECIMAL(20, 8) NOT NULL
            )
        ''')
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
    web.run_app(app) 