from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# Dictionary to store orders in progress based on session IDs
inprogress_orders = {}

# Handles incoming requests
@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    # Dictionary mapping intents to their respective handler functions
    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order,
        'show.order.items': show_order_items
    }

    # Execute the appropriate handler function based on the intent
    return intent_handler_dict[intent](parameters, session_id)

# Save the order to the database
def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    # Insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

# Complete the order
def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having trouble finding your order. Please place a new order."
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, we couldn't process your order due to a backend error. Please place a new order."
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Order successfully placed. Your order ID is {order_id}. Total amount to pay: {order_total}."

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Add items to the order
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Please specify food items and quantities clearly."
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"Added items to your order. Current order: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Remove items from the order
def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Please place a new order."
        })
    
    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    fulfillment_text = ''

    if len(removed_items) > 0:
        fulfillment_text += f'Removed {",".join(removed_items)} from your order. '

    if len(no_such_items) > 0:
        fulfillment_text += f'Items not found in your order: {",".join(no_such_items)}. '

    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Your remaining order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Track the status of an order
def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"Order ID: {order_id}, Status: {order_status}"
    else:
        fulfillment_text = f"No order found with ID: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Show items in a specific order
def show_order_items(parameters: dict, session_id: str):
    order_id = parameters['number']
    order_details = db_helper.get_order_details(order_id)

    if order_details:
        fulfillment_text = "Items in your order:\n"
        for item in order_details:
            food_item = item[0]
            quantity = item[1]
            fulfillment_text += f"{food_item}: {quantity}\n"
    else:
        fulfillment_text = "No items found for the specified order ID."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

