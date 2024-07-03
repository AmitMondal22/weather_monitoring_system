from db_model.MASTER_MODEL import insert_data,select_one_data
from utils.date_time_format import get_current_datetime,get_current_date,get_current_time

from Library.DecimalEncoder import DecimalEncoder
import json





@staticmethod
async def get_ups_data(data):
    try:
        current_datetime = get_current_datetime()
        columns = "client_id, device_id, device, do_channel, output_current, input_current,date, time, created_at"
        value = f"{data.client_id},{data.device_id}, '{data.device}', {data.do_channel}, {data.device_output_current}, {data.device_input_current}, '{get_current_date()}', '{get_current_time()}', '{current_datetime}'"
        ups_data_id = insert_data("td_ups_data", columns, value)
        if ups_data_id is None:
            raise ValueError("Ups data was not inserted")
        else:
            from routes.api_client_routes import SendEnergySocket
            lastdata=await send_last_energy_data(data.client_id, data.device_id, data.device)
            if lastdata is None:
                raise ValueError("Could not fetch data")
            user_data = {"ups_data_id":ups_data_id, "device_id": data.device_id, "device": data.device, "do_channel": data.do_channel}
        return user_data
    except Exception as e:
        raise ValueError("Could not fetch data")
  
@staticmethod  
async def send_last_energy_data(client_id, device_id, device):
        try:
            # Lazy import inside the function
            from Library.WsConnectionManagerManyDeviceTypes import WsConnectionManagerManyDeviceTypes
            manager = WsConnectionManagerManyDeviceTypes()
            
            condition = f"device_id = '{device_id}' AND device ='{device}' AND client_id = '{client_id}'"
            order_by="energy_data_id DESC" 
            lastdata = select_one_data("td_ups_data", "*", condition, order_by)
           
            await manager.send_personal_message("UPS",client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            
            print("lastdata last energy data>>>>>>>>>>/////////",json.dumps(lastdata, cls=DecimalEncoder))
            return json.dumps(lastdata, cls=DecimalEncoder)
        except Exception as e:
            raise ValueError("Could not fetch data")
 