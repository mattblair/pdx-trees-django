from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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


DRAFT_REVIEW_STATUS_TYPE = 'd'
PENDING_REVIEW_STATUS_TYPE = 'p'
APPROVED_REVIEW_STATUS_TYPE = 'a'
REJECTED_REVIEW_STATUS_TYPE = 'r'
TESTING_REVIEW_STATUS_TYPE = 't'

REVIEW_STATUS_TYPE_CHOICES = (
    (DRAFT_REVIEW_STATUS_TYPE, 'Draft'),
    (PENDING_REVIEW_STATUS_TYPE, 'Pending'),
    (APPROVED_REVIEW_STATUS_TYPE, 'Approved'),
    (REJECTED_REVIEW_STATUS_TYPE, 'Rejected'),
    (TESTING_REVIEW_STATUS_TYPE, 'Testing Only'),
)


CC_BY_SA_LICENSE = 'CC BY-SA' # the default
CC_BY_LICENSE = 'CC BY'
CC_BY_NC_SA_LICENSE = 'CC BY-NC-SA'
PUBLIC_DOMAIN_LICENSE = 'Public Domain'
UNKNOWN_LICENSE = 'Unknown'

LICENSE_CHOICES = (
    (CC_BY_SA_LICENSE, 'CC Attribution-ShareAlike'),
    (CC_BY_LICENSE, 'CC Attribution'),
    (CC_BY_NC_SA_LICENSE, 'CC Attribution-NonCommercial-ShareAlike'),
    (PUBLIC_DOMAIN_LICENSE, 'Public Domain'),
    (UNKNOWN_LICENSE, 'Unknown'),
)


PDF_ATTACHMENT_TYPE = 'pdf'
JSON_ATTACHMENT_TYPE = 'json'
ZIP_ATTACHMENT_TYPE = 'zip'
NONE_ATTACHMENT_TYPE = 'none'

