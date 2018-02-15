attachment_simple = [{
    "text": "Sample text",
    "callback_id": "coffee_order_form",
    "color": "#3AA3E3",
    "attachment_type": "default",
}]


attachment_coffee_button = [{
    "text": "Order a coffee:",
    "callback_id": "coffee_order_form",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [{
            "name": "coffee_order",
            "text": ":coffee: Order coffee",
            "type": "button",
            "value": "coffee_order"
        }]
}]


attachment_currency_dialog = [
    {
        "label": "Additional information",
        "name": "comment",
        "type": "textarea",
        "hint": "Provide additional information if needed."
    },
    {
        "text": "Choose a currency to request exchange rate:",
        "fallback": "You are unable to choose a currency",
        "callback_id": "currency_choice",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "actions": [
            {
                "name": "currency",
                "text": ":us: USD",
                "type": "button",
                "value": "USD"
            },
            {
                "name": "currency",
                "text": ":flag-eu: EUR",
                "type": "button",
                "value": "EUR"
            },
            {
                "name": "currency",
                "text": ":uk: GBP",
                "type": "button",
                "value": "GBP",
            }
        ]
    }
]

dialog_plot = {
    "title": "Draw a plot",
    "submit_label": "Submit",
    "callback_id": "draw_plot_form",
    "elements": [

        {
            "type": "text",
            "label": "y = ",
            "name": "formula"
        },

        {
            "type": "text",
            "label": "[x starts from..",
            "name": "x_from",
            "value": -1000
        },

        {
            "type": "text",
            "label": "..goes to]",
            "name": "x_to",
            "value": 1000
        },

        {
            "type": "text",
            "subtype": "number",
            "label": "x increment",
            "name": "step",
            "value": 1
        },


        {
            "label": "Colour",
            "type": "select",
            "name": "colour",
            "placeholder": "Select a colour",
            "value": "red",
            "options": [
                {
                    "label": "Red",
                    "value": "red"
                },
                {
                    "label": "Blue",
                    "value": "blue"
                },
                {
                    "label": "Green",
                    "value": "green"
                },
                {
                    "label": "Black",
                    "value": "black"
                }
            ]
        }
    ]
}