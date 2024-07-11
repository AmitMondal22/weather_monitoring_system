from pydantic import BaseModel, Field, constr, validator
from datetime import date,datetime,time
import re
from typing import Optional,List


class WeatherDeviceData(BaseModel):
    CLIENT_ID:  Optional[int] = 0
    UID: str # device id
    DT: str
    TIME: str
    TW: int
    TEMERATURE: float
    RAINFALL: float
    RAINFALL_CUMULATIVE: float
    ATM_PRESSURE: float
    SOLAR_RADIATION: float
    HUMIDITY: float
    WIND_SPEED: float
    WIND_DIRECTION: float    
    RUNHR: float


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
    device_type: str
    meter_type: str
    last_maintenance: date
    @validator('meter_type')
    def validate_meter_type(cls, v):
        validate_meter_type = {"ENSF", "ENTF"}
        if v not in validate_meter_type:
            raise ValueError('Invalid alert status')
        return v
    @validator('device_type')
    def validate_device_type(cls, v):
        valid_device_type = {"EN", "UPS"}
        if v not in valid_device_type:
            raise ValueError('Invalid alert status')
        return v

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
    device_type: str
    meter_type: str
    @validator('meter_type')
    def validate_meter_type(cls, v):
        valid_meter_type = {"ENSF", "ENTF"}
        if v not in valid_meter_type:
            raise ValueError('Invalid alert status')
        return v
    @validator('device_type')
    def validate_device_type(cls, v):
        valid_device_type = {"EN", "UPS"}
        if v not in valid_device_type:
            raise ValueError('Invalid alert status')
        return v
    
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
    

class BllingData(BaseModel):
    billing_type: str
    billing_price: float
    billing_status: str
    billing_day: int

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
    billing_data: List[BllingData]
    
class OrganizationSettingsList(BaseModel):
    organization_id: int
    
class AddBill(BaseModel):
    organization_id: int
    billing_type: str
    billing_price: float
    billing_day: int
    
class EditOrganization(BaseModel):
    organization_id: int
    countries_id: int
    states_id: int
    regions_id: int
    subregions_id: int
    cities_id: int
    address: str