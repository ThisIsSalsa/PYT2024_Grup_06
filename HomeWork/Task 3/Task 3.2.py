import re

try:
    with open('cereals.csv') as file_handle:
        # inicializē mainīgos karstajiem kelogsiem
        hot_lowest_rating = float('inf')
        hot_highest_rating = float('-inf')
        hot_lowest_name = ""
        hot_highest_name = ""
        hot_total_rating = 0
        hot_count = 0

        # Inicializē mainīgos aukstajiem kelogsiem
        cold_lowest_rating = float('inf')
        cold_highest_rating = float('-inf')
        cold_lowest_name = ""
        cold_highest_name = ""
        cold_total_rating = 0
        cold_count = 0

        # Define regex pattern to match the CSV format Nodefinē regex modeli, lait as atbilstu CSV formātam
        pattern = re.compile(r'^(.*),(.*),(.*),([\d.]+)$')

        # Loop cauri katrai līnijai failā
        for line in file_handle:
            match = pattern.match(line.strip())
            if not match:
                continue  # skipo līnijas, kuras neatbilst modelim

            name, ctype, _, rating = match.groups()  # izvelk attiecīgās grupas

            rating = float(rating)  # konvertē rating uz float

            if ctype == 'H':
                hot_total_rating += rating
                hot_count += 1
                if rating < hot_lowest_rating:
                    hot_lowest_rating = rating
                    hot_lowest_name = name
                if rating > hot_highest_rating:
                    hot_highest_rating = rating
                    hot_highest_name = name
            else:
                cold_total_rating += rating
                cold_count += 1
                if rating < cold_lowest_rating:
                    cold_lowest_rating = rating
                    cold_lowest_name = name
                if rating > cold_highest_rating:
                    cold_highest_rating = rating
                    cold_highest_name = name

        # izkalkulē vidējo reitingu karstiem un aukstiem kelogsiem
        hot_average_rating = hot_total_rating / hot_count if hot_count > 0 else 0
        cold_average_rating = cold_total_rating / cold_count if cold_count > 0 else 0

        # Izprintē rezultātus karstiem kelogsiem
        print("Cereal type: Hot")
        print("The lowest cereals rating value:", hot_lowest_rating, "Cereals name:", hot_lowest_name)
        print("The average cereals rating value: {:.2f}".format(hot_average_rating))
        print("The highest cereals rating value:", hot_highest_rating, "Cereals name:", hot_highest_name)

        # Izprintē rezultātus aukstiem kelogsiem
        print("\nCereal type: Cold")
        print("The lowest cereals rating value:", cold_lowest_rating, "Cereals name:", cold_lowest_name)
        print("The average cereals rating value: {:.2f}".format(cold_average_rating))
        print("The highest cereals rating value:", cold_highest_rating, "Cereals name:", cold_highest_name)

except FileNotFoundError:
    print('File not found.')
except Exception as e:
    print('An error occurred:', e)
