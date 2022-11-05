from flask import Flask, jsonify, request, abort
import operator
import re

operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            'addition': operator.add,
            'subtraction': operator.sub,
            'multiplication': operator.mul,
            }

add_list = ["add", "plus", "sum", "+"]
subtract_list = ["minus", "subtract", "remove", "difference", "-"]
multiply_list = ["multiply", "times", "product", "*"]

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET'])
    def load_homepage():

        welcome_message = "Welcome to home page. Send your POST request"

        return welcome_message

    @app.route("/", methods=['POST'])
    def accept_POST_request():
        try:
            response = request.get_json()
            operation_type = response.get("operation_type")
            x = response.get("x")
            y = response.get("y")

            operation = operators.get(operation_type)
            if operation is not None:
                result = operation(int(x), int(y))
                result2 = str(result)

            else:
                for item in add_list:
                    if item in operation_type:
                        temp = re.findall(r'\d+', operation_type)
                        nums = list(map(int, temp))
                        operation = operators.get("addition")
                        result = operation(nums[0], nums[1])

                for item in subtract_list:
                    if item in operation_type:
                        temp = re.findall(r'\d+', operation_type)
                        nums = list(map(int, temp))
                        operation = operators.get("subtraction")
                        result = operation(nums[0], nums[1])

                for item in multiply_list:
                    if item in operation_type:
                        temp = re.findall(r'\d+', operation_type)
                        nums = list(map(int, temp))
                        operation = operators.get("multiplication")
                        result = operation(nums[0], nums[1])
                
                result2 = str(result)

            return jsonify({
            "success": True,
            "slackUsername": "Ella Maria",
            "result": result2,
            "operation_type": operation_type,
            })

        except: 
            response = request.get_json()
            if type(response.get("x")) != int:
                abort("403")
            
            if type(response.get("y")) != int:
                abort("403")

    @app.errorhandler(403)
    def wrong_format(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "wrong format. use JSON payload. ensure values are integers."
        }), 403
    
    return app
