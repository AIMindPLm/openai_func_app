tools = [
    {
        "type": "function",
        "function": {
            "name": "get_top_products_by_metric_and_time",
            "description": "Fetch the top or low-performing products based on a specific metric (quantity, revenue, profit, or profit margin) and time period (monthly, quarterly, half-yearly, or annually).",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "description": "The metric to rank products by. Possible values: 'quantity', 'revenue', 'profit', 'profit_margin'.",
                        "enum": ["quantity", "revenue", "profit", "profit_margin"]
                    },
                    "time_period": {
                        "type": "string",
                        "description": "The time period for filtering the products. Possible values: 'monthly', 'quarterly', 'half_yearly', 'annually'.if not given anything about time period use monthly",
                        "enum": ["monthly", "quarterly", "half_yearly", "annually"]
                    },
                    "specific_period": {
                        "type": "string",
                        "description": "The specific period for the chosen time period. Format: 'YYYY-MM' for monthly, 'YYYY-QX' for quarterly, 'YYYY-HX' for half-yearly, or 'YYYY' for annually.",
                        "default": "Use Current Year and August Month as 2024-08"
                    },
                    "order_direction": {
                    "type": "string",
                    "description": "The direction of sorting. Use 'DESC' for top products and 'ASC' for low-performing products.",
                    "enum": ["ASC", "DESC"],
                    "default": "DESC"
                   },
                    "limit": {
                        "type": "integer",
                        "description": "The number of top products to return.",
                        "default": 5
                    }
                },
                "required": ["metric", "time_period", "specific_period", "limit"]
            }
        }
    }
]
