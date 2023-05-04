import requests
import json
import concurrent.futures
from PyQt5.QtGui import QPixmap
from bs4 import BeautifulSoup
import re
class scrap:
    def __init__(self):
        with open('./Scraping/brands_modelsAll.json') as f:
            self.data = json.load(f)

    def downloadScript(self,url):
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
                updated_model["img_url"] = self.getCarImages(model["link"])  # Update the "img_url" attribute
                updated_models.append(updated_model)
                print(updated_model["img_url"])
            updated_data[brand] = updated_models

    def getModelImage(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all link tags with rel attribute containing "image_src"
        link_tags = soup.find_all("link", rel="image_src")

        # Extract the href attribute from each link tag to get the image link
        image_links = []
        for link_tag in link_tags:
            href = link_tag.get("href")
            return href


    def get_image_from_url(self,url):
        try:
            response = requests.get(url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            return pixmap
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None


    def getCarUrlImages(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        img_src_list = []
        scripts = soup.find_all('script')

        # regular expression pattern to match the contents of the `bigs` array
        pattern = r'bigs\[\d+\] = "([\w\/\.-]+)";'

        # extract the `bigs` data using `re.findall()`
        matches = re.findall(pattern, str(scripts))
        # add prefix to each item in the list using a list comprehension
        bigs_data = ['https://www.auto-data.net/images/' + item for item in matches]

        # print the `bigs` data
        return bigs_data

    def download_images(self,image_urls):
        total_images = len(image_urls)
        current_image = 0
        images = []
        while current_image < total_images:
            print(f"Downloading image {current_image + 1}/{total_images}...")
            url = image_urls[current_image]
            print(url)
            url = self.getModelImage(url)
            pixmap = self.get_image_from_url(url)
            if pixmap is not None:
                images.append(pixmap)
                current_image += 1

        print("All images downloaded!")
        return images
    def download_img(self,url):
        url = self.getModelImage(url)
        pixmap = self.get_image_from_url(url)
        return pixmap




    #######################################################################################################################



    def getCarBrandAll(self):

        brands_dict = dict()

        for i, brand in enumerate(self.data.keys()):
            brands_dict[i] = brand

        return brands_dict

    def getCarModelsByBrand(self, brand_name):
        car_data = self.data.get(brand_name)
        if car_data is None:
            print(f"No data found for brand {brand_name}")
            return {}

        models = {}
        for i, car in enumerate(car_data):
            models[i + 1] = car["model"]

        return models

    def getCarsByBrand(self,brand_name):

        car_data = self.data.get(brand_name)
        if car_data is None:
            print(f"No data found for brand {brand_name}")
            return []

        return car_data

    def getCarByModel(self, brand, model):
        car_data = self.data.get(brand)
        if car_data is None:
            print(f"No data found for brand {brand}")
            return []
        matching_cars = []
        for car in car_data:
            if car["model"] == model:
                matching_cars.append(car)
        return matching_cars

    def get(self):
        data = json.loads(self.data)
        for brand in data.values():
            for item in brand:
                for value in item.values():
                    if isinstance(value, list):
                        for image in value:
                            print(image)
                    elif isinstance(value, dict):
                        for detail in value.values():
                            print(detail)
                    else:
                        print(value)

#######################################################################################################################

#getCarImages("https://www.auto-data.net/en/abarth-500c-1.4-t-jet-135hp-42380")
#getCarDataAll("https://api.auto-data.net/image-database")
#getCarData("https://api.auto-data.net/image-database")