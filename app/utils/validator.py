from .functions import add , divide , multiply , subtract


# Helper function to check if the function name is valid (within scope)
def valid_function_names():
  function_map= {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
}
  return function_map
  