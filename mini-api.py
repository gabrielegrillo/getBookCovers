import flask, requests, os
from flask import request, jsonify


apikey = os.environ.get('API_Key')
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def getISBN13(originalISBN): 
    FinalResult = "978" + str(originalISBN[:len(originalISBN)-1])
    Weight = 1
    Sum = 0
    for i in range(0, len(FinalResult)): 
        Sum += int(FinalResult[i]) * Weight
        if (Weight == 1):
            Weight = 3
        else:
            Weight = 1
    Module = Sum % 10
    
    # Like how it is described in the documentations, if the result of mod 10 is equal to zero, it can be placed as the final and checkdigit. 
    if (Module == 0):
        FinalResult += str(Module)
    else:
        Checkdigit = 10 - int(Module)
        FinalResult += str(Checkdigit)
    
    return str(FinalResult)


@app.route('/api/getbookcover', methods=['GET'])
def api_bookcover():
    
    if 'isbn' in request.args:
        # Removes the upper-dash included in the ISBN-13 (if there's any...)
        isbn = request.args['isbn'].replace('-','') 
        if (len(isbn) == 10):
            isbn = getISBN13(isbn)
        elif (len(isbn) > 13 or len(isbn) < 10):
            return "Error: ISBN is not valid"
    else:
        return "Error: No ISBN-10 or ISBN-13 found. Please specify the ISBN."

    req = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={apikey}")
    if (req.status_code == 200):
        jsonResp = req.json()
        urlBookCover = jsonResp["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        return jsonify(status=200, Url=urlBookCover)
    else:
        print(req.content)
        return "Error on making the request to the server, check the log on the server's console" 

app.run()