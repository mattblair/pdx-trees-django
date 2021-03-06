from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.core.serializers import serialize

from django.db.models import Count, Max

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


from trees.models import NotableTree, TreeGenus, SupplementalContent
from trees.utilities import trees_as_geojson

from trees.forms import SupplementalContentForm


def index(request):
    """
    main page with map, links to about, etc.
    """
    
    context = {"geojson": trees_as_geojson(NotableTree.objects.all())}
    return render(request, 'trees/index.html', context)


def public_logout(request):
    logout(request)
    return redirect('trees:index_url')


# DEPRECATED
def missing_list(request):
    """
    Iterates from 1 to max city_tree_id, collects missing id #s.
    This is really just a demo. 
    In production, focus on those marked deceased.
    """
    
    missing_tree_list = []
    
    maxtreeid = NotableTree.objects.all().aggregate(Max('city_tree_id'))
    
    for tid in range(1, maxtreeid['city_tree_id__max']):
        t = NotableTree.objects.filter(city_tree_id=tid)
        if not t:
            missing_tree_list.append(tid)
    
    context = {"missing_tree_list": missing_tree_list}
    
    return render(request, 'trees/missing_list.html', context)


def ghost_list(request):
    """
    Template can differentiate between known and unknown for now...
    """
    
    ghost_trees = NotableTree.objects.filter(deceased=True)
    
    context = {
        "ghost_trees": ghost_trees,
        "geojson": trees_as_geojson(ghost_trees)
        
    }
    
    return render(request, 'trees/ghost_list.html', context)


def no_photos_list(request):
    
    np = NotableTree.objects.filter(public_photo_count=0)
    
    context = {
        "tree_list": np,
        "geojson": trees_as_geojson(np),
        "photo_list_title": "Trees Without Photos",
        "photo_list_description": "We don't have any photos for these. Please click a tree to learn more about it, visit, and take a photo!"
    }
    
    return render(request, 'trees/by_photo_count.html', context)


def least_photographed_list(request):
    """
    The threshold for least photographed should change over time.
    """
    
    nt = NotableTree.objects.filter(public_photo_count__lt=3).filter(public_photo_count__gt=0).order_by('-public_photo_count')
    
    context = {
        "tree_list": nt,
        "geojson": trees_as_geojson(nt),
        "photo_list_title": "Least Photographed Trees",
        "photo_list_description": "We have a photo or two for these trees, but it would be great to have more. Please click a tree to learn more about it, visit, and take a photo!"
    }
    
    return render(request, 'trees/by_photo_count.html', context)


def most_photographed_list(request):
    """
    This theshold value should rise over time, too.
    """
    
    nt = NotableTree.objects.filter(public_photo_count__gte=8).order_by('-public_photo_count')
    
    context = {
        "tree_list": nt,
        "geojson": trees_as_geojson(nt),
        "photo_list_title": "Most Photographed Trees",
        "photo_list_description": "These trees are the most popular by far!"
    }
    
    return render(request, 'trees/by_photo_count.html', context)


def genus_detail(request, genus_slug):
    """
    Returns genus, to display genus-specific info, and trees of that genus.
    """
    
    genus = get_object_or_404(TreeGenus, slug=genus_slug)
    
    #genus_menu_list = TreeGenus.objects.filter(display_in_menu=True)
    genus_menu_list = TreeGenus.objects.all()
    
    genus_type = ContentType.objects.get_for_model(genus)
    
    related_content = SupplementalContent.objects.filter(
        content_type__pk=genus_type.id,
        object_id=genus.id
    )
    
    context = {
        "genus": genus,
        "genus_menu_list": genus_menu_list,
        "geojson": trees_as_geojson(genus.trees.all()),
        'related_content': related_content
    }
    return render(request, 'trees/genus_detail.html', context)


# DEPRECATED
def genus_search(request, genus_fragment):
    """
    Runs a wildcard search on scientific name, starting with genus_frament
    Note that this is url-based, not form-based, at least for now.
    Or you could list a series of links?
    """
    
    # try to find some based on the fragment
    
    trees_in_genus = NotableTree.objects.filter(scientific_name__startswith=genus_fragment)
    
    # if none found, return none
    
    # this should probably be defined centrally somewhere
    # and be checked for comprehensiveness
    genus_dict = {}
    genus_dict["Pinus"] = "Pine"
    genus_dict["Ulmus"] = "Elm"
    genus_dict["Quercus"] = "Oak"
    genus_dict["Fagus"] = "Beech"
    genus_dict["Carya"] = "Hickory"
    genus_dict["Acer"] = "Maple"
    genus_dict["Cedrus"] = "Cedar"
    genus_dict["Juglans"] = "Walnut"
    genus_dict["Sequoia"] = "Redwood (?)" 
    genus_dict["Platanus"] = "Planetree"    
    
    context = {
        "genus_dict": genus_dict,
        "genus_fragment" : genus_fragment,
        "trees_in_genus" : trees_in_genus,
        "geojson": trees_as_geojson(trees_in_genus)
    }
    return render(request, 'trees/genus_search.html', context)


