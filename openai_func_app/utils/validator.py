from .functions import get_top_products_by_metric_and_time


def valid_function_names():
  function_map = {
    "get_top_products_by_metric_and_time": get_top_products_by_metric_and_time
}
  return function_map