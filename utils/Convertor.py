def textToCommands(text: str):
    
    return text.split('\n')

def makeCorrectResponsePackage(data):
    
    return {'state': True, 'data': data}

def makeFailResponsePackage(errorMessage):

    return {'state': False, 'data': errorMessage}

if __name__ == "__main__":
    
    filename = "demofile2.txt"

    f = open(f"./AllFile/{filename}", "r")
    data = f.read()
    f.close()

    print(textToCommands(data))