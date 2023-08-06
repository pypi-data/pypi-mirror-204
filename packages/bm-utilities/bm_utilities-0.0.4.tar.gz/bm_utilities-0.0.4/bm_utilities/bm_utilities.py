import re

from shapely.geometry import Point, Polygon
import numpy as np

from tqdm import tqdm
import pandas as pd


import string

try:
    import geopandas as gpd

except ImportError:
    raise ImportError(
        "geopandas needs to be installed to use this module. Use 'pip install geopandas' to install the package. See https://deckgl.readthedocs.io/en/latest/installation.html for more details."
    )

try:
    from arcgis.gis import GIS
    from arcgis.geocoding import geocode

except ImportError:
    raise ImportError(
        "arcgis needs to be installed to use this module. Use 'pip install arcgis' to install the package. See https://deckgl.readthedocs.io/en/latest/installation.html for more details."
    )

try:
    import pyarabic.araby as araby

except ImportError:
    raise ImportError(
        "pyarabic needs to be installed to use this module. Use 'pip install pyarabic' to install the package. See https://deckgl.readthedocs.io/en/latest/installation.html for more details."
    )

class TextCleaner:
    def __init__(self, custom_stopwords=None, punctuation=None):
        self.custom_stopwords = custom_stopwords or ["رقم", "طريق", "شقة", "شقه", "القطع", "ارقام", 
                                                    "لوحة", "لوحه", "تقسيم", "ش", "فيلا", "م","مكرر", "من", 
                                                    "شارع", "متفرع","ورثه","ورثه ","ورثة ","ورثة ","ورثة", "والدها", "حسبى","nan","nan "]
        self.punctuation = punctuation or string.punctuation

    def clean_text(self, text):
        """clean data from any stopwords , punctuation and english litters
         input:
         if the input was list :
         list.apply(lambda text : clean_text(text))
         :return : clean Arabic text
         """
        text = araby.strip_tashkeel(str(text))
        text = re.sub('([@A-Za-z0-9_]+)|[^\w\s]|#|http\S+', ' ', str(text))
        text = " ".join(word for word in text.split() if word not in self.custom_stopwords)
        text = " ".join(word for word in text.split() if word not in self.punctuation)
        return text



class PolygonFinder:
    def __init__(self, polygons):
        self.polygons = polygons
        
    def get_closest_polygon(self, latitude, longitude):
        # transform latitude and longitude into a point object
        point = Point(longitude, latitude)

        # compute distances between point and all polygons
        distances = [point.distance(polygon) for polygon in self.polygons['geometry']]

        # find index of closest polygon
        index = np.argmin(distances)

        # return information about closest polygon
        closest_polygon = self.polygons.iloc[index]
        result = {
            'ADM3_PCODE': closest_polygon['ADM3_PCODE'],
            'ADM2_PCODE': closest_polygon['ADM2_PCODE'],
            'ADM1_PCODE': closest_polygon['ADM1_PCODE'],
            'geometry': closest_polygon['geometry'],
            'distance_polygon': distances[index],
            'محافظة': closest_polygon['محافظة'],
            'قسم / مركز': closest_polygon['قسم / مركز'],
            'منطقة': closest_polygon['منطقة']
        }
        return result

class get_places:
    def __init__(self, polygons):
        self.polygon_finder = PolygonFinder(polygons)
        
    def find_closest_polygon(self, latitude, longitude):
        return self.polygon_finder.get_closest_polygon(latitude, longitude)
        
    def find_closest_places(self, input_table):
        result = input_table.apply(lambda x: self.find_closest_polygon(x[0], x[1]), axis=1, result_type='expand')
        result = pd.concat([input_table, result], axis=1)
        result = result.loc[:, ~result.columns.duplicated()]
        return result


class AddressFinder:
    def __init__(self, geo_df):
      all_sub_regions = geo_df[['ADM3_AR',"ADM3_PCODE",'ADM2_AR',"ADM2_PCODE",'ADM1_AR',"ADM1_PCODE",'geometry']]
      all_sub_regions['ADM1_AR'] = all_sub_regions['ADM1_AR'].apply(lambda x : re.sub('\n','',x))
      all_sub_regions['ADM2_AR'] = all_sub_regions['ADM2_AR'].apply(lambda x : re.sub('\n','',x))
      all_sub_regions['ADM3_AR'] = all_sub_regions['ADM3_AR'].apply(lambda x : re.sub('\n','',x))
      all_sub_regions.rename(columns={
      'ADM3_AR':'منطقة',
      'ADM2_AR':'قسم / مركز',
      'ADM1_AR':'محافظة',
      },inplace=True)
      self.polygons = all_sub_regions
    
    def find_address(self,data_0_100k,k):
        portal = GIS()
        portal
        for address_1 ,idz ,_ in zip(data_0_100k["full_address"], data_0_100k["CUSTOMER_ID"],tqdm(range(len(data_0_100k)))):
            single_line_address = " مصر "+ str(address_1)
            text_clean = TextCleaner()
            single_line_address = text_clean.clean_text(single_line_address)
            geocode_results = geocode(single_line_address)
            if len(geocode_results) != 0 :
                country = geocode_results[0]["attributes"].get("Country",np.nan)

                if country == 'EGY':
                    Latitude = geocode_results[0]["location"].get("y",np.NAN)
                    Longitude =  geocode_results[0]["location"].get("x",np.NAN)
                    input_data = pd.DataFrame({"Latitude":Latitude,"Longitude":Longitude,"address":address_1,"id":idz},index=[0])
                    get_polygon = PolygonFinder(self.polygons)
                    address = get_polygon.get_closest_polygon(Latitude,Longitude)
        return address