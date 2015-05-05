from django.db import models
from django.core.urlresolvers import reverse

# these may be reused for several models
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


PENDING_REVIEW_STATUS_TYPE = 'p'
APPROVED_REVIEW_STATUS_TYPE = 'a'
REJECTED_REVIEW_STATUS_TYPE = 'r'
TESTING_REVIEW_STATUS_TYPE = 't'

REVIEW_STATUS_TYPE_CHOICES = (
    (PENDING_REVIEW_STATUS_TYPE, 'Pending'),
    (APPROVED_REVIEW_STATUS_TYPE, 'Approved'),
    (REJECTED_REVIEW_STATUS_TYPE, 'Rejected'),
    (TESTING_REVIEW_STATUS_TYPE, 'Testing Only'),
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
    
    def get_absolute_url(self):
        return reverse('trees:genus_detail_url', args=[self.slug])
    
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
    city_object_id = models.FloatField(null=True, blank=True)
    # this is a float in their shapefile
    city_tree_id = models.IntegerField(null=True, blank=True)
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
    
    # <designation>-<source_id>, e.g. "h-103" for Heritage Tree #103
    unified_identifier = models.CharField(max_length=10, unique=True)
    
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
    
    
    def save(self, *args, **kwargs):
        
        if not self.unified_identifier:
            
            print "Setting unified identifier"
            if self.city_tree_id:
                self.unified_identifier = "%s-%s" % (self.designation, str(self.city_tree_id))
            else:
                # TODO: add error-handling, or add a uuid
                print "Can't determine a unified_identifier because no id has been specified."
                return
                
        super(NotableTree, self).save(*args, **kwargs)
    
    def __unicode__(self):
        """
        Customize this, based on designation?
        """
        return "Tree %s" % str(self.unified_identifier)
    
    class Meta:
        ordering = ['unified_identifier']


class TreePhoto(models.Model):
    """
    Fan-submitted tree photos
    """
    
    # May be temporarily undefined if submitted_tree_id 
    # can not be resolved to an existing notable tree object.
    related_tree = models.ForeignKey(NotableTree, related_name="photographed_trees", null=True, blank=True, related_query_name="photographed_tree", on_delete=models.PROTECT)
    
    # information from the submitter:
    
    # this may be null for legacy submissions 
    submitted_image = models.ImageField(upload_to="submitted_photos/%Y/%m/%d", blank=True, null=True)
    # if this is an integer, assume it's a City of Portland
    # Heritage Tree.
    submitted_tree_id = models.IntegerField(null=True, blank=True)
    
    submitted_caption = models.TextField(blank=True)
    submitted_name = models.CharField(max_length=100, blank=True)
    submitted_email = models.CharField(max_length=200, blank=True)
    submitted_url = models.CharField(max_length=200, blank=True)
    submitted_date = models.DateTimeField(blank=False)
    submitted_user_agent = models.CharField(max_length=255, blank=True)
    
    # if retrievable from image, could be used to verify proxmity
    submitted_latitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    submitted_longitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    
    # moderation:
    review_status = models.CharField(max_length=10, choices=REVIEW_STATUS_TYPE_CHOICES, default=PENDING_REVIEW_STATUS_TYPE, blank=False)
    review_notes = models.TextField(blank=True)
    reviewed_date = models.DateTimeField(blank=False)
    
    # for publicly available images only:
    approved_image_filename = models.CharField(max_length=150, blank=True)
    approved_photograher_name = models.CharField(max_length=100, blank=True)
    # truncated/edited?
    approved_caption = models.TextField(blank=True)
    
    # old CouchDB uuid of photographed tree from v1.0 of the project
    legacy_uuid = models.CharField(max_length=64, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField('last modified', auto_now=True)
    
    
    def __unicode__(self):
        """
        Will this every be important? Include tree ID?
        """
        return "Tree Image #%s" % str(self.id)
    
    class Meta:
        ordering = ['created_date']


# Future Models:

# Submission model

# TreeGroup model