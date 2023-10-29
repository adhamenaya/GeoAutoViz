import libpysal
import momepy
import pandas as pd
from shapely import Polygon

from GeoAutoViz.GeoUtils import GeoUtils
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


class POIsAnalyzer:
    def __init__(self, extractor):
        super().__init__()
        self.model = None
        self.percentiles_joined = None
        self.weights = None
        self.buildings = None
        self.tessellation = None
        self.public_service = None
        self.leisure = None
        self.residential = None
        self.green_spaces = None
        self.commercial = None
        self.sustenance = None
        self.business = None
        self.poi_extractor = extractor
        self.lst_classes = None
        self.classified_buildings = None
        self.buildings_tessellation = None

    def get_building(self, polygon):
        print("get_building...")

        list_polygons = []
        if GeoUtils.is_geo_multipolygon(polygon):
            list_polygons.extend(GeoUtils.convert_multipolygon_to_list_of_polygons(polygon))
        elif GeoUtils.is_geo_polygon(polygon):
            list_polygons = [Polygon(polygon)]

        for p in list_polygons:
            plgn = Polygon(p.exterior.coords)
            if self.buildings is None:
                self.buildings = self.poi_extractor.get_buildings(plgn)
            else:
                self.buildings = self.buildings.append(self.poi_extractor.get_buildings(plgn))

        return self.buildings

    def get_classified_building(self, polygon):
        print("get_classified_building...")
        self.business = self.poi_extractor.get_business(polygon)
        self.sustenance = self.poi_extractor.get_sustenance(polygon)
        self.commercial = self.poi_extractor.get_commercial(polygon)
        #self.green_spaces = self.poi_extractor.get_green_spaces(polygon)
        self.residential = self.poi_extractor.get_residential(polygon)
        self.leisure = self.poi_extractor.get_leisure(polygon)
        self.public_service = self.poi_extractor.get_public_service(polygon)
        self.lst_classes = [self.business, self.sustenance, self.commercial,
                            self.residential, self.leisure, self.public_service]

    def get_class(self, osmid):
        for cate in self.lst_classes:
            cate["osmid"] = self.get_single_index_value(cate.index)
            osmids = self.get_single_index_value(cate.index)
            if osmid in osmids:
                return cate[cate['osmid'] == osmid].iloc[0]["class"]
        return -1

    def get_single_index_value(self, index):
        return [t[1] for t in index]

    def setup_buildings(self):
        print("setup_buildings...")
        self.buildings["osmid"] = [t[1] for t in self.buildings.index]
        self.buildings = self.buildings[self.buildings.geom_type == "Polygon"].reset_index(drop=True)

        self.classified_buildings = self.buildings[["geometry"]].to_crs(5514)
        self.classified_buildings["osmid"] = self.buildings["osmid"].values
        self.classified_buildings["business"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.business.index)).astype(int))
        self.classified_buildings["sustenance"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.sustenance.index)).astype(int))
        self.classified_buildings["commercial"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.commercial.index)).astype(int))
        #self.classified_buildings["green_spaces"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.green_spaces.index)).astype(int))
        self.classified_buildings["residential"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.residential.index)).astype(int))
        self.classified_buildings["leisure"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.leisure.index)).astype(int))
        self.classified_buildings["public_service"] = (self.classified_buildings["osmid"].isin(self.get_single_index_value(self.public_service.index)).astype(int))

    def setup_spatial_unit(self):
        print("setup_spatial_unit...")
        limit = momepy.buffered_limit(self.classified_buildings, 2)
        tess = momepy.Tessellation(self.classified_buildings, "osmid", limit, verbose=False, segment=1)
        self.tessellation = tess.tessellation

    def set_neighbours(self):
        print("set_neighbours...")
        self.weights = libpysal.weights.contiguity.Queen.from_dataframe(self.tessellation, ids="osmid",
                                                                        silence_warnings=True)
        self.tessellation["neighbors"] = momepy.Neighbors(self.tessellation, self.weights, "osmid", weighted=False,
                                                          verbose=False).series
        self.buildings_tessellation = self.tessellation.merge(self.classified_buildings.drop(columns=['geometry']),
                                                              on='osmid')

    def calculate_spatial_distribution_of_classes(self):
        print("calculate_spatial_distribution_of_classes...")
        queen_1 = momepy.sw_high(k=1, weights=self.weights)
        percentiles = []
        for column in self.buildings_tessellation.columns.drop(["osmid", 'neighbors', "geometry"]):
            perc = momepy.Percentiles(self.buildings_tessellation, column, queen_1, "osmid", verbose=False,
                                      interpolation='higher').frame
            perc.columns = [f"{column}_" + str(x) for x in perc.columns]
            percentiles.append(perc)

        self.percentiles_joined = pd.concat(percentiles, axis=1)
        self.percentiles_joined['neighbors'] = self.buildings_tessellation["neighbors"].values
        self.percentiles_joined['osmid'] = self.buildings_tessellation["osmid"].values
        self.percentiles_joined['class'] = self.buildings_tessellation.apply(lambda row: self.get_class(row["osmid"]),
                                                                             axis=1)

    def classify_poi(self):
        print("classify_poi...")
        self.percentiles_joined_with_classes = self.percentiles_joined[self.percentiles_joined['class'] != -1]

        # Split the data into training and testing sets
        X = self.percentiles_joined_with_classes[self.percentiles_joined_with_classes.columns[0:-2]]
        y = self.percentiles_joined_with_classes['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train a decision tree classifier
        classifier = DecisionTreeClassifier()
        self.model = classifier.fit(X_train, y_train)

        # Make predictions on the test data
        y_pred = classifier.predict(X_test)

        # Evaluate the classifier's performance
        accuracy = accuracy_score(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print(f"Accuracy: {accuracy}")
        print(f"Confusion: {confusion}")
        print(f"Report: {report}")
        return accuracy

    def predict_missing_poi_class(self):
        print("predict_missing_poi_class...")
        # Split the data into training and testing sets
        self.percentiles_joined_without_classes = self.percentiles_joined[self.percentiles_joined['class'] == -1]
        X2 = self.percentiles_joined_without_classes[self.percentiles_joined_without_classes.columns[0:-2]]
        predictions = self.model.predict(X2)
        self.percentiles_joined_without_classes['pred'] = predictions
        return self.percentiles_joined_without_classes

    def save(self, id, accuracy):
        poi_classes_pred = {"osmid": self.percentiles_joined_without_classes["osmid"].values,
                            "class": self.percentiles_joined_without_classes['pred'].values,
                            "pred": 1}

        poi_classes_origin = {"osmid": self.percentiles_joined_with_classes["osmid"].values,
                              "class": self.percentiles_joined_with_classes['class'].values,
                              "pred": 0}
        df1 = pd.DataFrame(poi_classes_origin)
        df2 = pd.DataFrame(poi_classes_pred)

        df_final = pd.concat([df1, df2])

        df_final = pd.merge(self.buildings[['osmid','geometry']], df_final, on='osmid', how='inner')
        df_final.to_csv("data/generated/"+id+"_classes_"+str(accuracy)+".csv")
