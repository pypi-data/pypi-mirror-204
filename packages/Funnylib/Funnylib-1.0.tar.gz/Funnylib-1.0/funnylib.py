import requests, random

def GenerateJsonResponse(url):
    """
    
    Args:
        url (str): URL to get JSON response from
        
    Returns:
        JSON code with response for given url
    """
    response = requests.get(url)
    return response.json()
    
def RandomJoke():
    """Generates random joke
    
    Returns:
        JSON code with joke
    """
    url = 'https://some-random-api.ml/others/joke'
    return GenerateJsonResponse(url)
    
def RandomAnimalFact():
    """Generates a random animal fact

    Returns:
        JSON code with animal and fact about it
    """
    animal_int = random.randint(0, 5)
    if animal_int == 0:
        animal = 'bird'
    elif animal_int == 1:
        animal = 'cat'
    elif animal_int == 2:
        animal = 'dog'
    elif animal_int == 3:
        animal = 'fox'
    elif animal_int == 4:
        animal = 'koala'
    elif animal_int == 5:
        animal = 'panda'
            
    url = f'https://some-random-api.ml/facts/{animal}'
    response = GenerateJsonResponse(url)
    return {"animal": animal, "fact": response["fact"]}

def RandomAnimalImage():
    """Generate a random animal image link

    Returns:
        JSON code with animal and image_link
    """
    animal_int = random.randint(0, 5)
    if animal_int == 0:
        animal = 'bird'
    elif animal_int == 1:
        animal = 'cat'
    elif animal_int == 2:
        animal = 'dog'
    elif animal_int == 3:
        animal = 'fox'
    elif animal_int == 4:
        animal = 'koala'
    elif animal_int == 5:
        animal = 'panda'
        
    url = f'https://some-random-api.ml/img/{animal}'
    response = GenerateJsonResponse(url)
    return {"animal": animal, "image_link": response["link"]}

class OverlayType():
    """Overlay options for GenerateAvatarOverlay() function
    """
    comrade = ['comrade', 'https://some-random-api.ml/canvas/overlay/comrade?avatar=']
    gay = ['gay', 'https://some-random-api.ml/canvas/overlay/gay?avatar=']
    glass = ['glass', 'https://some-random-api.ml/canvas/overlay/glass?avatar=']
    jail = ['jail', 'https://some-random-api.ml/canvas/overlay/jail?avatar=']
    passed = ['passed', 'https://some-random-api.ml/canvas/overlay/passed?avatar=']
    triggered = ['triggered', 'https://some-random-api.ml/canvas/overlay/triggered?avatar=']
    wasted = ['wasted', 'https://some-random-api.ml/canvas/overlay/comrade?avatar=']
    
def GenerateAvatarOverlay(avatar_url: str, overlay_type: OverlayType):
    """Generate an avatar overlay

    Args:
        avatar_url (str): link/url to your avatar
        overlay_type (OverlayType): type of overlay that you want to generate

    Returns:
        JSON code with overlay_type and overlay_url
    """
    url = f'{overlay_type[1]}{avatar_url}'
    return {"overlay_type": overlay_type[0], "overlay_url": url}

class Base64Functions():
    """Encode/decode options to use in Base64DecodeEncode() function
    """
    decode = ['decode', 'https://some-random-api.ml/others/base64?decode=']
    encode = ['encode', 'https://some-random-api.ml/others/base64?encode=']

def Base64DecodeEncode(text: str, function: Base64Functions):
    """Function to decode and encode strings using Base64

    Args:
        text (str): what do you want to decode/encode fe. print('Hello, world!')
        function (Base64Functions): what you want to do encode/decode

    Returns:
        JSON code with choosen option and result
    """
    url = f'{function[1]}{text}'
    response = GenerateJsonResponse(url)
    if function[0] == 'encode':
        return {"function": function[0], "text": text, "encoded_output": response["base64"]}
    else:
        return {"function": function[0], "text": text, "decoded_output": response["text"]}