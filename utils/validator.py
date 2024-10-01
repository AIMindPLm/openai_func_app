from .functions import sales_order_time_filter_query , manufacturing_time_filter_query , purchase_order_time_filter_query 


# Helper function to check if the function name is valid (within scope)
def valid_function_names():
  function_map = {
    "sales_order_time_filter_query": sales_order_time_filter_query,
    "manufacturing_time_filter_query": manufacturing_time_filter_query,
    "purchase_order_time_filter_query": purchase_order_time_filter_query
}
  return function_map