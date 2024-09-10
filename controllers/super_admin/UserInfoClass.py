from db_model.MASTER_MODEL import select_data, insert_data,update_data,delete_data


async def upload_update_client_logo(user_data,client_name,client_address,client_mobile,client_email,filename=None):
    try:
        update_condition=f"client_id = {user_data['client_id']}"
        if filename is None:
            set_values={"client_name":client_name,"client_address":client_address,"client_mobile":client_mobile,"client_email":client_email,"create_by":user_data['user_id']}
        else:
            set_values={"logo":filename,"client_name":client_name,"client_address":client_address,"client_mobile":client_mobile,"client_email":client_email,"create_by":user_data['user_id']}
        
    
        edit_organization=update_data("md_client",set_values,update_condition)
        return edit_organization
    except Exception as e:
          raise e