

def is_within_scope(query):
    valid_keywords = ["product", "revenue", "sales", "profit_margin" "top","quantity", "order","customer","cost_of_goods","low","least" ]
    for keyword in valid_keywords:
        if keyword in query.lower():
            return True
    return False