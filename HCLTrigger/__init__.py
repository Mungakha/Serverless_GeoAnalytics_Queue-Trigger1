import logging
import json
import os
import azure.functions as func
from arcgis.features.manage_data import dissolve_boundaries
from arcgis.features.find_locations import find_centroids
from arcgis.geometry import from_geo_coordinate_string
from arcgis.geocoding import geocode
from arcgis.geometry import lengths, areas_and_lengths, project
from arcgis.geometry import Point, Polyline, Polygon, Geometry
from arcgis.gis import GIS
import arcgis
from arcgis import geometry 
from arcgis import features
from arcgis.geoanalytics import manage_data
from arcgis.features.manage_data import overlay_layers
from arcgis.features import GeoAccessor, GeoSeriesAccessor, FeatureLayer
from arcgis.features import FeatureLayerCollection
import pandas


def main(msg: func.QueueMessage, msg1: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    
    test = os.environ["testers"]#Read Key Vault Credentials Integrated in Function
    gis = GIS("https://yyyy.maps.arcgis.com", "UserName", test)#Log into ESRI Portal with the password read above
    
    #Search and if feature services named "findcentroids" and "HealthLyrPolygonToPoint" delete. If not there proceed
    try:
        gis.content.search("findcentroids")[0].delete()
        gis.content.search("HealthLyrPolygonToPoint")[0].delete()
    except:
        pass

    item=gis.content.get('asset 1 FeatureServiceID')#Find asset1 feature service using the given feature service ID
    l=item.layers[0]#Create a layer
    dissolve_fields=['Name','Operation_Code']#List of Fields to dissolve on
    try:
        g=dissolve_boundaries(l, dissolve_fields,output_name='findcentroids')#Dissolve defined layer on fields listed above and publish on portal
        c= gis.content.get(g.id).layers[0]#Create Layer for feature published above
    except:
        pass
    try:
        pp= find_centroids(c, output_name="HealthLyrPolygonToPoint")#Create Centroids from the feature layer and publish on the ESRI portal
        
        msg1.set(msg.get_body().decode('utf-8'))
    except:
        pass
    