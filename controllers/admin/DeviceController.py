from db_model.MASTER_MODEL import select_data,update_data,select_one_data,batch_insert_data,insert_data
from utils.date_time_format import get_current_datetime, get_current_date_time_utc
from utils.last12month import last_12_month
from routes.mqtt_routes import subscribe_topics


@staticmethod
async def list_device(client_id):
    try:
        select="device_id, device"
        # select="device_id, device, do_channel, model, lat, lon, imei_no, last_maintenance, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        condition=f"client_id={client_id}"
        data = select_data("md_device", select, condition)
        return data
    except Exception as e:
        raise e
    
    
@staticmethod
async def user_device_list(client_id, user_id, organization_id):
    try:
        select="d.device_id, d.device, d.do_channel, d.model, d.lat, d.lon, d.imei_no, d.last_maintenance, DATE_FORMAT(d.created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(d.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        
        condition = f"d.device_id = mud.device_id AND d.client_id = mud.client_id AND mud.client_id = {client_id} AND mud.user_id = {user_id} AND mud.organization_id = {organization_id}"
        find_devices=select_data("md_device AS d, md_manage_user_device AS mud", select, condition,order_by="d.device_id ASC")
        print("find_devices>>>>>>>>>>>>>>>>>",find_devices)
        return find_devices
    except Exception as e:
        raise ValueError("Could not fetch data")


@staticmethod
async def device_info(params,userdata):
    try:
        condition = f"client_id={userdata['client_id']} AND device_id = {params.device_id}"
        select="device_id, client_id, device, device_name, do_channel, model, lat, lon, imei_no, last_maintenance, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        data = select_one_data("md_device",select, condition,order_by="device_id DESC")
        
        # select2="count(a.alert_id) alert, a.alert_type, a.unit_id,u.unit,u.unit_name"
        # condition2 = f"a.unit_id=u.unit_id AND a.client_id={userdata['client_id']} AND a.device_id = {params.device_id} GROUP BY a.alert_type, a.unit_id, u.unit, u.unit_name"
        # table2="td_alert AS a, md_unit AS u"
        # alert=select_data(table2,select2, condition2)
        
        return {"data":data}
        # return {"data":data, "data2":alert}
    except Exception as e:
        raise e

@staticmethod
async def add_device(params):
    try:
        
        
        column="client_id, device, device_name, do_channel, model, lat, lon, imei_no, last_maintenance, created_at"
        
        rows_data = []
        for params_data in params:
            row_data = {
                "client_id": params_data.client_id,
                "device": params_data.device,
                "device_name": params_data.device_name,
                "do_channel": params_data.do_channel,
                "model": params_data.model,
                "lat": params_data.lat,
                "lon": params_data.lon,
                "imei_no": params_data.imei_no,
                "last_maintenance": params_data.last_maintenance,
                "created_at": get_current_datetime()  # Assuming get_current_datetime() returns the current datetime
            }
            rows_data.append(row_data)        
        batch_dataid=batch_insert_data("md_device", column, rows_data)
        print("batch_dataid---------------------", batch_dataid)
        
        
        await subscribe_topics()
        return batch_dataid
    except Exception as e:
        raise e
    
@staticmethod
async def edit_device(params):
    try:
        condition = f"device_id = {params.device_id} AND client_id = {params.client_id}"
        columns={"device":params.device, "device_name":params.device_name, "do_channel":params.do_channel, "model":params.model, "lat":params.lat, "lon":params.lon, "imei_no":params.imei_no, "updated_at":get_current_datetime()}
        data = update_data("md_device", columns, condition)
        print(data)
        return data
    except Exception as e:
        raise e
    

@staticmethod
async def manage_list_device(params):
    try:
        condition = f"a.client_id = {params.client_id}"
        
        select="a.device_id, a.client_id, a.device, a.device_name, a.do_channel, a.model, a.lat, a.lon, a.imei_no, a.last_maintenance, DATE_FORMAT(a.created_at, '%Y-%m-%d') AS device_created_at,DATE_FORMAT(a.updated_at, '%Y-%m-%d %H:%i:%s') AS device_updated_at, b.weather_data_id, b.device_id AS b_device_id, b.do_channel AS b_do_channel, b.e1, b.e2, b.e3, b.r, b.y, b.b, b.r_y, b.y_b, b.b_r, b.curr1, b.curr2, b.curr3, b.activep1, b.activep2, b.activep3, b.apparentp1, b.apparentp2, b.apparentp3, b.pf1, b.pf2, b.pf3, b.freq, b.reactvp1, b.reactvp2, b.reactvp3, b.avaragevln, b.avaragevll, b.avaragecurrent, b.totkw, b.totkva, b.totkvar, b.runhr,  DATE_FORMAT(b.date, '%Y-%m-%d') AS date, TIME_FORMAT(b.time, '%H:%i:%s') AS time, DATE_FORMAT(b.created_at, '%Y-%m-%d %H:%i:%s') AS energy_data_created_at, DATE_FORMAT(b.updated_at, '%Y-%m-%d %H:%i:%s') AS energy_data_updated_at"
        
        table="""md_device a LEFT JOIN (SELECT t1.*
    FROM td_weather_data t1
    INNER JOIN (
        SELECT device_id, MAX(CONCAT(date, ' ', time)) AS max_datetime
        FROM td_weather_data
        GROUP BY device_id
    ) t2 ON t1.device_id = t2.device_id AND CONCAT(t1.date, ' ', t1.time) = t2.max_datetime) b ON a.device_id = b.device_id AND a.client_id = b.client_id"""
        
        order_by="a.device_id ASC"
        data = select_data(table, select,condition,order_by)
        print("????????????????>>>>>>>>>>>>>>>>",data)
        return data
    except Exception as e:
        raise e
    



    
