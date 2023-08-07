from django.core.exceptions import ValidationError

def read_image(actions):
    processed_data = actions.function_args.get("processed_data")
    ser_data = actions.function_args.get("ser_data")
    try:
        product_code = processed_data.get("product_code")
        processed_data["product_img"] = 'https://producthub-z.s3.ap-south-1.amazonaws.com/products/original/' + \
            str(product_code)+".jpg"

    except:
        raise ValidationError("product code not found")
    return processed_data


def write_image(actions):
    processed_data = actions.function_args.get("processed_data")
    ser_data = actions.function_args.get("ser_data")
    if "product_code" in ser_data:
        product_code = ser_data.get("product_code")
    else:
        product_code = processed_data.get("Product.product_code")
    image = ser_data.get("product_img")

    if image:
        # status = upload_file(image, "original/"+str(product_code) +
        #             ".jpg", "products", "producthub-z")
        pass
    else:
        raise ValidationError("image not found")
    return processed_data