ATTACHMENT_TYPE_CHOICES = (
    (PDF_ATTACHMENT_TYPE, 'PDF'),
    (JSON_ATTACHMENT_TYPE, 'JSON'),
    (ZIP_ATTACHMENT_TYPE, 'Zip File'),
    (NONE_ATTACHMENT_TYPE, 'None')
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
    public_photo_count = models.IntegerField(default=0)
    
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
    
    def get_absolute_url(self):
        # TODO: Adapt to non-heritage trees
        return reverse('trees:tree_detail_url', args=[self.city_tree_id])
    
    class Meta:
        ordering = ['unified_identifier']
    
    def public_photos(self):
        return self.photographed_trees.filter(review_status=APPROVED_REVIEW_STATUS_TYPE)


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
    approved_submitter_name = models.CharField(max_length=100, blank=True)
    # truncated/edited?
    approved_caption = models.TextField(blank=True)
    display_order = models.IntegerField(help_text="Higher values will be displayed first.",default=50)
    
    # old CouchDB uuid of photographed tree from v1.0 of the project
    legacy_uuid = models.CharField(max_length=64, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField('last modified', auto_now=True)
    
    
    def save(self, *args, **kwargs):
        
        super(TreePhoto, self).save(*args, **kwargs)
        
        # run this *after* saving:
        from trees.utilities import update_public_photo_count_for_tree
        update_public_photo_count_for_tree(self.related_tree)
    
    
    def __unicode__(self):
        """
        Will this every be important? Include tree ID?
        """
        return "Tree Image #%s" % str(self.id)
    
    class Meta:
        ordering = ['-display_order','submitted_date']


class PhotoFlag(models.Model):
    """
    Allow anonymous viewers to flag photos.
    
    Since these photos are moderated, this will probably be
    photos of the wrong tree, or confusing comment, etc.
    """

    UNDEFINED_PHOTO_FLAG_TYPE = 0
    BAD_TREE_PHOTO_FLAG_TYPE = 1
    BAD_COMMENT_PHOTO_FLAG_TYPE = 2

    PHOTO_FLAG_TYPE_CHOICES = (
        (UNDEFINED_PHOTO_FLAG_TYPE, 'Other'),
        (BAD_TREE_PHOTO_FLAG_TYPE, 'Incorrect Tree'),
        (BAD_COMMENT_PHOTO_FLAG_TYPE, 'Incorrect Comment'),
    )


    PENDING_FLAG_STATUS = 'p'
    CONFIRMED_FLAG_STATUS = 'c'
    REJECTED_FLAG_STATUS = 'r'

    PHOTO_FLAG_STATUS_CHOICES = (
        (PENDING_FLAG_STATUS, 'Pending'),
        (CONFIRMED_FLAG_STATUS, 'Confirmed'),
        (REJECTED_FLAG_STATUS, 'Rejected'),
    )


    flagged_photo = models.ForeignKey(TreePhoto, related_name="flagged_photos", related_query_name="flagged_photo", on_delete=models.PROTECT)
    flag_type = models.IntegerField(choices=PHOTO_FLAG_TYPE_CHOICES, default=UNDEFINED_PHOTO_FLAG_TYPE)
    complaint = models.TextField(blank=False)
    flag_date = models.DateTimeField(auto_now_add=True)

    reviewed = models.BooleanField(default=False)
    review_date = models.DateTimeField(blank=True, null=True)
    review_action = models.CharField(max_length=1, choices=PHOTO_FLAG_STATUS_CHOICES, default=PENDING_FLAG_STATUS)
    review_notes = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.flag_date)

    class Meta:
        ordering = ['flag_date']
        verbose_name_plural = "submitted Photo Flags"


class SupplementalContent(models.Model):
    """
    Could be added to a tree, genus, or group.
    """
    
    
    SUPPLEMENTAL_TEXT_LAYOUT = 'T'
    SUPPLEMENTAL_IMAGE_LAYOUT = 'I'
    SUPPLEMENTAL_SOUND_LAYOUT = 'S'
    SUPPLEMENTAL_DOCUMENT_LAYOUT = 'D'
    SUPPLEMENTAL_UNKNOWN_LAYOUT = 'U'
    
    SUPPLEMENTAL_LAYOUT_CHOICES = (
        (SUPPLEMENTAL_TEXT_LAYOUT, 'Text'),
        (SUPPLEMENTAL_IMAGE_LAYOUT, 'Image'),
        (SUPPLEMENTAL_SOUND_LAYOUT, 'Sound'),
        (SUPPLEMENTAL_DOCUMENT_LAYOUT, 'Document'),
        (SUPPLEMENTAL_UNKNOWN_LAYOUT, 'Unknown')
    )
    
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    display_order = models.IntegerField(default=50)
    
    summary = models.CharField(max_length=255, blank=True, help_text="Used for previews, list presentations, etc.")
    article_text = models.TextField(blank=True)
    
    credit = models.CharField(max_length=255, blank=True)
    license = models.CharField(max_length=20,
                               choices=LICENSE_CHOICES,
                               default=CC_BY_SA_LICENSE)
    
    copyright_notice = models.CharField(max_length=255, blank=True)
    copyright_notes = models.TextField(blank=True, help_text="Not visible to the public at any time.")
    
    
    editorial_notes = models.TextField(blank=True, help_text="Not visible to the public at any time.")

    workflow_status = models.CharField(max_length=20, choices=REVIEW_STATUS_TYPE_CHOICES, default=DRAFT_REVIEW_STATUS_TYPE)
    
    # mainly determined by media to present
    layout = models.CharField(max_length=1, 
                              choices=SUPPLEMENTAL_LAYOUT_CHOICES,
                              default=SUPPLEMENTAL_TEXT_LAYOUT)
    
    
    photo = models.ImageField(upload_to="supplemental_photos", blank=True, null=True)
    photo_title = models.CharField(max_length=100, blank=True)
    photo_caption = models.CharField(max_length=255, blank=True)
    photo_credit = models.CharField(max_length=255, blank=True)
    photo_copyright = models.CharField(max_length=255, blank=True)
    
    photo_license = models.CharField(max_length=20,
                                     choices=LICENSE_CHOICES,
                                     default=CC_BY_SA_LICENSE)
                                    
    photo_notes = models.TextField(blank=True, help_text="Not visible to the public at any time.")
    
    
    audio = models.FileField(upload_to="supplemental_audio", blank=True, null=True)
    audio_title = models.CharField(max_length=100, blank=True)
    audio_caption = models.CharField(max_length=255, blank=True)
    audio_transcription = models.TextField(blank=True)
    audio_credit = models.CharField(max_length=255, blank=True)
    audio_copyright = models.CharField(max_length=255, blank=True)
    
    audio_license = models.CharField(max_length=20,
                                     choices=LICENSE_CHOICES,
                                     default=CC_BY_SA_LICENSE)
                                    
    audio_notes = models.TextField(blank=True, help_text="Not visible to the public at any time.")
    
    
    # downloadable file: PDF, JSON, or Zip for now
    attached_file = models.FileField(upload_to="supplemental_file", blank=True, null=True)
    attached_file_title = models.CharField(max_length=100, blank=True)
    attached_file_caption = models.CharField(max_length=255, blank=True)
    attached_file_type = models.CharField(max_length=20,
                                          choices=ATTACHMENT_TYPE_CHOICES,
                                          default=NONE_ATTACHMENT_TYPE)
                                     
    attached_file_credit = models.CharField(max_length=255, blank=True)
    attached_file_copyright = models.CharField(max_length=255, blank=True)
    
    attached_file_license = models.CharField(max_length=20,
                                             choices=LICENSE_CHOICES,
                                             default=CC_BY_SA_LICENSE)
                                    
    attached_file_notes = models.TextField(blank=True, help_text="Not visible to the public at any time.")
    
    
    created_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField('last modified', auto_now=True)
    
    
    def __unicode__(self):
        return self.slug
        
    class Meta:
        ordering = ['mod_date'] # or display_order


# TreeGroup model