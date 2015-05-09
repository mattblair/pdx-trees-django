import os
import json
import csv # for photo import

from django.db import transaction
from django.core.exceptions import ValidationError


from models import NotableTree, TreeGenus, CITY_DATASOURCE_TYPE, TreePhoto


# to serialize from a queryset:
#from django.core import serializers


# keys are properties in the GeoJSON file
# values are properties of target object
heritagetree_mapping = {
    'OBJECTID' : 'city_object_id',
    'TREEID' : 'city_tree_id',
    'STATUS' : 'city_status',
    'SCIENTIFIC' : 'scientific_name',
    'COMMON_NAM' : 'common_name',
    'STATEID' : 'state_id',
    'ADDRESS' : 'address',
    'HEIGHT' : 'height',
    'SPREAD' : 'spread',
    'CIRCUMFERE' : 'circumference',
    'DIAMETER' : 'diameter',
    'YEAR' : 'year_designated',
    'OWNER' : 'owner',
    'NOTES' : 'city_notes'
}


def load_initial_data():
    """
    A one-off load of GeoJSON file containing heritage trees.
    
    Converted using this command:
    
    ogr2ogr -f GeoJSON -t_srs crs:84 ./<reprojected-data>.geojson ./<original-data>.shp
    
    For more information:
    http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/
    
    use trial_run argument to rollback?
    """
    
    geojson_filename = "pdx-heritage-trees-150419.geojson"
    
    # relative dir is: ../../data
    # must be a better way to do this than triple-nesting dirname calls?
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print project_root
    
    tree_geojson_path = os.path.join(project_root, 'data', geojson_filename)
    print tree_geojson_path
    
    with open(tree_geojson_path, 'r') as infile:
        geojson_data = json.load(infile)
    
    # open json, iterate the list in the features key
    if geojson_data['type'] == 'FeatureCollection':
        
        geojson_features = geojson_data['features']
        
        # length check on features?
        
        for feature in geojson_features:
            
            nt = NotableTree()
            
            # set properties
            nt.city_object_id = feature["properties"]["OBJECTID"]
            nt.city_tree_id = int(feature["properties"]["TREEID"])
            nt.city_status = feature["properties"]["STATUS"]
            # TODO: apply mappings for misspellings?
            nt.scientific_name = feature["properties"]["SCIENTIFIC"]
            nt.common_name = feature["properties"]["COMMON_NAM"]
            si = feature["properties"]["STATEID"]
            if si:
                nt.state_id = si
            ca = feature["properties"]["ADDRESS"]
            if ca:
                nt.address = ca
            nt.height = feature["properties"]["HEIGHT"]
            nt.spread = feature["properties"]["SPREAD"]
            nt.circumference = feature["properties"]["CIRCUMFERE"]
            nt.diameter = feature["properties"]["DIAMETER"]
            nt.year_designated = feature["properties"]["YEAR"]
            nt.owner = feature["properties"]["OWNER"]
            cn = feature["properties"]["NOTES"]
            if cn:
                nt.city_notes = cn
            
            # set latitude and longitude
            nt.longitude = feature["geometry"]["coordinates"][0]
            nt.latitude = feature["geometry"]["coordinates"][1]
            
            # TODO: create or match genus!
            gn = nt.scientific_name.split(' ')[0]
            
            g = TreeGenus.objects.filter(genus_name=gn)
            
            if not g:
                print "Making genus with name %s" % gn
                
                g = TreeGenus()
                g.genus_name = gn
                g.slug = gn.lower()
                g.save()
                
                nt.genus = g
                
            else:
                nt.genus = g[0]
                
            
            # override defaults
            nt.designation = NotableTree.HERITAGE_TREE_DESIGNATION_TYPE
            nt.initial_datasource = CITY_DATASOURCE_TYPE
            nt.display_icon = NotableTree.HERITAGE_TREE_ICON_TYPE
            
            nt.save()
            
    else:
        print "Unexpected GeoJSON type: %s" % geojson_data['type']


