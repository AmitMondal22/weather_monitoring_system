from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from utils.response import errorResponse, successResponse
from models import device_data_model
from controllers.device_to_server import WeatherController,DeviceController

import json

devices_routes = APIRouter()


@devices_routes.post("/device_auto_register")
async def post_device_auto_register(data: device_data_model.DeviceAutoRegister):
    try:
        controllerRes =  await DeviceController.device_auto_register(data)
        resdata = successResponse(controllerRes, message="Device registered successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@devices_routes.post('/checked_devices')
async def post_checked_devices(data: device_data_model.CheckedDevices):
    try:
        controllerRes =  await DeviceController.checked_devices(data)
        resdata = successResponse(controllerRes, message="Device checked successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



# ==============================================================================
# # modifications
# ==============================================================================
@devices_routes.post('/weather_data')
async def post_weather_data(data: device_data_model.WeatherDeviceData):
    try:
        controllerRes =  await WeatherController.get_weather_data(data,data.CL_ID,data.UID)
        resdata = successResponse(controllerRes, message="data stored successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
# ==============================================================================
# # modifications
# ==============================================================================

@devices_routes.post("/ws_data_wms")
async def post_ws_data(data: device_data_model.WsDeviceData):
    try:
        print(">>>>>>>>>>>>>>....",data)
        await WeatherController.send_last_weather_data(client_id=data.client_id, device_id=data.device_id, device=data.device)
        resdata = successResponse("success", message="data stored successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

