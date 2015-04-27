from django.contrib import admin

from models import NotableTree, TreeGenus


class NotableTreeAdmin(admin.ModelAdmin):
    
    readonly_fields = ['created_date', 'mod_date',
    'city_tree_id', 'scientific_name', 'common_name',
    'address', 'year_designated', 'owner', 'city_notes',
    'height', 'spread', 'circumference', 'diameter',
    'city_object_id', 'city_status', 'state_id',
    'latitude', 'longitude',
    'legacy_uuid'] 
    
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
                    ('circumference', 'diameter')
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