@transaction.atomic
def populate_ghost_trees():
    """
    Create placeholder records for all missing heritage trees.
    
    First pass: populate with details from 2010, where available.
    Second pass: just create dummy records for those which remain.
    Note: This will only be used via the shell after initial population 
    of the database.
    """
    
    missing_in_2015 = [13, 28, 29, 42, 50, 59, 65, 72, 92, 93, 94, 95, 96, 99, 114, 118, 123, 131, 138, 142, 166, 215, 227, 228, 230, 232, 234, 267]
    
    original_json_filename = "heritage-tree-details-100917-pp.json"
    
    # relative dir is: ../../data
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    old_json_path = os.path.join(project_root, 'data', original_json_filename)
    
    with open(old_json_path, 'r') as infile:
        data_from_2010 = json.load(infile)
    
    for tree in data_from_2010:
        
        # see if the city id is in the missing list and not db
        missing_id = int(tree["treeid"])
        mt = NotableTree.objects.filter(city_tree_id=missing_id)
        
        if missing_id in missing_in_2015 and len(mt) == 0:
            
            print "Making ghost record for %s based on 2010 data." % tree["treeid"]
            
            nt = NotableTree()
            
            nt.city_object_id = tree["objectid"]
            nt.city_tree_id = int(tree["treeid"])
            nt.city_status = tree["status"]
            nt.scientific_name = tree["scientific"]
            nt.common_name = tree["common_nam"]
            
            si = tree["stateid"]
            if si:
                nt.state_id = si
            else:
                nt.state_id = "Unknown"
                
            ca = tree["address"]
            if ca:
                nt.address = ca
            else:
                nt.address = "Unknown"
                
            nt.height = tree["height"]
            nt.spread = tree["spread"]
            nt.circumference = tree["circumfere"]
            nt.diameter = tree["diameter"]
            nt.year_designated = tree["year"]
            
            own = tree["owner"]
            if own:
                nt.owner = own
            else:
                nt.owner = "Unknown"
            
            cn = tree["notes"]
            if cn:
                nt.city_notes = cn
            
            nt.longitude = tree["geometry"]["coordinates"][0]
            nt.latitude = tree["geometry"]["coordinates"][1]
            
            gn = nt.scientific_name.split(' ')[0]
            
            g = TreeGenus.objects.filter(genus_name=gn)
            
            if not g:
                print "Making genus with name %s" % gn
                
                g = TreeGenus()
                g.genus_name = gn
                g.slug = gn.lower()
                g.save()
                
                nt.genus = g
                
            else:
                nt.genus = g[0]
                
            
            # override defaults
            nt.designation = NotableTree.HERITAGE_TREE_DESIGNATION_TYPE
            nt.initial_datasource = CITY_DATASOURCE_TYPE
            
            # specific to ghost tree status:
            nt.display_icon = NotableTree.GHOST_TREE_ICON_TYPE
            nt.deceased = True
            
            """
            try:
                nt.full_clean()
            except ValidationError as e:
                print e
            """
            nt.save()
    
    # re-iterate the ghost tree list, create dummy records for any 
    # which still aren't found.
    # Max photo from v1.0 is for tree with id #297
    
    print "Starting second pass..."
    
    for tid in missing_in_2015:
        
        mt = NotableTree.objects.filter(city_tree_id=tid)
        
        if len(mt) > 0:
            print "Missing Tree %s Already Created" % str(tid)
        else: 
            print "Creating Placeholder for Missing Heritage Tree %s" % str(tid)
            
            # if not found, post a dummy record
            nt = NotableTree()
            
            nt.city_tree_id = tid
            nt.city_status = "Unknown"
            nt.scientific_name = "Unknown"
            nt.common_name = "Unknown"
            nt.state_id = "Unknown"
            nt.address = "Unknown"
            nt.owner = "Unknown"
            nt.latitude = 0.0
            nt.longitude = 0.0
            nt.designation = NotableTree.HERITAGE_TREE_DESIGNATION_TYPE
            
            # create a dummy genus? Probably not.
            
            # specific to ghost tree status:
            nt.display_icon = NotableTree.GHOST_TREE_ICON_TYPE
            nt.deceased = True
            nt.internal_notes = "This number was skipped in the city's heritage tree listings. No further information is available."
            
            nt.save()


