from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.auth.router import auth_router
from src.receipts.router import receipts_router
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Context manager for setting up and tearing down application lifespan.

    :param app_instance: FastAPI application instance
    """
    # Create and set up the database
    await create_db_and_tables()
    try:
        yield
    finally:
        pass  # Add any teardown steps if necessary


# Create FastAPI application instance
app = FastAPI(title="Receipt Management API", version="1.0", lifespan=lifespan)

# Include authentication router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Include receipts router
app.include_router(receipts_router, prefix="/receipts", tags=["receipts"])
