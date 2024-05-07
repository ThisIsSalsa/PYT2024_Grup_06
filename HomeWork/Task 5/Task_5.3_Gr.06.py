import requests

def reverse_geocode(latitude, longitude):
    # Basicly Creates the URL that we use for the apps workflow
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"

    # Send a GET request to the API 
    response = requests.get(url)

    # Check if the request was successful (the statuse code is 200)
    if response.status_code == 200:
        data = response.json()

        # Extract relevant information from the response
        place_name = data.get('display_name', 'Not available')
        place_type = data.get('type', 'Not available')
        address = data.get('address', {})
        house_number = address.get('house_number', 'Not available')
        street_name = address.get('road', 'Not available')
        city = address.get('city', 'Not available')
        postcode = address.get('postcode', 'Not available')
        country = address.get('country', 'Not available')
        country_code = address.get('country_code', 'Not available')

        # Display the extracted information
        print("Place Name:", place_name)
        print("Place Type:", place_type)
        print("House Number:", house_number)
        print("Street Name:", street_name)
        print("City:", city)
        print("Postcode:", postcode)
        print("Country:", country)
        print("Country Code:", country_code)
    else:
        # Basic error to check if we got the datta
        print("Failed to retrieve geocoding data.")
    # basic Inputs
latitude = input("Enter latitude: ")
longitude = input("Enter longitude: ")

# Call the function and get Lan and Lon
reverse_geocode(latitude, longitude)
