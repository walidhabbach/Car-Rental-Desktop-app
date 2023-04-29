import requests
import json
from bs4 import BeautifulSoup
import sys

class scrap:
    def __init__(self):
        with open('./Scraping/brands_modelsAll.json') as f:
            self.data = json.load(f)
    def dowloadScript(self,url):
        # Send a GET request to the URL and get the response
        response = requests.get(url)

        # Check if the request was successful (status code 200 indicates success)
        if response.status_code == 200:
            # Get the HTML content from the response
            html_content = response.text

            # You can now manipulate the HTML content as needed, e.g. save it to a file
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML page downloaded successfully.")
        else:
            print("Failed to download HTML page. Status code:", response.status_code)

    def getCarDataAll(self,url):

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the data
        table = soup.find("table")

        # Extract the data from the table
        data = {}
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 2:
                link = cells[0].find("a")
                brand_model = link.text.strip()
                brand = brand_model.split()[0]
                model = " ".join(brand_model.split()[1:])
                data.setdefault(brand, [])
                if brand not in data:
                    data[brand] = []
                data[brand].append({
                    "model": model,
                    "link": link["href"]
                })

        # Write the data to a JSON file
        with open("brands_modelsAll.json", "w") as f:
            json.dump(data, f, indent=4)

    def getCarData(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the data
        table = soup.find("table")

        # Extract the data from the table
        data = {}
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 2:
                link = cells[0].find("a")
                brand_model = link.text.strip()
                brand = brand_model.split()[0]
                model = " ".join(brand_model.split()[1:])
                if brand not in data:
                    data[brand] = []
                # Check if the model is similar to any existing models
                similar_model = None
                for d in data[brand]:
                    if model in d["model"] or d["model"] in model:
                        similar_model = d
                        break
                # If similar model found, update the link
                if similar_model:
                    similar_model["link"] = link["href"]
                else:
                    data[brand].append({
                        "model": model,
                        "link": link["href"]
                    })


        # Write the data to a JSON file
        with open("brands_models.json", "w") as f:
            json.dump(data, f, indent=4)

    def addImageUrl(self,data):
        # Create a new dictionary to store the updated data
        updated_data = {}
        for brand, models in data.items():
            updated_models = []
            for model in models:
                updated_model = model.copy()  # Create a copy of the model to avoid modifying the original dictionary
                updated_model["img_url"] = getCarImages(model["link"])  # Update the "img_url" attribute
                updated_models.append(updated_model)
                print(updated_model["img_url"])
            updated_data[brand] = updated_models

    def getCarImages(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all link tags with rel attribute containing "image_src"
        link_tags = soup.find_all("link", rel="image_src")

        # Extract the href attribute from each link tag to get the image link
        image_links = []
        for link_tag in link_tags:
            href = link_tag.get("href")
            return href

#######################################################################################################################



    def getCarBrandAll(self):

        brands_dict = dict()

        for i, brand in enumerate(self.data.keys()):
            brands_dict[i] = brand

        return brands_dict


    def getCarModelsByBrand(self,brand_name):

        car_data = self.data.get(brand_name)
        print(car_data)
        if car_data is None:
            print(f"No data found for brand {brand_name}")
            return {}
        models = []
        for car in car_data:
            models.append(car["model"])

        return models
    def getCarsByBrand(self,brand_name):

        car_data = self.data.get(brand_name)
        if car_data is None:
            print(f"No data found for brand {brand_name}")
            return {}

        return car_data


#######################################################################################################################

#getCarImages("https://www.auto-data.net/en/abarth-500c-1.4-t-jet-135hp-42380")
#getCarDataAll("https://api.auto-data.net/image-database")
#getCarData("https://api.auto-data.net/image-database")