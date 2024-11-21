tools = [
    {
         "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together , if not any number given ask for number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
        "name": "subtract",
        "description": "Subtract the second number from the first.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
            }
        },

    },
    {
        "type": "function",
        "function": {
        "name": "multiply",
        "description": "Multiply two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
          },

       },
    },
    {
        "type": "function",
        "function": {
        "name": "divide",
        "description": "Divide the first number by the second.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
           },

       },
    }
]