# =========================================================
@staticmethod
async def weather_data(params,user_data):
    try:
        select="wd.weather_data_id, wd.client_id, wd.device_id, wd.device, wd.tw, wd.temperature, wd.rainfall, wd.rainfall_cumulative, wd.atm_pressure, wd.solar_radiation, wd.humidity, wd.wind_speed, wd.wind_direction, wd.runhr, wd.date, wd.time, wd.created_at, wd.updated_at"
        condition=f"wd.client_id = {user_data['client_id']} AND wd.device_id = {params.device_id} AND wd.date BETWEEN '{params.start_date}' AND '{params.end_date}'"
        data = select_data("td_weather_data AS wd",select, condition,order_by="wd.date DESC, wd.time DESC")
        return data
    except Exception as e:
        raise e


@staticmethod
async def temperature(params,user_data):
    try:
        select="ed.date, ed.time, ed.temperature"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def rainfall_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.rainfall, ed.rainfall_cumulative"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e

@staticmethod
async def atm_pressure_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.atm_pressure"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    
    
@staticmethod
async def solar_radiation_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.solar_radiation"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def humidity_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.humidity"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def wind_speed_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.wind_speed,ed.wind_direction"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    
async def wind_direction_data(params,user_data):
    try:
        select="ed.date, ed.time, ed.wind_speed,ed.wind_direction"
        condition=f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND ed.date ='{params.start_date}'"
        data = select_data("td_weather_data AS ed",select, condition,order_by="date DESC, time DESC")
        return data
    except Exception as e:
        raise e
    


@staticmethod
async def organization_settings(client_id,user_id,params):
    try:
        columndata="organization_id, client_id, countries_id, states_id, regions_id, subregions_id, cities_id, address, create_by, created_at"
        insdata=f"{params.organization_id}, {params.client_id}, {params.countries_id}, {params.states_id}, {params.regions_id}, {params.subregions_id}, {params.cities_id}, '{params.address}', {user_id}, '{get_current_datetime()}'"
        st_view_organization=insert_data("st_ms_organization",columndata,insdata)
    
    
        res={"settings_organization":st_view_organization}
        return res
    except Exception as e:
        raise e
    
@staticmethod
async def organization_settings_list(client_id,user_id,params):
    try:
        condition = f"""st_org.cities_id = mlc.id
                        AND st_org.states_id = mls.id
                        AND st_org.countries_id = mlco.id
                        AND st_org.regions_id = mlr.id
                        AND st_org.subregions_id = mlsr.id
                        AND st_org.client_id = {client_id}
                        AND st_org.organization_id = {params.organization_id}"""
        
        select="st_org.id_ms_organization,st_org.organization_id, st_org.client_id, st_org.countries_id, st_org.states_id, st_org.regions_id, st_org.subregions_id, st_org.cities_id, st_org.address, DATE_FORMAT(st_org.created_at, '%Y-%m-%d %H:%i:%s') AS created_at, mlc.name AS cityes, mls.name AS state, mlco.name AS countries, mlr.name AS subregions, mlsr.name AS regions"
        table="st_ms_organization AS st_org, md_lo_cities AS mlc, md_lo_states AS mls, md_lo_countries AS mlco, md_lo_regions AS mlr, md_lo_subregions AS mlsr"
        data = select_data(table,select, condition)
        return data
    except Exception as e:
        raise e
    
    

    
@staticmethod
async def edit_organization_info(client_id,user_id,params):
    try:
        update_condition=f"client_id = {client_id} AND organization_id = {params.organization_id}"
        set_values={"countries_id":params.countries_id,"states_id":params.states_id,"regions_id":params.regions_id,"subregions_id":params.subregions_id,"cities_id":params.cities_id,"address":params.address,"create_by":user_id}
        edit_organization=update_data("st_ms_organization",set_values,update_condition)
        return edit_organization
    except Exception as e:
        raise e