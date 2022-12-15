import hashlib
import json

def textToCommands(text: str):
    
    return text.split('\n')

def makeCorrectResponsePackage(data):
    
    return {'state': True, 'data': data}

def makeFailResponsePackage(errorMessage):

    return {'state': False, 'data': errorMessage}

def hashText(text):
    """
        Basic hashing function for a text using random unique salt.  
    """

    with open("config/hash.json") as hash_file:
        hash = json.load(hash_file)
    salt = hash['salt']
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest()

if __name__ == "__main__":
    
    filename = "demofile2.txt"

    f = open(f"./AllFile/{filename}", "r")
    data = f.read()
    f.close()

    print(textToCommands(data))