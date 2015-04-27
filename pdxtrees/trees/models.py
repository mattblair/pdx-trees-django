from django.db import models


# may be reused for several models
CITY_DATASOURCE_TYPE = 'c'
STATE_DATASOURCE_TYPE = 's'
EWA_DATASOURCE_TYPE = 'e'
FAN_DATASOURCE_TYPE = 'f'
UNDEFINED_DATASOURCE_TYPE = 'u'

TREE_DATASOURCE_TYPE_CHOICES = (
    (CITY_DATASOURCE_TYPE, 'City of Portland'),
    (STATE_DATASOURCE_TYPE, 'State of Oregon'),
    (EWA_DATASOURCE_TYPE, 'Elsewise'),
    (FAN_DATASOURCE_TYPE, 'Fan'),
    (UNDEFINED_DATASOURCE_TYPE, 'Undefined or Other'),
)


class TreeGenus(models.Model):
    """
    Inferred where possible from scientific name on import
    """
    genus_name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    notes = models.TextField(blank=True)
    display_in_menu = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.genus_name
    
    class Meta:
        ordering = ['genus_name'] # or display_order
        verbose_name_plural = "Genera"


class NotableTree(models.Model):
    """
    Could be a heritage tree, a tree of merit, or some other significant tree.
    """
    
    
    """
    Fields from the city
    """
    # what is this? Just the primary key from their data?
    city_object_id = models.FloatField(null=True)
    # this is a float in their shapefile
    city_tree_id = models.IntegerField(null=True)
    # status in the city is always "Heritage" as of April 2015
    city_status = models.CharField(max_length=20, default="None")
    scientific_name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    state_id = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    height = models.IntegerField(null=True, blank=True)
    spread = models.IntegerField(null=True, blank=True)
    circumference = models.FloatField(null=True, blank=True)
    diameter = models.FloatField(null=True, blank=True)
    year_designated = models.IntegerField(null=True, blank=True)
    owner = models.CharField(max_length=255, blank=True)
    # notes is truncated to 254 in city data in 8+ records
    city_notes = models.TextField(blank=True)
    latitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    
    """
    Additional fields:
    """
    
    genus = models.ForeignKey(TreeGenus, related_name="trees", related_query_name="tree", null=True, blank=True, on_delete=models.SET_NULL)
    
    HERITAGE_TREE_DESIGNATION_TYPE = 'h'
    TREE_OF_MERIT_DESIGNATION_TYPE = 'm'
    SIGNIFICANT_TREE_DESIGNATION_TYPE = 's'
    UNDEFINED_DESIGNATION_TYPE = 'u'

    DESIGNATION_TYPE_CHOICES = (
        (HERITAGE_TREE_DESIGNATION_TYPE, 'Heritage Tree'),
        (TREE_OF_MERIT_DESIGNATION_TYPE, 'Tree of Merit'),
        (SIGNIFICANT_TREE_DESIGNATION_TYPE, 'Significant'),
        (UNDEFINED_DESIGNATION_TYPE, 'Undefined'),
    )
    
    
    designation = models.CharField(max_length=1, choices=DESIGNATION_TYPE_CHOICES, default=UNDEFINED_DESIGNATION_TYPE)
    initial_datasource = models.CharField(max_length=1, choices=TREE_DATASOURCE_TYPE_CHOICES, default=UNDEFINED_DATASOURCE_TYPE) 
    
    
    # client apps would map these keys to filenames with a dictionary, etc.
    HERITAGE_TREE_ICON_TYPE = 'h'
    GHOST_TREE_ICON_TYPE = 'g'
    NO_ACCESS_TREE_ICON_TYPE = 'n'
    OTHER_TREE_ICON_TYPE = 'z'

    ICON_TYPE_CHOICES = (
        (HERITAGE_TREE_ICON_TYPE, 'Heritage Tree Icon'),
        (GHOST_TREE_ICON_TYPE, 'Ghost Tree Icon'),
        (NO_ACCESS_TREE_ICON_TYPE, 'No Access Icon'),
        (OTHER_TREE_ICON_TYPE, 'Other Tree Icon'),
    )
    
    display_icon = models.CharField(max_length=1, choices=ICON_TYPE_CHOICES, default=OTHER_TREE_ICON_TYPE)
    
    # for trees that have been cut down or removed, aka 'ghost' trees
    deceased = models.BooleanField(default=False)
    year_deceased = models.IntegerField(null=True, blank=True)
    cause_of_death = models.CharField(max_length=255, blank=True)
    
    internal_notes = models.TextField(blank=True)
    
    # old CouchDB uuid from v1.0 of the project
    legacy_uuid = models.CharField(max_length=64, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField('last modified', auto_now=True)
    
    
    def __unicode__(self):
        """
        NOTE: city_tree_id will not be a good representation field if the
        project expands beyond official heritage trees.
        """
        return "Tree #%s" % str(self.city_tree_id)
    
    class Meta:
        ordering = ['city_tree_id']


# Future Models:

# TreePhoto model (adapt from 1.0)

# Submission model

# TreeGroup model