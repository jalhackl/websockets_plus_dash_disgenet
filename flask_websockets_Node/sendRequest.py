import requests

def send(adress, data):  
    # Sample array

    
    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/in', json=data) 
    
    # Convert response data to json
    #returned_data = res.json() 
    
    #print(returned_data)
