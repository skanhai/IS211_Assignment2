import argparse
import urllib.request
import logging
import datetime




logging.basicConfig(filename='error.log', level=logging.ERROR)

logger = logging.getLogger('assignment2')


def downloadData(url):

    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    return response



def processData(file_content):

    user_info = dict()

    for x, line in enumerate(file_content.split("\n")):
        if x == 0:
            continue
        if len(line) == 0:
            continue

        component = line.split(",")

        name = component[1]

        id = int(component[0])

        try:
            DOB = datetime.datetime.strptime(component[2], "%d/%m/%Y")

        except ValueError:
            logging.error(f"Error processing line #{x} for ID #{id}")

        user_info[id] = (name, DOB)

    return user_info


def displayPerson(id, personData):
    try:
        name, date = personData[id]
        print(f"Person #{id} is {name} with a birthday of {date:%Y-%m-%d}")

    except KeyError:
        print(f"No user found with that id")


def main(url):

    print(f"Running main with URL = {url}...")
    csvData = downloadData(url)

    user_data = processData(csvData)
    while True:
        try:
            id = int(input("Enter an ID to lookup:"))
            if id <= 0:
                print("Exiting Program")
                break
            displayPerson(id, user_data)
        except ValueError:
            print("Please enter an integer.")


if __name__ == "__main__":
    """Main entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
