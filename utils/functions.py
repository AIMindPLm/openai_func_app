# utils/functions.py
from .db_connector import connect_to_database
from metric_map import metrics_map , time_filters

def get_top_products_by_metric_and_time(metric, time_period, organization_id = '7f366021-c66a-4fdc-99ae-bdfce2113cb2', limit=int,order_direction=' ',**kwargs):

   time_params = {}

    # Determine time parameters based on the provided time_period
   if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period: 
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

   elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
           try:
              year = specific_period
              quarter = '2'
              time_params = {'year': year, 'quarter': quarter}
           except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")


   elif time_period == 'half_yearly':
         specific_period = kwargs.get('specific_period')
         if specific_period:
            try:
              year = specific_period
              half = '1'
              time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
         else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

   elif time_period == 'annually':
        specific_period = kwargs.get('specific_period') 
        if specific_period:
          try :
            year = specific_period
            time_params = {'year': year}
          except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

   else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
   query = metrics_map.get(metric).format(
        time_filter=time_filters.get(time_period),
        order_direction=order_direction,
        limit=limit,
    )
  # Add time filter parameters like year, month, etc.
  # Execute the query with the provided time_params
   conn = connect_to_database()
   cursor = conn.cursor(dictionary=True)
   cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
   result = cursor.fetchall()
   return result



def sales_order_time_filter_query(metric, time_period, organization_id = '7f366021-c66a-4fdc-99ae-bdfce2113cb2', limit=int,order_direction=' ',**kwargs):

   time_params = {}

    # Determine time parameters based on the provided time_period
   if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

   elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
           try:
              year = specific_period
              quarter = '2'
              time_params = {'year': year, 'quarter': quarter}
           except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")


   elif time_period == 'half_yearly':
         specific_period = kwargs.get('specific_period')
         if specific_period:
            try:
              year = specific_period
              half = '1'
              time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
         else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

   elif time_period == 'annually':
        specific_period = kwargs.get('specific_period')
        if specific_period:
          try :
            year = specific_period
            time_params = {'year': year}
          except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

   else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
   query = metrics_map.get(metric).format(
        time_filter=time_filters['sales_order'].get(time_period),
        order_direction=order_direction,
        limit=limit,
    )
  # Add time filter parameters like year, month, etc.
  # Execute the query with the provided time_params
   conn = connect_to_database()
   cursor = conn.cursor(dictionary=True)
   cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
   result = cursor.fetchall()
   return result


def manufacturing_time_filter_query(metric, time_period, organization_id = '7f366021-c66a-4fdc-99ae-bdfce2113cb2', limit=int,order_direction=' ',**kwargs):

   time_params = {}

    # Determine time parameters based on the provided time_period
   if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

   elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
           try:
              year = specific_period
              quarter = '2'
              time_params = {'year': year, 'quarter': quarter}
           except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")


   elif time_period == 'half_yearly':
         specific_period = kwargs.get('specific_period')
         if specific_period:
            try:
              year = specific_period
              half = '1'
              time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
         else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

   elif time_period == 'annually':
        specific_period = kwargs.get('specific_period')
        if specific_period:
          try :
            year = specific_period
            time_params = {'year': year}
          except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

   else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
   query = metrics_map.get(metric).format(
        time_filter=time_filters['manufacturing_order'].get(time_period),
        order_direction=order_direction,
        limit=limit,
    )
  # Add time filter parameters like year, month, etc.
  # Execute the query with the provided time_params
   conn = connect_to_database()
   cursor = conn.cursor(dictionary=True)
   cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
   result = cursor.fetchall()
   return result


def purchase_order_time_filter_query(metric, time_period, organization_id = '7f366021-c66a-4fdc-99ae-bdfce2113cb2', limit=int,order_direction=' ',**kwargs):

   time_params = {}

    # Determine time parameters based on the provided time_period
   if time_period == 'monthly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
            try:
                year, month = specific_period.split('-')
                time_params = {'year': year, 'month': month}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-MM'.")
        else:
            raise ValueError("specific_period is required for monthly time period.")

   elif time_period == 'quarterly':
        specific_period = kwargs.get('specific_period')
        if specific_period:
           try:
              year = specific_period
              quarter = '2'
              time_params = {'year': year, 'quarter': quarter}
           except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-QX'.")
        else:
            raise ValueError("Both 'year' and 'quarter' are required for quarterly time period.")


   elif time_period == 'half_yearly':
         specific_period = kwargs.get('specific_period')
         if specific_period:
            try:
              year = specific_period
              half = '1'
              time_params = {'year': year, 'half_year': half}
            except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY-HX'.")
         else:
            raise ValueError("Both 'year' and 'half' are required for half-yearly time period.")

   elif time_period == 'annually':
        specific_period = kwargs.get('specific_period')
        if specific_period:
          try :
            year = specific_period
            time_params = {'year': year}
          except ValueError:
                raise ValueError(f"Invalid specific_period format: {specific_period}. Expected 'YYYY'.")
        else:
            raise ValueError("Year is required for annual time period.")

   else:
        raise ValueError(f"Unsupported time_period: {time_period}")

    # Prepare the query by replacing the time_filter placeholder with the correct filter
   query = metrics_map.get(metric).format(
        time_filter=time_filters['purchase_order'].get(time_period),
        order_direction=order_direction,
        limit=limit,
    )
  # Add time filter parameters like year, month, etc.
  # Execute the query with the provided time_params
   conn = connect_to_database()
   cursor = conn.cursor(dictionary=True)
   cursor.execute(query, {
        'organization_id': organization_id,
        **time_params
    })
   result = cursor.fetchall()
   return result





