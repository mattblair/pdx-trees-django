from django.contrib import admin

from models import NotableTree, TreeGenus, TreePhoto, SupplementalContent


class NotableTreeAdmin(admin.ModelAdmin):
    
    readonly_fields = ['created_date', 'mod_date',
    'city_tree_id', 'scientific_name', 'common_name',
    'address', 'year_designated', 'owner', 'city_notes',
    'height', 'spread', 'circumference', 'diameter',
    'city_object_id', 'city_status', 'state_id',
    'latitude', 'longitude',
    'legacy_uuid','public_photo_count'] 
    
    list_display = ('city_tree_id', 'common_name', 'address')
    
    fieldsets = [
            ('City Data', {
                'fields': [
                    ('city_tree_id', 'scientific_name', 'common_name'),
                    ('address', 'year_designated', 'owner'),
                    'city_notes',
                    ('latitude', 'longitude')
                ]
            }),
            ('Statistics', {
                'fields': [
                    ('height', 'spread'),
                    ('circumference', 'diameter'),
                    'public_photo_count'
                ]
            }),
            ('City (Unused)', {
                'fields': [
                    'city_object_id', 'city_status', 'state_id'
                ],
                'classes': ['collapse']
            }),
            ('Display', {
                'fields': [
                    'genus',
                    ('designation', 'display_icon')
                ]
            }),
            ('Removed Trees', {
                'fields': [
                    ('deceased', 'year_deceased'),
                    'cause_of_death'
                ]
            }),
            ('Internal', {
                'fields' : [
                    'internal_notes',
                    ('created_date', 'mod_date'),
                    'legacy_uuid'
                ]
            })
    ]


admin.site.register(NotableTree, NotableTreeAdmin)


class TreeGenusAdmin(admin.ModelAdmin):
    
    list_display = ('genus_name', 'common_name', 'display_in_menu', 'display_order')
    list_filter = ['display_in_menu']
    prepopulated_fields = {'slug': ('genus_name',)}


admin.site.register(TreeGenus, TreeGenusAdmin)


class TreePhotoAdmin(admin.ModelAdmin):
    
    list_display = ('related_tree', 'submitted_date', 'review_status')
    list_filter = ['review_status']
    readonly_fields = ['created_date', 'mod_date',
        'submitted_caption', 'submitted_name', 'submitted_email',
        'submitted_tree_id', 'submitted_date', 'submitted_url',
        'submitted_user_agent', 'submitted_image',
        'submitted_latitude', 'submitted_longitude',
        'related_tree', 'legacy_uuid'
    ]
    
    fieldsets = [
            ('Submitted', {
                'fields': [
                    ('submitted_caption', 'submitted_name', 'submitted_email'),
                    ('submitted_tree_id', 'submitted_date', 'submitted_url'),
                    ('submitted_user_agent', 'submitted_image'),
                    ('submitted_latitude', 'submitted_longitude')
                ]
            }),
            ('Moderation', {
                'fields': [
                    ('review_status', 'reviewed_date'),
                    'review_notes'
                ]
            }),
            ('Public', {
                'fields': [
                    'approved_image_filename',
                    'approved_submitter_name',
                    'approved_caption'
                ]
            }),
            ('Metadata', {
                'fields': [
                    ('created_date', 'mod_date'),
                    ('related_tree', 'legacy_uuid')
                ]
            })
    ]


admin.site.register(TreePhoto, TreePhotoAdmin)


class SupplementalContentAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'mod_date', 'content_type', 'workflow_status')
    list_filter = ['workflow_status']
    readonly_fields = ['created_date', 'mod_date', 'content_type', 'object_id', 'content_object']

admin.site.register(SupplementalContent, SupplementalContentAdmin)