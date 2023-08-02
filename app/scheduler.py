from fastapi import Depends
from rocketry import Rocketry
from rocketry.conds import every
from datetime import datetime as dt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .databases import pg_async_session

app = Rocketry(config={"task_execution": "async"})


@app.task(every("1 minutes"))
async def do_async(db: AsyncSession = pg_async_session()):
    now = dt.now()
    print("executed do_async", now.strftime("%H:%M:%S"))
    stmt = f"""
        CREATE TABLE public.test_tb_{now.hour}_{now.minute}
        (
            id serial NOT NULL,
            value double precision,
            PRIMARY KEY (id)
        );
    """
    print(stmt)
    await db.execute(text(stmt))
    await db.commit()
