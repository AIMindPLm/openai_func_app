# Define the mapping for metrics and queries
metrics_map = {
    #Top or Low Selling product by Quantity
    'product_quantity': """
        SELECT
            CASE
                WHEN p.id IS NOT NULL THEN p.name
                ELSE m.name
            END AS product_name,
            SUM(sr.quantity) AS total_quantity_sold
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        LEFT JOIN product p ON v.product_id = p.id
        LEFT JOIN material m ON v.material_id = m.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY product_name
        ORDER BY total_quantity_sold {order_direction}
        LIMIT {limit};
    """,

    #Top or Low Selling product by Revenue
    'product_revenue': """
        SELECT
            CASE
                WHEN p.id IS NOT NULL THEN p.name
                ELSE m.name
            END AS product_name,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        LEFT JOIN product p ON v.product_id = p.id
        LEFT JOIN material m ON v.material_id = m.id
        WHERE s.organization = UNHEX(REPLACE( %(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY product_name
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,

    #Top or Low Selling  product by Revenue
    'product_profit': """
        SELECT
            CASE
                WHEN p.id IS NOT NULL THEN p.name
                ELSE m.name
            END AS product_name,
            SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) AS total_profit
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        LEFT JOIN product p ON v.product_id = p.id
        LEFT JOIN material m ON v.material_id = m.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY product_name
        ORDER BY total_profit {order_direction}
        LIMIT {limit};
    """,

    #Top or Low Selling product by Profit Margin
    'product_profit_margin': """
        SELECT
            CASE
                WHEN p.id IS NOT NULL THEN p.name
                ELSE m.name
            END AS product_name,
            SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) AS total_profit,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue,
            (SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        LEFT JOIN product p ON v.product_id = p.id
        LEFT JOIN material m ON v.material_id = m.id
        WHERE s.organization = UNHEX(REPLACE( %(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY product_name
        HAVING total_revenue > 0
        ORDER BY profit_margin_percentage {order_direction}
        LIMIT {limit};
    """,
    # Top or Low Revenue from Sales Order
    'sales_order_revenue': """
        SELECT
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY sr.sales_order
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,
    
    # Top or Low Cost of Goods Sold (COGS) from Sales Order
    'sales_order_cogs': """
        SELECT
            SUM(sr.quantity * v.purchase_price) AS total_cogs
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY sr.sales_order
        ORDER BY total_cogs {order_direction}
        LIMIT {limit};
    """,
    
    #Top or Low Profit from Sales Order
    'sales_order_profit': """
        SELECT
            SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) AS total_profit
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY sr.sales_order
        ORDER BY total_profit {order_direction}
        LIMIT {limit};
    """,
    
    # Top or Low Profit Margin from Sales Order
    'sales_order_profit_margin': """
        SELECT
            (SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN variant v ON sr.variant = v.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY sr.sales_order
        HAVING SUM(sr.quantity * sr.cost_per_unit) > 0
        ORDER BY profit_margin_percentage {order_direction}
        LIMIT {limit};
    """,

    # Top or Low Revenue from Customer
    'customer_revenue': """
        SELECT
            c.id AS customer_id,
            c.company_name,
            SUM(sr.quantity * sr.cost_per_unit) AS total_revenue
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN customer c ON s.customer = c.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY c.id, c.company_name
        ORDER BY total_revenue {order_direction}
        LIMIT {limit};
    """,

    # Top or Low COGS from Customer
    'customer_quantity': """
        SELECT
            c.id AS customer_id,
            c.company_name,
            CASE
                WHEN p.id IS NOT NULL THEN p.name
                ELSE m.name
            END AS product_name,
            SUM(sr.quantity) AS total_quantity_sold
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN customer c ON s.customer = c.id
        JOIN variant v ON sr.variant = v.id
        LEFT JOIN product p ON v.product_id = p.id
        LEFT JOIN material m ON v.material_id = m.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY c.id, c.company_name, product_name
        ORDER BY total_quantity_sold {order_direction}
        LIMIT {limit};
    """,

    #Top or Low Profit from Customer
    'customer_profit': """
        SELECT
            c.id AS customer_id,
            c.company_name,
            SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) AS total_profit
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN customer c ON s.customer = c.id
        JOIN variant v ON sr.variant = v.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY c.id, c.company_name
        ORDER BY total_profit {order_direction}
        LIMIT {limit};
    """,

    #Top or Low Profit margin from Customer 
    'customer_profit_margin': """
        SELECT
            c.id AS customer_id,
            c.company_name,
            (SUM(sr.quantity * (sr.cost_per_unit - v.purchase_price)) / SUM(sr.quantity * sr.cost_per_unit)) * 100 AS profit_margin_percentage
        FROM sales_order_row sr
        JOIN sales_order s ON sr.sales_order = s.id
        JOIN customer c ON s.customer = c.id
        JOIN variant v ON sr.variant = v.id
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY c.id, c.company_name
        HAVING SUM(sr.quantity * sr.cost_per_unit) > 0
        ORDER BY profit_margin_percentage {order_direction}
        LIMIT {limit};
    """,
   # Total Amount Spend in Purchase 
   'purchase_spend': """
        SELECT
            SUM(po.total) AS total_purchase_spend
        FROM purchase_order po
        WHERE po.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter};
    """,

    # Total Purchase Orders
    'purchase_orders': """
        SELECT
            COUNT(po.id) AS total_purchase_orders
        FROM purchase_order po
        WHERE po.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter};
    """,

    # Total Production Orders
    'production_orders': """
        SELECT
            COUNT(mo.id) AS total_production_orders
        FROM manufacturing_order mo
        WHERE mo.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter};
    """,

    
  # 1. Revenue, COGS, Profit, Profit Margin
    'revenue_cogs_profit_query' : """
    SELECT
        SUM(sr.item_total) AS revenue,
        SUM(sr.quantity * v.purchase_price) AS cogs,
        SUM(sr.item_total - (sr.quantity * v.purchase_price)) AS profit,
        (SUM(sr.item_total - (sr.quantity * v.purchase_price)) / SUM(sr.item_total)) * 100 AS profit_margin_percentage
    FROM sales_order_row sr
    JOIN sales_order s ON sr.sales_order = s.id
    JOIN variant v ON sr.variant = v.id
    WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
    {time_filter}
  """,
    
    'customer_metrics_query' : """
    WITH customer_orders AS (
        SELECT
            s.customer,
            MIN(s.sales_order_date) AS first_order_date,
            COUNT(DISTINCT s.id) AS total_orders,
            SUM(s.total) AS total_revenue
        FROM sales_order s
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY s.customer
    )
    SELECT
        COUNT(DISTINCT co.customer) AS total_customers,
        SUM(co.total_orders) AS total_sales_orders,
        SUM(CASE WHEN co.first_order_date < %(period_start)s THEN co.total_revenue ELSE 0 END) AS recurring_customer_revenue,
        SUM(CASE WHEN co.first_order_date >= %(period_start)s THEN co.total_revenue ELSE 0 END) AS new_customer_revenue
    FROM customer_orders co
  """,
    # 2. Total customers, Total sales orders, Recurring Customer revenue, New customer revenue
    'customer_metrics_query' : """
    WITH customer_orders AS (
        SELECT
            s.customer,
            MIN(s.sales_order_date) AS first_order_date,
            COUNT(DISTINCT s.id) AS total_orders,
            SUM(s.total) AS total_revenue
        FROM sales_order s
        WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
        {time_filter}
        GROUP BY s.customer
    )
    SELECT
        COUNT(DISTINCT co.customer) AS total_customers,
        SUM(co.total_orders) AS total_sales_orders,
        SUM(CASE WHEN co.first_order_date < %(period_start)s THEN co.total_revenue ELSE 0 END) AS recurring_customer_revenue,
        SUM(CASE WHEN co.first_order_date >= %(period_start)s THEN co.total_revenue ELSE 0 END) AS new_customer_revenue
    FROM customer_orders co
  """,
   #  3. Top 15 Customers (based on Revenue)
  'top_customers_query' : """
    SELECT
        c.company_name,
        SUM(s.total) AS total_revenue
    FROM sales_order s
    JOIN customer c ON s.customer = c.id
    WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
    {time_filter}
    GROUP BY c.id, c.company_name
    ORDER BY total_revenue DESC
    LIMIT 15
  """,
    # 4. Customer Performance report
  'customer_performance_query' :"""
    SELECT
        c.company_name,
        SUM(sr.item_total) AS revenue,
        SUM(sr.quantity) AS quantity,
        SUM(sr.item_total - (sr.quantity * v.purchase_price)) AS profit,
        (SUM(sr.item_total - (sr.quantity * v.purchase_price)) / SUM(sr.item_total)) * 100 AS profit_margin_percentage
    FROM sales_order_row sr
    JOIN sales_order s ON sr.sales_order = s.id
    JOIN customer c ON s.customer = c.id
    JOIN variant v ON sr.variant = v.id
    WHERE s.organization = UNHEX(REPLACE(%(organization_id)s, "-", ""))
    {time_filter}
    GROUP BY c.id, c.company_name
    ORDER BY revenue DESC
  """

}

# Define the mapping for time filters
time_filters = {
    'sales_order': {
        'monthly': "AND YEAR(s.sales_order_date) = %(year)s AND MONTH(s.sales_order_date) = %(month)s",
        'quarterly': "AND YEAR(s.sales_order_date) = %(year)s AND QUARTER(s.sales_order_date) = %(quarter)s",
        'half_yearly': "AND YEAR(s.sales_order_date) = %(year)s AND CASE WHEN MONTH(s.sales_order_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "AND YEAR(s.sales_order_date) = %(year)s"
    },
    'purchase_order': {
        'monthly': "AND YEAR(po.purchase_order_date) = %(year)s AND MONTH(po.purchase_order_date) = %(month)s",
        'quarterly': "AND YEAR(po.purchase_order_date) = %(year)s AND QUARTER(po.purchase_order_date) = %(quarter)s",
        'half_yearly': "AND YEAR(po.purchase_order_date) = %(year)s AND CASE WHEN MONTH(po.purchase_order_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "AND YEAR(po.purchase_order_date) = %(year)s"
    },
    'manufacturing_order': {
        'monthly': "AND YEAR(mo.order_created_date) = %(year)s AND MONTH(mo.order_created_date) = %(month)s",
        'quarterly': "AND YEAR(mo.order_created_date) = %(year)s AND QUARTER(mo.order_created_date) = %(quarter)s",
        'half_yearly': "AND YEAR(mo.order_created_date) = %(year)s AND CASE WHEN MONTH(mo.order_created_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
        'annually': "AND YEAR(mo.order_created_date) = %(year)s"
    }
}