@transaction.atomic
def import_v1_photos():
    """
    This method is a one-time import of photos from v1.0.
    
    NOTE: Do NOT commit photo data to git. It contains private info,
    such as email addresses.
    """
    
    photo_data_filename = "pdx-trees-photos-moderated-150504.csv"
    private_data_dir = "/Users/matt/Dropbox/appWorkingNotes/pdxTrees/privateData"
    photo_data_path = os.path.join(private_data_dir, photo_data_filename)
    
    photo_data_v1 = csv.DictReader(open(photo_data_path, 'rb'),delimiter=",")
    
    for p in photo_data_v1:
        
        #print "Photo id: %s of tree %s is %s" % (p["id"], p["related_tree_id"], p["review_status"])
        
        # find related tree based on city id
        try:
            rt = NotableTree.objects.get(city_tree_id=int(p["related_tree_id"]))
        except DoesNotExist:
            # if it can't find an existing tree, log an error and continue
            print "WARNING: Could not find matching tree!"
            continue
        
        tp = TreePhoto()
        
        tp.related_tree = rt
        tp.submitted_tree_id = p["related_tree_id"]
        
        # these can all be blank
        tp.submitted_caption = p["caption"]
        tp.submitted_name = p["submitter_name"]
        tp.submitted_email = p["submitter_email"]
        #tp.submitted_url -- always blank in the source data
        tp.submitted_user_agent = p["submitter_user_agent"]
        
        # this is required:
        tp.submitted_date = p["date_taken"]
        
        # read from the image file? Maybe later.
        tp.submitted_latitude = 0.0
        tp.submitted_longitude = 0.0
        
        # extract photo name by removing prefix: photologue/photos/
        photo_file = p["image"].replace('photologue/photos/','')
        original_review_status = p["review_status"]
        
        # map review_status values:
        # original: pending, approved, flagged, banned, testing
        # new: p, a, r, t
        
        status_mapping = {
            "pending" : "p",
            "approved" : "a",
            "flagged" : "r",
            "banned" : "r",
            "testing" : "t"
        }
        
        tp.review_status = status_mapping[original_review_status]
        
        # special handling for flagged/banned photos:
        # put photo name in review notes, not in approved field
        if p["review_status"] in ["flagged", "banned"]:
            tp.review_notes = "Photo (%s) was %s" % (photo_file, p["review_status"])
        
        # required -- but v1.0 of the site did not log review dates
        tp.reviewed_date = p["date_taken"]
        
        # copy data to public fields, if approved or for testing
        if tp.review_status in ["a", "t"]:
            tp.approved_image_filename = photo_file
            tp.approved_submitter_name = p["submitter_name"]
            tp.approved_caption = p["caption"]
        
        tp.legacy_uuid = p["related_tree_couch_id"]
        
        tp.save()


def diff_with_geojson(geojson_path, persist_data=False):
    """
    Reads the geojson file (after conversion from shapefile)
    Iterates each feature:
        * if TREE_ID matches city_tree_id in the database, field-level diff
        * else suggest appending it
        
    default persist_data argument can be used to log results without saving.
    """
    print "Not Implemented Yet"
    
    return None


def update_public_photo_count_for_tree(tree_to_update):
    """
    Call directly from save when a tree photo's review_status = approved.
    """
    
    if tree_to_update:
        
        approved = tree_to_update.photographed_trees.filter(review_status='a')
        tree_to_update.public_photo_count = len(approved)
        tree_to_update.save()


def update_public_photo_counts(trees):
    """
    Iterate a queryset or list of trees, reset public photo count for each.
    
    Photo counts could also be pulled in real-time with:

    from django.db.models import Count

    photo_counts = NotableTree.objects.annotate(photo_count=Count('photographed_tree')).order_by('photo_count')
    
    And then filtering as needed.
    """
    
    for t in trees:
        update_public_photo_count_for_tree(t)


def trees_as_geojson(trees):
    """
    Iterate though the trees, possibly with a filtering criteria,
    and return a GeoJSON Feature Collection
    """
    # or accept a subset iterable as an argument
    #trees = NotableTree.objects.all()
    
    tree_list = []
    
    for t in trees:

        # could add a geojson_representation to Tree class, rather than here

        tree_properties_dict = {}
        tree_geojson_dict = {}

        geometry_dict = {}

        tree_properties_dict['title'] = "%s: %s" % (t.city_tree_id, t.common_name)
        tree_properties_dict['subtitle'] = t.scientific_name
        if t.genus:
            tree_properties_dict['genus'] = t.genus.genus_name

        # structure it as GeoJSON
        geometry_dict['type'] = "Point"
        geometry_dict['coordinates'] = [float(t.longitude), float(t.latitude)]

        tree_geojson_dict['geometry'] = geometry_dict
        tree_geojson_dict['type'] = "Feature"
        tree_geojson_dict['properties'] = tree_properties_dict

        # make the id a peer of properties, in accordance with GeoJSON
        # TODO: make a decision about the most appropriate id?
        # city_tree_id, or the internal id for this project.
        tree_geojson_dict['id'] = t.id

        # shouldn't need this:
        """
        if t.longitude is None or t.latitude is None:
            print "Coordinates not defined: %s" % t.title
        else:
            tree_list.append(tree_geojson_dict)
        """

        tree_list.append(tree_geojson_dict)

    trees_geojson = {}
    trees_geojson['type'] = "FeatureCollection"
    trees_geojson['features'] = tree_list

    # to serialize from a queryset:
    #return serializers.serialize("json", trees_geojson)

    # but since we've restructured it here, just convert the dict
    return json.dumps(trees_geojson)
    