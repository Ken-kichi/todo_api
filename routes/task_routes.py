from fastapi import APIRouter, Depends,HTTPException
from typing import List
from models import User, Task, Message, TaskRead
from connect_db import ConnectDB
from db_manager import DatabaseManager
from fastapi.responses import JSONResponse
from routes.auth_routes import get_current_active_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# all_task
@router.get("/", response_model=List[TaskRead])
async def all_tasks(current_user: User = Depends(get_current_active_user)):
    connect_db = ConnectDB()
    conn = connect_db.get_connection()
    db_manager = DatabaseManager()
    tasks = db_manager.read_all_task_record_by_general_user(conn, current_user.id)

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for the user."
        )
    return tasks



# detail_task
@router.get("/{id}", response_model=TaskRead)
async def task(id, current_user: User = Depends(get_current_active_user)):

    connect_db = ConnectDB()
    conn = connect_db.get_connection()
    db_manager = DatabaseManager()
    task = db_manager.read_task_record_by_id(conn, id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for the user."
        )

    return task


# add_task
@router.post("/", response_model=Message)
async def create_task(form_data: Task, current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        db_manager = DatabaseManager()
        message = db_manager.create_task_record(
            conn=conn,
            title=form_data.title,
            description=form_data.description,
            user_id=form_data.user_id
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

# edit_task
@router.put("/{id}", response_model=Message)
async def update_task(id, form_data: TaskRead, current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        db_manager = DatabaseManager()
        message = db_manager.update_task_record(
            conn=conn,
            id=id,
            title=form_data.title,
            description=form_data.description,
            completed=form_data.completed,
            user_id=form_data.user_id
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

# delete_task
@router.delete("/{id}", response_model=Message)
async def delete_task(id, current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        db_manager = DatabaseManager()
        message = db_manager.delete_task_record(
            conn=conn,
            id=id,
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )
