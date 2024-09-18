#Define the mapping for metrics and queries

metrics_map = {
    #Top or Low product by Quantity 
    'quantity': """
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

    #Top or Low product by Revenue 
    'revenue': """
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
    
    #Top or Low product by Revenue 
    'profit': """
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

    #Top or Low product by Profit Margin
    'profit_margin': """
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

    }

# Define the mapping for time filters
time_filters = {
    'monthly': "AND YEAR(s.sales_order_date) = %(year)s  AND MONTH(s.sales_order_date) = %(month)s",
    'quarterly': "AND YEAR(s.sales_order_date) = %(year)s  AND QUARTER(s.sales_order_date) = %(quarter)s",
    'half_yearly': "AND YEAR(s.sales_order_date) = %(year)s  AND CASE WHEN MONTH(s.sales_order_date) BETWEEN 1 AND 6 THEN 1 ELSE 2 END = %(half_year)s",
    'annually': "AND YEAR(s.sales_order_date) = %(year)s "
}

