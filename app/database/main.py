from fastapi import FastAPI, HTTPException
from database import get_db_connection
import pyodbc
from models import UserCreate, TaskCreate

app = FastAPI()

@app.post('/users/')
async def create_user(user: UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (user.username, user.email, user.password_hash))
        conn.commit()
        return {'message': 'Користувач успішно створений'}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get('/users/')
async def get_users():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        if not users:
            raise HTTPException(status_code=404, detail="Користувачі не знайдені")
        return {"users": [dict(zip([column[0] for column in cursor.description], row)) for row in users]}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        return {"message": "Користувач успішно видалений"}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.put('/users/{user_id}')
async def update_user(user_id: int, user: UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET username = ?, email = ?, password_hash = ? WHERE id = ?", (user.username, user.email, user.password_hash, user_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        return {"message": "Користувач успішно оновлений"}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.post('/tasks/')
async def create_task(task: TaskCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tasks_active (user_id, title, description, category, duration, date_of_deadline,  description_length, priority) VALUES (?,?,?,?,?,?,?,?)", (task.user_id, task.title, task.description, task.category, task.duration, task.date_of_deadline,  task.description_length, task.priority))
        cursor.execute("INSERT INTO tasks_passive (title, description, category, duration, date_of_deadline,  description_length, priority) VALUES (?,?,?,?,?,?,?)", (task.title, task.description, task.category, task.duration, task.date_of_deadline,  task.description_length, task.priority))
        conn.commit()

        return {'message': 'Завдання успішно створено'}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks_active WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Завдання не знайдено")
        return {"message": "Завдання успішно видалено"}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()
    
@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task: TaskCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE tasks_active SET title = ?, description = ?, category = ?, duration = ?, date_of_deadline = ?, description_length = ?, priority = ? WHERE id = ?", (task.title, task.description, task.category, task.duration, task.date_of_deadline, task.description_length, task.priority, task_id))
        cursor.execute("UPDATE tasks_passive SET title = ?, description = ?, category = ?, duration = ?, date_of_deadline = ?, description_length = ?, priority = ? WHERE id = ?", (task.title, task.description, task.category, task.duration, task.date_of_deadline, task.description_length, task.priority, task_id))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Завдання не знайдено")
        
        return {"message": "Завдання успішно оновлено"}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get('/tasks/')
async def get_tasks(user_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Помилка підключення до БД")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM tasks_active WHERE user_id = ?", (user_id,))
        tasks = cursor.fetchall()

        if not tasks:  
            raise HTTPException(status_code=404, detail="Завдання не знайдено")
        return {'tasks': [dict(zip([column[0] for column in cursor.description], row)) for row in tasks]}
    except pyodbc.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()


