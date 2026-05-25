from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("courses.json")


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def read_courses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return {"message": "FastAPI course record server is running"}


@app.get("/courses")
def get_courses():
    courses = read_courses()
    return courses


@app.post("/courses")
def add_course(course: Course):
    courses = read_courses()

    new_course = {
        "course_name": course.course_name,
        "year": course.year,
        "semester": course.semester,
        "grade": course.grade
    }

    courses.append(new_course)
    save_courses(courses)

    return {
        "message": "새 수강기록이 추가되었습니다.",
        "added_course": new_course,
        "total_count": len(courses)
    }