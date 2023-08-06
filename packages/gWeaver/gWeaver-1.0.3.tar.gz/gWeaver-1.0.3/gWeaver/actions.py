


# class product_actions:
#     entity = "Product"
#     dqquery = dgraph.dqproduct()
#     pk_field = "product_id"
#     serializer = productHubSerializer
#     fields = fields
#     pk_fetch_strategy = 0  # "requests"
#     add_functions = [
#                      {"function": generate_product_code,
#                          "methods": ["POST","PUT"]},
#                      {"function": read_image,
#                          "methods": ["GET"]},
#                      {"function": dummy,
#                          "methods": ["GET"]},
#                      {"function": write_image,
#                          "methods": ["POST", "PUT"]},
#                      {"function": seperate_search_tags,
#                          "methods": ["POST", "PUT"]},
#                      {"function": combine_search_tags,
#                          "methods": ["GET"]},
#                      {"function": send_to_elasticsearch,
#                          "methods": ["POST"]},
#                      {"function": delete_from_elasticsearch,
#                          "methods": ["DELETE"]},
#                      {"function": update_elasticsearch,
#                          "methods": ["PUT"]}]