def year_list(request):
    """
    Count of trees designated from 1973 to present (including years with none)
    """
    # get counts for each year, in order
    
    # iterate through, and add a 0 when non-represented years
    
    trees_counts = NotableTree.objects.values('year_designated').annotate(year_count=Count('year_designated')).order_by('year_designated')
    
    # the result is a list of objects like this:
    # {'year_count': 1, 'year_designated': 1973}
    # convert into a dictionary so we can search on the year:
    count_dict = {}
    for yc in trees_counts:
    	count_dict[yc['year_designated']] = yc['year_count']
    
    starting_year = 1973
    ending_year = 2015 # not inclusive
    
    trees_by_year = []
    
    for year in range(starting_year, ending_year):

    	if year in count_dict:
    		trees_by_year.append( {"year": year, "tree_count": count_dict[year]})
    	else:
    		trees_by_year.append( {"year": year, "tree_count" : 0})
    		
    context = {"trees_by_year": trees_by_year}
    
    return render(request, 'trees/year_list.html', context)


def year_detail(request, year):
    """
    accepts year as a string, returns list of trees designated in that year
    """
    trees_in_year = NotableTree.objects.filter(year_designated=year)
    
    context = {
        "trees_in_year": trees_in_year,
        "year": year,
        "geojson": trees_as_geojson(trees_in_year)
    }
    
    return render(request, 'trees/year_detail.html', context)


def tree_detail(request, treeid):
    """
    Show details for a tree, including a map
    """
    tree = get_object_or_404(NotableTree, city_tree_id=treeid)
    
    # get content type of tree
    tree_type = ContentType.objects.get_for_model(tree)
    # use that content_type to fetch related content
    related_content = SupplementalContent.objects.filter(content_type__pk=tree_type.id,object_id=tree.id)
    
    # and do the same for genus
    genus_type = ContentType.objects.get_for_model(tree.genus)
    
    genus_related_content = SupplementalContent.objects.filter(
        content_type__pk=genus_type.id,
        object_id=tree.genus.id
    )
    
    context = {
        'tree': tree,
        'geojson': trees_as_geojson([tree]),
        'related_content': related_content,
        'genus_related_content': genus_related_content
    }
    return render(request, 'trees/tree_detail.html', context)


@login_required
def tree_add_content(request, treeid):
    """
    Show/process form for submitting supplemental content for a tree.
    """
    tree = get_object_or_404(NotableTree, city_tree_id=treeid)
    
    content_form = SupplementalContentForm(request.POST or None, request.FILES)
    
    if request.method == 'POST':
        
        if content_form.is_valid():
            
            new_content = content_form.save(commit=False)
            
            # set tree and author
            new_content.content_object = tree
            new_content.author = request.user
            
            # set any other properties
            
            new_content.save()
                
            messages.add_message(request, messages.SUCCESS, 'Submission saved.')
            
            return HttpResponseRedirect(reverse('trees:tree_detail_url', args=[treeid]))
        
        else:
            # TODO: Add a more specific validation error, or pass errors through
            # print request.POST
            messages.add_message(request, messages.WARNING, 'Content could not be saved.')
    
    # if the request method is a GET, send tree detail + form
    context = {
        'tree': tree,
        'geojson': trees_as_geojson([tree]),
        'content_form': content_form
    }
    return render(request, 'trees/tree_add_content.html', context)


@login_required
def genus_add_content(request, genus_slug):
    """
    Show/process form for submitting supplemental content for a tree.
    """
    
    genus = get_object_or_404(TreeGenus, slug=genus_slug)
    
    content_form = SupplementalContentForm(request.POST or None, request.FILES)
    
    if request.method == 'POST':
        
        if content_form.is_valid():
            
            new_content = content_form.save(commit=False)
            
            # set genus and author
            new_content.content_object = genus
            new_content.author = request.user
            
            # set any other properties
            
            new_content.save()
                
            messages.add_message(request, messages.SUCCESS, 'Submission saved.')
            
            return HttpResponseRedirect(reverse('trees:genus_detail_url', args=[genus_slug]))
        
        else:
            # TODO: Add a more specific validation error, or pass errors through
            # print request.POST
            messages.add_message(request, messages.WARNING, 'Content could not be saved for this genus.')
    
    # if the request method is a GET, send tree detail + form
    context = {
        'genus': genus,
        'geojson': trees_as_geojson(genus.trees.all()),
        'content_form': content_form
    }
    return render(request, 'trees/genus_add_content.html', context)
