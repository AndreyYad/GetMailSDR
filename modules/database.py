from aiosqlite import connect
from os import mkdir
from sqlite3 import IntegrityError
from aiogram.types.user import User

async def create_database():
    try:
        mkdir('database')
    except FileExistsError:
        pass
    async with connect('database/sdr_e-mails.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("CREATE TABLE IF NOT EXISTS emails (user_id INTEGER PRIMARY KEY, username char[50], name char[50], email char[254])")
        await conn.commit()

async def save_email(user: User, email: str):
    async with connect('database/sdr_e-mails.sql') as conn:
        cur = await conn.cursor()
        try:
            await cur.execute("INSERT INTO emails (user_id, username, name, email) VALUES (?, ?, ?, ?)", (user.id, f'@{user.username}', user.full_name, email))
        except IntegrityError:
            await cur.execute("UPDATE emails SET email = ? WHERE user_id = ?", (email, user.id))
        await conn.commit()

async def get_email(user_id: int):
    async with connect('database/sdr_e-mails.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT email FROM emails WHERE user_id = ?", (user_id,))
        result = await cur.fetchall()
        if len(result) == 0:
            result = None
        else:
            result = result[0][0]
        return result
    
async def delete_email(user_id: int):
    if await get_email(user_id) is None:
        result = False
    else:
        async with connect('database/sdr_e-mails.sql') as conn:
            cur = await conn.cursor()
            await cur.execute("DELETE FROM emails WHERE user_id = ?", (user_id,))
            await conn.commit()
            result = True
    return result