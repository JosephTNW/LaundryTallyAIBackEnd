from flask import url_for

def launderer_to_dict(launderer):
    if launderer:
        return {
            "id": launderer.id,
            "name": launderer.name,
            "phone_num": launderer.phone_num,
            "launderer_pic": url_for("serve_launderer_image", filename=launderer.l_pic),
            "address": launderer.address,
            "desc": launderer.desc,
            "has_whatsapp": launderer.has_whatsapp,
            "has_delivery": launderer.has_delivery,
            "inputted_at": launderer.inputted_at
        }
    return None

def clothes_to_dict(clothes):
    if clothes:
        return {
            "id": clothes.id,
            "color": clothes.color,
            "cloth_pic": url_for("serve_clothes_image", filename=clothes.cloth_pic),
            "desc": clothes.desc,
            "inputted_at": clothes.inputted_at,
            "type": clothes.c_type
        }
    return None