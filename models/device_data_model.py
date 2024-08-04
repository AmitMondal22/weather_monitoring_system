from pydantic import BaseModel, Field, constr, validator
from datetime import date,datetime,time
import re
from typing import Optional,List


class WeatherDeviceData(BaseModel):
    # CL_ID:  Optional[int] = 0
    # UID: str # device id
    # DT: str
    # TIME: str
    # TW: int
    # TEMP: float
    # RAIN: float
    # RAIN_CUM: float
    # ATM_PRESS: float
    # SOLAR_RAD: float
    # HUMID: float
    # WIND_SPD: float
    # WIND_DIR: float
    # RUNHR : float
    
    CL_ID:  Optional[int] = 0
    UID: str # device id
    DT: str
    TM: str
    TW: int
    
    C1: float #TEMP
    PULSE1: float #RAIN
    PULSE2: Optional[float] = 0.00
    C3: float #ATM_PRESS
    C6: float #SOLAR_RAD
    C2: float #HUMID
    C4: float #WIND_SPD
    C5: float #WIND_DIR
    RUNHR : Optional[float] = 0.00
    
    
    
#     {
#   "TYPE": "N", // Assuming logType = 0
#   "UID": "12345", // Example UID
#   "DT": "2024-07-25", // Example date
#   "TM": "12:34:56", // Example time
#   "TW": 80, // Example signal strength
#   "C1N": "Temperature",
#   "C1U": "Celsius",
#   "C1": 25.50,
#   "C2N": "Pressure",
#   "C2U": "Bar",
#   "C2": 1.23,
#   "C3N": "Humidity",
#   "C3U": "Percent",
#   "C3": 45.67,
#   "C4N": "Flow Rate",
#   "C4U": "Liters/Minute",
#   "C4": 30.12,
#   "C5N": "Voltage",
#   "C5U": "Volts",
#   "C5": 220.5,
#   "C6N": "Current",
#   "C6U": "Amperes",
#   "C6": 10.75,
#   "PULSE1": 1500.0,
#   "PULSE2": 3000.0,
#   "DI1": true,  // Digital Input 1 state, true indicates 'ON'
#   "DI2": false  // Digital Input 2 state, false indicates 'OFF'
# }
    
    
    


class DeviceAutoRegister(BaseModel):
    # client_id: int
    ib_id: int
    # device_id: int
    do_channel:int
    model:str
    lat:str
    lon:str
    imei_no:str


class CheckedDevices(BaseModel):
    device:str
    
class WeatherData(BaseModel):
    client_id: int
    device_id: int
    device: str
    start_date: date
    end_date: date
    
    
class TemperatureUsed(BaseModel):
    device_id: int
    device: str
    # type: str
    start_date: date
    # end_date: date
    # start_date_time: datetime = Field(..., alias="start_date_time", description="Format: '%Y-%m-%d %H:%M:%S'")
    # start_date_time: datetime
    # end_date_time: datetime
    
    
class VoltageData(BaseModel):
    client_id: int
    device_id: int
    device: str
    start_date_time: datetime
    end_date_time: datetime
    
class WsEnergyData(BaseModel):
    client_id: int
    device_id: int
    device: str
    
    
    
# ==========================================
# ==========================================



class UpsDeviceData(BaseModel):
    client_id: int
    device_id: int
    device: str
    do_channel: int
    device_location: str
    device_output_current: float
    device_input_current: float
    
    
    
# ========================================

class AddAlert(BaseModel):
    client_id: int
    organization_id: int
    device_id: int
    device: str
    unit_id: int
    alert_type: str
    alert_status: str
    alert_status: str
    alert_value: float
    alert_email : str
    create_by: int
    @validator('alert_type')
    def validate_alert_type(cls, v):
        valid_alert_types = {"3H", "2L", "1CL", "4CH"}
        if v not in valid_alert_types:
            raise ValueError('Invalid alert type')
        return v
    @validator('alert_status')
    def validate_alert_status(cls, v):
        valid_alert_status = {"Y", "N"}
        if v not in valid_alert_status:
            raise ValueError('Invalid alert status')
        return v
    @validator('alert_email')
    def validate_email(cls, alert_email):
        # Regular expression for basic email validation
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, alert_email):
            raise ValueError("Invalid email address")
        return alert_email
    
class EditAlert(BaseModel):
    alert_id: int
    client_id: int
    organization_id: int
    device_id: int
    device: str
    unit_id: int
    alert_type: str
    alert_status: str
    alert_status: str
    alert_value: float
    alert_email : str
    create_by: int
    @validator('alert_type')
    def validate_alert_type(cls, v):
        valid_alert_types = {"3H", "2L", "1CL", "4CH"}
        if v not in valid_alert_types:
            raise ValueError('Invalid alert type')
        return v
    @validator('alert_status')
    def validate_alert_status(cls, v):
        valid_alert_status = {"Y", "N"}
        if v not in valid_alert_status:
            raise ValueError('Invalid alert status')
        return v
    @validator('alert_email')
    def validate_email(cls, alert_email):
        # Regular expression for basic email validation
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, alert_email):
            raise ValueError("Invalid email address")
        return alert_email

class DeleteAlert(BaseModel):
    alert_id: int
    client_id: int
    organization_id: int
    device_id: int
    
    
class DeviceAdd(BaseModel):
    client_id: int
    device: str
    device_name: str
    do_channel: int
    model: str
    lat: str
    lon: str
    imei_no: str
    # device_type: str
    # meter_type: str
    last_maintenance: date
    # @validator('meter_type')
    # def validate_meter_type(cls, v):
    #     validate_meter_type = {"ENSF", "ENTF"}
    #     if v not in validate_meter_type:
    #         raise ValueError('Invalid alert status')
    #     return v
    # @validator('device_type')
    # def validate_device_type(cls, v):
    #     valid_device_type = {"EN", "UPS"}
    #     if v not in valid_device_type:
    #         raise ValueError('Invalid alert status')
    #     return v

class DeviceEdit(BaseModel):
    device_id:int
    client_id: int
    device: str
    device_name: str
    do_channel: int
    model: str
    lat: str
    lon: str
    imei_no: str
    # device_type: str
    # meter_type: str
    # @validator('meter_type')
    # def validate_meter_type(cls, v):
    #     valid_meter_type = {"ENSF", "ENTF"}
    #     if v not in valid_meter_type:
    #         raise ValueError('Invalid alert status')
    #     return v
    # @validator('device_type')
    # def validate_device_type(cls, v):
    #     valid_device_type = {"EN", "UPS"}
    #     if v not in valid_device_type:
    #         raise ValueError('Invalid alert status')
    #     return v
    
class UserDeviceList(BaseModel):
    client_id: int
    device_id: int
    device: str
    user_id: int
    organization_id:int



class WsDeviceData(BaseModel):
    client_id: int
    device_id: int
    device: str
    

# class BllingData(BaseModel):
#     billing_type: str
#     billing_price: float
#     billing_status: str
#     billing_day: int

class OrganizationSettings(BaseModel):
    organization_id: int
    client_id: int
    countries_id: int
    states_id: int
    regions_id: int
    subregions_id: int
    cities_id: int
    address: str
    created_by: int
    # billing_data: List[BllingData]
    
class OrganizationSettingsList(BaseModel):
    organization_id: int
    
# class AddBill(BaseModel):
#     organization_id: int
#     billing_type: str
#     billing_price: float
#     billing_day: int
    
class EditOrganization(BaseModel):
    organization_id: int
    countries_id: int
    states_id: int
    regions_id: int
    subregions_id: int
    cities_id: int
    address: str