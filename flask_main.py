from flask import Flask, request, render_template

@app.route("/")
def render_home():
    return "This is the main page"
    
@app.route("/add_resource", methods=["POST"])
def parse_resource():
    """Receive json input via POST requests and store them server-side"""
    try:
        arg = request.get_json()
        print(arg) 
        return "resource added!"
        

if __name__ == "__main__":
    app.run()
