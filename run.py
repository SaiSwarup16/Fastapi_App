if __name__ == "__main__":
    import uvicorn
    from app.main import app  # Use absolute import path

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
