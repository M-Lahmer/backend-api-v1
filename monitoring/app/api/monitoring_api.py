from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.monitoring_service import get_device_data

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/devices/{device_id}/data", response_model=List[dict])
def get_data(device_id: str, limit: int = Query(100, ge=1, le=1000)):
    """
    Récupère les mesures les plus récentes pour un device.
    """
    data = get_device_data(device_id, limit=limit)
    if data is None:
        raise HTTPException(status_code=404, detail="Device data not found")
    return data
