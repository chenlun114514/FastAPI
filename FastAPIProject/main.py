from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import uuid

app = FastAPI()

# 挂载静态文件目录（核心配置）
app.mount("/static", StaticFiles(directory="static"), name="static")  #

# 初始化模板引擎（用于上传页面）
templates = Jinja2Templates(directory="templates")

# 确保图片存储目录存在
os.makedirs("static/images", exist_ok=True)  #


@app.post("/upload/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """文件上传接口（支持跨网络访问）"""
    try:
        # 生成唯一文件名（保留原始扩展名）
        file_ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"  #
        file_path = os.path.join("static/images", filename)

        # 保存文件到本地
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)  #

        # 动态生成完整URL（核心逻辑）
        base_url = str(request.base_url).rstrip("/")  # 处理URL格式
        full_url = f"{base_url}/static/images/{filename}"  #

        return {"url": full_url}

    except Exception as e:
        return {"error": str(e)}  #


@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """上传页面（带自动刷新）"""
    return templates.TemplateResponse("index.html", {"request": request})



