from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.core.serializers import serialize

from django.db.models import Count, Max

from trees.models import NotableTree, TreeGenus
from trees.utilities import trees_as_geojson

def index(request):
    """
    main page with map, links to about, etc.
    """
    
    context = {"geojson": trees_as_geojson(NotableTree.objects.all())}
    return render(request, 'trees/index.html', context)


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
    context = {'tree': tree }
    return render(request, 'trees/tree_detail.html', context)
