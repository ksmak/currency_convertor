from flask import Flask, render_template, request, jsonify

import service

# global variable for save currency list
currency_list = service.load_all_currency()

app = Flask(__name__)

@app.route("/")
def main():
    global currency_list

    convert_type = request.args.get('convert_type')
    convert_name = request.args.get('convert_name')
    count = request.args.get('count')
    json = request.args.get('json')
    

    curr_list = []
    if convert_type != None:
        for currency in currency_list:
            if currency['convert_type'] == convert_type:
                curr_list.append(currency)

    result = {}
    if len(curr_list) > 0 and convert_type != None and convert_name != None and count != None and count != '':
        currency = service.get_currency(curr_list, convert_type, convert_name)
        if currency != None:
            result = {
                "sale": "{:.2f}".format(currency["sale"] * int(count)),
                "buy": "{:.2f}".format(currency["buy"] * int(count)),
            }
    
    if json:
        return jsonify(result)
        
    return render_template(
        "index.html", 
        currency_list=curr_list, 
        convert_type=convert_type, 
        convert_name=convert_name,
        count=count,
        result=result,
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
