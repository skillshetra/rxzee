####################################### Importing Packages #######################################
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_GET
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from app.models import User
from app import models as AwsDynamoDb
from RxZee.settings import ADMIN_PATH, ALLOWED_HOSTS
from functools import reduce
from operator import or_
from re import search
from itertools import combinations
#################################################################################################################################################################
################################################################### Global Views Start Here #####################################################################
#################################################################################################################################################################

##################### HomePage #####################
def HomePage(request):
    metadata = {"og_description": "Giving reliable and impartial details about more than 23,000 prescription drugs, over-the-counter drugs, and health-related subjects.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com"}
    news = AwsDynamoDb.news.objects.filter(status="approved").order_by('-search_count').only('permalink', 'title', 'featured_image')[:6]
    return render(request, "homepage.html", {"title": "Information about health and prescription drugs", 'HomePage': AwsDynamoDb.HomePage.objects.first(), 'top_news': news.first(), 'news': list(news)[1:], "trendingSearches": AwsDynamoDb.drug_search.objects.filter(off_market_drug = False).order_by('search_count').only('permalink', 'name')[:5], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
##################### Drugs Pages Starts Here #####################
def drugsPage(request):
    metadata = {"og_description": "Our A to Z list of over 23,000 prescription and over-the-counter drugs makes it easy and quick to find the medicine you need.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/drugs"}
    latest_drugs_news = AwsDynamoDb.news.objects.filter(status="approved", category='Drugs').only('permalink', 'title', 'search_count')
    return render(request, "drugs.html", {"title": "Medicines and drugs from A to Z", "mostFrequentSearches": list({record['name']: record for record in list(AwsDynamoDb.drug_search.objects.filter(off_market_drug = False).order_by('name')[:500].values("permalink", "name"))}.values()), "latestDrugsNews": list(latest_drugs_news), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Drugs', 'link': "/drugs"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
def drugsCategoryPage(request, slug):
    metadata = {"og_description": "Our A to Z list of over 23,000 prescription and over-the-counter drugs makes it easy and quick to find the medicine you need.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": f"https://rxzee.com/drugs/alpha{slug}"}
    try:
        if slug == '0-9':
            drugs = list(AwsDynamoDb.drug_search.objects.filter((Q(name__istartswith='0') | Q(name__istartswith='1') | Q(name__istartswith='2') | Q(name__istartswith='3') | Q(name__istartswith='4') | Q(name__istartswith='5') | Q(name__istartswith='6') | Q(name__istartswith='7') | Q(name__istartswith='8') | Q(name__istartswith='9')) &Q(off_market_drug=False)).order_by('name').distinct('name').values("permalink", "name"))
        else:
            drugs = list(AwsDynamoDb.drug_search.objects.filter(name__istartswith=slug.lower(), off_market_drug=False).order_by('name').distinct('name').values("permalink", "name"))
    except:
        drugs = False
    google_tag_id = AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()
    if drugs and len(slug) < 4:
        return render(request, "drugsCategory.html", {"title": f"Medicines and drugs from {slug.upper()}", "slug": slug, "drugs": drugs, "hidden": len(slug) > 1, "allSecondAvailable": list({drug['name'][1] for drug in drugs if len(drug['name']) > 1}), "breadcrumbs": [{'name': 'Home', 'link': "/"}, {'name': f'Drugs starting {slug}', 'link': f"/drugs/alpha/{slug}/"}], "GoogleTagId": google_tag_id, "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/drugs')
def drugsOffMarketPage(request, slug):
    metadata = {"og_description": "Our A to Z list of over 23,000 prescription and over-the-counter drugs makes it easy and quick to find the medicine you need.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/drugs"}
    latest_drugs_news = AwsDynamoDb.news.objects.filter(status="approved", category='Drugs').only('permalink', 'title', 'search_count')
    try:
        if slug == '0-9':
            drugs = list(AwsDynamoDb.drug_search.objects.filter((Q(name__istartswith='0') | Q(name__istartswith='1') | Q(name__istartswith='2') | Q(name__istartswith='3') | Q(name__istartswith='4') | Q(name__istartswith='5') | Q(name__istartswith='6') | Q(name__istartswith='7') | Q(name__istartswith='8') | Q(name__istartswith='9')) & Q(off_market_drug=True)).order_by('name').distinct('name').values("permalink", "name"))
        else:
            drugs = list(AwsDynamoDb.drug_search.objects.filter(name__istartswith=slug.lower(), off_market_drug=True).order_by('name').distinct('name').values("permalink", "name"))
    except:
        drugs = False
    if drugs:
        return render(request, "drug-offmarket.html", {"title": "Off-Market Medicines and drugs from A to Z", 'slug': slug, "drugs": drugs, "latestDrugsNews": list(latest_drugs_news), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Off-Market Drugs', 'link': f"/drugs/off-market/{slug}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/drugs')
def drugsConditionsPage(request):
    metadata = {"og_description": "Our A to Z list of over 23,000 prescription and over-the-counter drugs makes it easy and quick to find the medicine you need.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/drugs"}
    condition = request.GET.get('condition', False)
    drugs = []
    if condition:
        conditions = []
        drugs = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug = False).filter(condition = condition.replace('-', ' ')).values('name', 'permalink', 'label', 'type'))
    else:
        conditions = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug=False).exclude(condition__isnull=True).exclude(condition='').order_by('condition', 'search_count').distinct('condition')[:50].values_list('condition', flat = True))
    return render(request, "drug_conditions.html", {"title": "Medicines and drugs from A to Z", "conditions": conditions, 'drugs': drugs, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Drug Conditions', 'link': "/drugs/conditions"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
def drugsConditionsCategoryPage(request, slug):
    metadata = {"og_description": "Our A to Z list of over 23,000 prescription and over-the-counter drugs makes it easy and quick to find the medicine you need.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/drugs"}
    condition = request.GET.get('condition', False)
    drugs = []
    if condition:
        conditions = []
        drugs = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug = False).filter(condition = condition.replace('-', ' ')).values('name', 'permalink', 'label', 'type'))
    else:
        drugs = []
        if slug == '0-9':
            conditions = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug=False).filter(Q(condition__istartswith='0') | Q(condition__istartswith='1') | Q(condition__istartswith='2') | Q(condition__istartswith='3') | Q(condition__istartswith='4') | Q(condition__istartswith='5') | Q(condition__istartswith='6') | Q(condition__istartswith='7') | Q(condition__istartswith='8') | Q(condition__istartswith='9')).exclude(condition__isnull=True).exclude(condition='').order_by('condition', 'search_count').distinct('condition').values_list('condition', flat=True))
        else:
            conditions = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug=False).filter(condition__istartswith=slug.lower()).exclude(condition__isnull=True).exclude(condition='').order_by('condition', 'search_count').distinct('condition').values_list('condition', flat=True))
    return render(request, "drug_conditions.html", {"title": "Medicines and drugs from A to Z", "conditions": conditions, 'drugs': drugs, 'slug': slug, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Drug Conditions', 'link': f"/drugs/conditions/alpha{slug}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
##################### Vitamins and Supplements Pages Starts Here #####################
def vitaminsAndSupplementsPage(request):
    metadata = {"og_description": "RxZee's collection covers vitamins and supplements from A to Z. From health advantages to side effects and links, our professional sources cover it all.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/vitamins"}
    approved_vitamins_and_supplements = AwsDynamoDb.vitaminsAndSupplement.objects.filter(status="approved").only('permalink', 'name', 'search_count')
    latest_news = AwsDynamoDb.news.objects.filter(category='Vitamins', status="approved").only('permalink', 'title')[:5]
    return render(request, "vitaminsAndSupplements.html", {"title": "A to Z information about vitamins and supplements in one place", "mostFrequentSearches": list(approved_vitamins_and_supplements.order_by('-search_count').values('permalink', 'name')[:50]), "vitaminsAndSupplements": list(approved_vitamins_and_supplements.values('permalink', 'name')), "latestVitaminsAndSupplementsNews": list(latest_news), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Supplements and Vitamins', 'link': "/vitamins"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
def vitaminsAndSupplementsCategoryPage(request, slug):
    metadata = {"og_description": "RxZee's collection covers vitamins and supplements from A to Z. From health advantages to side effects and links, our professional sources cover it all.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": f"https://rxzee.com/vitamins/alpha/{slug}"}
    vitamins_and_supplements = list(AwsDynamoDb.vitaminsAndSupplement.objects.filter(name__istartswith=slug, status="approved").values("permalink", "name"))
    if vitamins_and_supplements and len(slug) < 3:
        return render(request, "vitaminsAndSupplementsCategory.html", {"title": f"{slug} information about vitamins and supplements in one place", "slug": slug, "vitaminsAndSupplements": vitamins_and_supplements, "hidden": len(slug) != 2, "allSecondAvailable": list({vs.get('name')[1] for vs in vitamins_and_supplements if len(vs.get('name', '')) > 1}), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': f'Supplements and Vitamins starting {slug}', 'link': f"/vitamins/category/{slug}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/vitamins')
##################### Vitamins and Supplements Pages Ends Here #######################

######################################################################################################################################################################################
######################################################################################################################################################################################

##################### Pill Identifications Pages Starts Here #####################
def show_pill(request, permalink):
    metadata = {"og_description": "", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": f"https://rxzee.com/imprints/{permalink}"}
    pill_data = True
    if pill_data:
        return render(request, "imprint.html", {"title": f"Imprints", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': f'Imprint', 'link': f"/imprints/{permalink}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/pill-identifier')
def pillIdentifier(request):
    colors = [{ "name": "Orange", "code": "bg-[#FFA500]" }, { "name": "White", "code": "bg-[#FFFFFF]" }, { "name": "Peach", "code": "bg-[#FFDAB9]" }, { "name": "Off-White", "code": "bg-[#F8F8F0]" }, { "name": "Yellow", "code": "bg-[#FFFF00]" }, { "name": "Clear", "code": "bg-[#ffffff50]" }, { "name": "Gold", "code": "bg-[#FFD700]" }, { "name": "Gray", "code": "bg-[#A9A9A9]" }, { "name": "Green", "code": "bg-[#008000]" }, { "name": "Black", "code": "bg-[#000000]" }, { "name": "Turquoise", "code": "bg-[#40E0D0]" }, { "name": "Tan", "code": "bg-[#D2B48C]" }, { "name": "Blue", "code": "bg-[#0000FF]" }, { "name": "Brown", "code": "bg-[#A52A2A]" }, { "name": "Purple", "code": "bg-[#800080]" }, { "name": "Red", "code": "bg-[#FF0000]" }, { "name": "Pink", "code": "bg-[#FFC0CB]" }, { "name": "Multi-Color", "code": "bg-gradient-to-r from-red-500 via-yellow-500 to-blue-500"}]
    shapes = [{"name": "Round", "svg": "<svg width='20' height='20'><circle cx='10' cy='10' r='8' fill='#374151' /></svg>"}, {"name": "Oblong", "svg": "<svg width='20' height='10'><rect x='2' y='0' width='16' height='10' rx='5' fill='#374151' /></svg>"}, {"name": "Oval", "svg": "<svg width='20' height='10'><ellipse cx='10' cy='5' rx='8' ry='4' fill='#374151' /></svg>"}, {"name": "Five-Sided", "svg": "<svg width='20' height='20'><polygon points='10,2 18,8 14,18 6,18 2,8' fill='#374151' /></svg>"}, {"name": "Rectangular", "svg": "<svg width='20' height='10'><rect x='2' y='2' width='16' height='6' fill='#374151' /></svg>"}, {"name": "Trapezoidal", "svg": "<svg width='20' height='10'><polygon points='4,10 16,10 14,2 6,2' fill='#374151' /></svg>"}, {"name": "Diamond", "svg": "<svg width='20' height='20'><polygon points='10,2 18,10 10,18 2,10' fill='#374151' /></svg>"}, {"name": "Elliptical", "svg": "<svg width='20' height='10'><ellipse cx='10' cy='5' rx='10' ry='5' fill='#374151' /></svg>"}, {"name": "Square", "svg": "<svg width='20' height='20'><rect width='16' height='16' x='2' y='2' fill='#374151' /></svg>"}, {"name": "Triangular", "svg": "<svg width='20' height='20'><polygon points='10,2 18,18 2,18' fill='#374151' /></svg>"}, {"name": "Pentagon", "svg": "<svg width='20' height='20'><polygon points='10,2 18,8 18,18 10,20 2,18 2,8' fill='#374151' /></svg>"}, {"name": "Almond", "svg": "<svg width='20' height='10'><path d='M10 2 C 18 5, 18 5, 10 8 C 2 5, 2 5, 10 2' fill='#374151' /></svg>"}, {"name": "Hexagonal", "svg": "<svg width='20' height='20'><polygon points='10,2 18,8 18,18 10,20 2,18 2,8' fill='#374151' /></svg>"}, {"name": "Cylindrical", "svg": "<svg width='20' height='20'><rect x='6' y='4' width='8' height='12' fill='#374151' /><ellipse cx='10' cy='4' rx='6' ry='3' fill='#374151' /><ellipse cx='10' cy='16' rx='6' ry='3' fill='#374151' /></svg>"}, {"name": "Teardrop", "svg": "<svg width='20' height='20'><path d='M10,2 C14,2 18,8 10,18 C2,8 6,2 10,2' fill='#374151' /></svg>"}, {"name": "Shield", "svg": "<svg width='20' height='20'><path d='M10 2 L18 6 L14 18 L6 18 L2 6 Z' fill='#374151' /></svg>"}, {"name": "Bullet", "svg": "<svg width='20' height='20'><circle cx='10' cy='10' r='10' fill='#374151' /></svg>"}, {"name": "Square (Rounded Corners)", "svg": "<svg width='20' height='20'><rect width='16' height='16' x='2' y='2' rx='2' fill='#374151' /></svg>"}, {"name": "Rectangular (Rounded End)", "svg": "<svg width='20' height='10'><rect x='2' y='0' width='16' height='10' rx='5' fill='#374151' /></svg>"}, {"name": "Other", "svg": ""}]
    metadata = {"og_description": "RxZee's Pill Identifier lets you find and identify any over-the-counter or prescription drug, pill, or medicine by color, shape, or imprint. You can instantly compare medicine images.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/pill-identifier/"}
    latestDrugsNews = [{"title": "Popular Weight Loss Drugs Raise Risk of More Stomach Trouble", "link": "link"}, {"title": "New Depression Drug Avoids Unfortunate Side Effects of Others", "link": "link"}, {"title": "FDA Adds Warning of Intestinal Blockages to Ozempic Label", "link": "link"}, {"title": "3D-Printed Meds Customize the Exact Dose for Sick Children", "link": "link"}]
    context = {"title": "Find Pills by Color, Shape, Imprint, or Picture with Pill Identifier", 'latestDrugsNews': latestDrugsNews, 'imprint': '', 'shape': False, 'color': False, 'color_class': '', 'shape_class': '', 'heading': 'Commonly Searched Pill Imprints.', 'allPills': list(AwsDynamoDb.pill.objects.filter(status="approved").order_by('?').values('redirect_url_imprint', 'imprint_side_1', 'imprint_side_2', 'name', 'image', 'redirect_url_name')[:100]), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Pill Identifier', 'link': "/pill-identifier"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
    if request.method == "POST":
            context['imprint'] = [item.strip() for item in request.POST.get('imprint', '|').split('|')]
            context['color'] = request.POST.get('color', '').strip()
            context['shape'] = request.POST.get('shape', '').strip()
            context['color_class'] = next((color['code'] for color in colors if color['name'] == context['color']), None)
            context['shape_class'] = next((shape['svg'] for shape in shapes if shape['name'] == context['shape']), None)
            filters = Q(status="approved")
            if context['imprint'][0] != "" or (context['color'] != "Select Color" and context['color'] != "Multi-Color" and context['color'] != "") or (context['shape'] != "Select Shape" and context['shape'] != "Other" and context['shape'] != ""):
                if context['imprint'][0] != "":
                    if len(context['imprint']) == 1:
                        filters &= Q(*[Q(imprint_side_1 = imprint) | Q(imprint_side_2 = imprint) for imprint in context.get('imprint', [])]) if context.get('imprint') else Q()
                    else:
                        filters &= Q(*[Q(imprint_side_1__icontains = imprint) | Q(imprint_side_2__icontains = imprint) for imprint in context.get('imprint', [])]) if context.get('imprint') else Q()
                if context['color'] and context['shape'] != "Multi-Color":
                    filters &= Q(color__icontains = context['color']) 
                if context['shape'] and context['shape'] != "Other":
                    filters &= Q(shape = context['shape'])
                context['allPills'] = list(AwsDynamoDb.pill.objects.filter(filters).values('redirect_url_name', 'redirect_url_imprint', 'name', 'generic_name', 'strength', 'imprint_side_1', 'imprint_side_2', 'color', 'shape', 'image'))
                context['heading'] = f"There are a total of {len(context['allPills'])} pills for your search."
    return render(request, "pillIdentifier.html", context)
##################### Pill Identifications Pages Ends Here #######################

##################### Interaction Checker Pages Starts Here #####################
def interactionChecker(request):
    drugs = [AwsDynamoDb.drug_search.objects.filter(id = drug).values('name', 'generic_name', 'id').first() for drug in request.GET.get('drugs', '').split(',') if drug] if request.GET.get('drugs', '') else False
    generic_name = request.GET.get('generic_name', '').split(',') if request.GET.get('generic_name', '').strip() else False
    drugs_list = ''
    generic_name_list = ''
    if drugs and generic_name:
        show_input = len(drugs) + len(generic_name) > 3
        drugs_list = ', '.join([f"{drug['name']} ({drug['generic_name'].replace('|', ', ')})" for drug in drugs if drug])
        generic_name_list = ', '.join(generic_name) if generic_name else ''
        metadata = {"og_description": f"Drug Interaction List of drugs: {drugs_list} and generic names: {generic_name_list}", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/interaction-checker"}
    elif drugs:
        drugs_list = ', '.join([f"{drug['name']} ({drug['generic_name'].replace('|', ', ')})" for drug in drugs if drug])
        show_input = len(drugs) > 3
        metadata = {"og_description": f"Drug Interaction List of drugs: {drugs_list}", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/interaction-checker"}
    elif generic_name:
        generic_name_list = ', '.join(generic_name) if generic_name else ''
        show_input = len(generic_name) > 3
        metadata = {"og_description": f"Drug Interaction List of generic names: {generic_name_list}", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/interaction-checker"}
    else:
        show_input = False
        metadata = {"og_description": "Enter two or more drugs into the RxZee Drug Interaction Checker tool to find and identify potentially harmful and unsafe dose combinations of prescription drugs.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/interaction-checker"}
    context = {"title": "Drug Interaction Checker - Quickly Look Over Your Medications", 'drugs': drugs, 'drugs_list': drugs_list, 'generic_name_list': generic_name_list, 'generic_name': generic_name, 'show_input': show_input, 'dont_show': False if drugs or generic_name else True, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Interactions Checker', 'link': "/interaction-checker"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
    return render(request, "interactionChecker.html", context)
def checkerInteractions(request):
    interactions = {'drugs': False, 'food': False, 'disease': False}
    drugs_list = set(request.GET.get('drugs_list', []).replace('-', ' ').replace('), ', ')), ').split('),') if request.GET.get('drugs_list', []) else [])
    generic_name_list = set(request.GET.get('generic_name_list', []).replace('-', ' ').split(', ')) if request.GET.get('generic_name_list', []) else []
    one_drug = False
    if drugs_list and generic_name_list and len(drugs_list) + len(generic_name_list) > 4:
        return redirect('/interaction-checker')
    else:
        if generic_name_list and drugs_list:
            generic_name_list.update({value.strip().strip("'") for drug in drugs_list if (match := search(r'\((.*?)\)', drug)) for value in match.group(1).split(',')})
            generic_name_list = list(generic_name_list)
        elif drugs_list:
            generic_name_list = list(set(name.strip() for drug in drugs_list for name in search(r'\((.*?)\)', drug).group(1).split(',')))
        drugs_list = list(drugs_list)
        generic_name_list = list(generic_name_list)
        if (len(drugs_list) == 1 and all([generic_name in drugs_list[0] for generic_name in generic_name_list])) or (len(drugs_list) != 1 and len(generic_name_list) < 2):
            one_drug = drugs_list[0] if drugs_list else generic_name_list[0]
            interactions['drugs'] = list(AwsDynamoDb.drug_interactions.objects.filter(Q(first_drug = generic_name_list[0]) | Q(second_drug = generic_name_list[0]) & Q(status = 'approved')).order_by('first_drug', 'second_drug', 'level').values('first_drug', 'second_drug', 'level'))
            interactions['food'] = list(AwsDynamoDb.food_interactions.objects.filter(Q(status = 'approved') & reduce(or_, (Q(formula__iexact = name) for name in generic_name_list))).select_related('author').values('formula', 'header', 'severity', 'other_details', 'level', 'consumer', 'professional', 'author__first_name', 'author__id', 'status', 'last_updated'))
            interactions['disease'] = list(AwsDynamoDb.disease_interactions.objects.filter(Q(status = 'approved') & reduce(or_, (Q(formula__iexact = name) for name in generic_name_list))).select_related('author').values('formula', 'header', 'severity', 'content', 'level', 'author__first_name', 'author__id', 'last_updated'))
        else:
            interactions['drugs'] = [interaction for drugs in [{'first_drug': first, 'second_drug': second} for first, second in combinations(generic_name_list, 2)] for interaction in (list(AwsDynamoDb.drug_interactions.objects.filter((Q(first_drug=drugs['second_drug']) & Q(second_drug=drugs['first_drug'])) | (Q(first_drug=drugs['first_drug']) & Q(second_drug=drugs['second_drug'])), status='approved').select_related('author').values('first_drug', 'second_drug', 'level', 'consumer', 'professional', 'author__first_name', 'author__id', 'last_updated')) ) if interaction]
            interactions['food'] = list(AwsDynamoDb.food_interactions.objects.filter(Q(status = 'approved') & reduce(or_, (Q(formula__iexact = name) for name in generic_name_list))).select_related('author').values('formula', 'header', 'severity', 'other_details', 'level', 'consumer', 'professional', 'author__first_name', 'author__id', 'status', 'last_updated'))
            interactions['disease'] = list(AwsDynamoDb.disease_interactions.objects.filter(Q(status = 'approved') & reduce(or_, (Q(formula__iexact = name) for name in generic_name_list))).select_related('author').values('formula', 'header', 'severity', 'content', 'level', 'author__first_name', 'author__id', 'last_updated'))
        interaction_length = (len(interactions['drugs']) if isinstance(interactions['drugs'], list) else 0) + (len(interactions['food']) if isinstance(interactions['food'], list) else 0) + (len(interactions['disease']) if isinstance(interactions['disease'], list) else 0)
        context = {"title": f"{request.GET.get('drugs_list', '')} {request.GET.get('generic_name_list', '')} Interactions - Quickly Look Over Your Medications", 'drugs_list': list(drugs_list), 'one_drug': one_drug, 'generic_name_list': generic_name_list, 'interaction_length': interaction_length, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Interactions Checker', 'link': "/interaction-checker"}], 'interactions': interactions, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': {"og_description": f"({interaction_length}) medications are known to interact with {request.GET.get('drugs_list', '')} {request.GET.get('generic_name_list', '')}", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/interaction-checker/interactions"}}
        return render(request, "interactionscheck.html", context)
##################### Interaction Checker Pages Ends Here #######################
######################################################################################################################################################################################
######################################################################################################################################################################################


##################### Conditions Pages Starts Here #####################
def conditionsPage(request, category = False, slug = False):
    category = category.replace('-', ' ') if category else False
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
    latestNews = [{'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}]
    if category and category != 'alpha' and  slug:
        specific_condition_article = AwsDynamoDb.condition.objects.filter(permalink = slug, category = category, status = "approved").first() or False
        if specific_condition_article:
            return render(request, "wellbeingconditionsSpecificPage.html", {"title": specific_condition_article.heading, 'specific_condition_article': specific_condition_article, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Conditions', 'link': "/conditions"}, {'name': category, 'link': f"/conditions/{category.replace(' ', '-')}/{slug}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'news': latestNews, 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
        else:
            return redirect('/conditions')
    elif category and category != 'alpha':
        sub_category = request.GET.get('sub_category', '').replace('-', ' ').strip()
        page = request.GET.get('page')
        articles = AwsDynamoDb.condition.objects.filter(category = category)
        if articles:
            sub_categories = list(set(articles.values_list('sub_category', flat = True)))
            if sub_category in sub_categories:
                paginator = Paginator(list(articles.filter(sub_category = sub_category).values('heading', 'content', 'permalink', 'featured_image')), 5)
            else:
                paginator = Paginator(list(articles.values('heading', 'content', 'permalink', 'featured_image')), 5)
            try:
                articles = paginator.page(page).object_list
            except PageNotAnInteger:
                articles = paginator.page(1).object_list
            except EmptyPage:
                articles = paginator.page(paginator.num_pages).object_list
            context = {"title": category, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Conditions', 'link': "/conditions"}, {'name': category, 'link': f"/conditions/{category.replace(' ', '-')}"}], 'sub_category': sub_category, 'sub_categories': sub_categories, 'articles': articles, 'page_numbers': list(paginator.page_range), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'news': latestNews, 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
            return render(request, "wellBeingConditionCategory.html", context)
        else:
            return redirect('/conditions')
    else:
        if category == 'alpha' and (len(slug) == 1 or slug == '0-9'):
            slug = slug.lower()
            conditions = ["A1AT Deficiency", "AAT", "AAT Deficiency", "Abdominal Migraine", "Abercrombie Syndrome", "Abnormal Pap Test", "Abortion", "Abruptio Placenta", "Abruption, Placental", "Abscessed Tooth", "Absence of Menstruation, Primary", "Absence Seizure", "Abuse, Child", "Babesiosis", "Baby", "Baby Hygiene", "Baby Safety", "Back Pain", "Bacterial Arthritis", "Bacterial Meningitis", "Bacterial Meningococcal Meningitis", "Bacterial Vaginosis", "Bad or Changed Breath", "Balance", "Baldness"]
            context = {"title": f"Conditions Starting {slug.upper()}", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': f'Conditions {slug.upper()}', 'link': f"/conditions/alpha/{slug.upper()}"}], 'conditions': conditions, 'slug': slug, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'news': latestNews, 'metadata': metadata, 'redirect_url':  "/conditions"}
        else:
            conditions = ["A1AT Deficiency", "AAT", "AAT Deficiency", "Abdominal Migraine", "Abercrombie Syndrome", "Abnormal Pap Test", "Abortion", "Abruptio Placenta", "Abruption, Placental", "Abscessed Tooth", "Absence of Menstruation, Primary", "Absence Seizure", "Abuse, Child", "Babesiosis", "Baby", "Baby Hygiene", "Baby Safety", "Back Pain", "Bacterial Arthritis", "Bacterial Meningitis", "Bacterial Meningococcal Meningitis", "Bacterial Vaginosis", "Bad or Changed Breath", "Balance", "Baldness"]
            context = {"title": "Conditions A-Z", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Conditions', 'link': "/conditions"}], 'conditions': conditions, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'news': latestNews, 'metadata': metadata, 'redirect_url':  "/conditions"}
        return render(request, "wellbeingconditions.html", context)
##################### Conditions Pages Ends Here #######################

##################### Well Being Pages Starts Here #####################
def WellBeing(request, category = False, slug = False):
    category = category.replace('-', ' ') if category else False
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
    latestNews = [{'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}, {'title': 'Symptoms of adult ADHD are generally treated with medicine', 'seo_description': "Symptoms of adult ADHD are generally treated with medicine. But there's more to effective treatment than just taking a pill."}]
    if category and category != 'alpha' and  slug:
        specific_condition_article = AwsDynamoDb.condition.objects.filter(permalink = slug, category = category, status = "approved").first() or False
        if specific_condition_article:
            return render(request, "wellbeingconditionsSpecificPage.html", {"title": specific_condition_article.heading, 'specific_condition_article': specific_condition_article, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Conditions', 'link': "/conditions"}, {'name': category, 'link': f"/conditions/{category.replace(' ', '-')}/{slug}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'news': latestNews, 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
        else:
            return redirect('/well-being')
    elif category and category != 'alpha':
        sub_category = request.GET.get('sub_category', '').replace('-', ' ').strip()
        page = request.GET.get('page')
        articles = AwsDynamoDb.condition.objects.filter(category = category)
        if articles:
            sub_categories = list(set(articles.values_list('sub_category', flat = True)))
            if sub_category in sub_categories:
                paginator = Paginator(list(articles.filter(sub_category = sub_category).values('heading', 'content', 'permalink', 'featured_image')), 5)
            else:
                paginator = Paginator(list(articles.values('heading', 'content', 'permalink', 'featured_image')), 5)
            try:
                articles = paginator.page(page).object_list
            except PageNotAnInteger:
                articles = paginator.page(1).object_list
            except EmptyPage:
                articles = paginator.page(paginator.num_pages).object_list
            context = {"title": category, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Conditions', 'link': "/conditions"}, {'name': category, 'link': f"/conditions/{category.replace(' ', '-')}"}], 'sub_category': sub_category, 'sub_categories': sub_categories, 'articles': articles, 'page_numbers': list(paginator.page_range), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'news': latestNews, 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
            return render(request, "wellBeingConditionCategory.html", context)
        else:
            return redirect('/well-being')
    else:
        if category == 'alpha' and (len(slug) == 1 or slug == '0-9'):
            slug = slug.lower()
            well_beings = ["Aging Well", "Baby", "Birth Control", "Children's Health", "Diet & Weight Management", "Fitness & Exercise", "Food & Recipes", "Health & Balance", "Healthy Beauty", "Men's Health", "Parenting", "Pet Health", "Pregnancy", "Sex & Relationships", "Teen Health", "Women's Health"]
            context = {"title": f"Well Being Starting {slug.upper()}", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': f'Well Being {slug.upper()}', 'link': f"/well-being/alpha/{slug.upper()}"}], 'conditions': well_beings, 'slug': slug, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'news': latestNews, 'metadata': metadata, 'redirect_url':  "/well-being"}
        else:
            well_beings = ["Aging Well", "Baby", "Birth Control", "Children's Health", "Diet & Weight Management", "Fitness & Exercise", "Food & Recipes", "Health & Balance", "Healthy Beauty", "Men's Health", "Parenting", "Pet Health", "Pregnancy", "Sex & Relationships", "Teen Health", "Women's Health"]
            context = {"title": "Well Being A-Z", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Well Being', 'link': "/well-being"}], 'conditions': well_beings, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'news': latestNews, 'metadata': metadata, 'redirect_url':  "/well-being"}
        return render(request, "wellbeingconditions.html", context)
##################### Well Being Pages Ends Here #######################

##################### NEWS Pages Starts Here #####################
def news(request, permalink = False):
    if permalink:
        news = AwsDynamoDb.news.objects.filter(status="approved", permalink = permalink).first()
        if news:
            return render(request, "newsSpecific.html", {"title": news.title, 'news': news, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'News', 'link': f"/news/{permalink}"}], 'metadata': {"og_description": news.seo_description, "og_image": news.featured_image, "og_url": f"https://rxzee.com/news/{permalink}"}})
        else:
            return redirect('/news')
    else:
        return render(request, "news.html", {"title": "Health, medical, and drug news—updated every day.", 'approved_news': list(AwsDynamoDb.news.objects.filter(status="approved").order_by('-last_updated', '-search_count').values('permalink', 'title', 'content', 'featured_image', 'last_updated')[:12]), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'News', 'link': "/news"}], 'metadata': {"og_description": "Find out about the newest health, medical, and drug news every day at RxZee. You can sign up by email.", "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": "https://rxzee.com/news"}})
##################### NEWS Pages Ends Here #######################

##################### Contact Us Pages Starts Here #####################
def contactUs(request):
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
    form = AwsDynamoDb.ContactUsForm()
    success = False
    if request.method == 'POST':
        form = AwsDynamoDb.ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save()
            for file in request.FILES.getlist('file_upload'):
                AwsDynamoDb.ContactFile.objects.create(contact=contact, file=file)
            success = True
            form = AwsDynamoDb.ContactUsForm()
    return render(request, "contactus.html", {"title": "Contact Us", 'form': form, 'success': success, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Contact US', 'link': "/contactus"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
##################### Contact Us Pages Ends Here #######################

##################### Pages Starts Here #####################
def GlobalPages(request, slug):
    try:
        page_data = AwsDynamoDb.footer_page.objects.filter(permalink__iexact=slug).first() or AwsDynamoDb.header_page.objects.filter(permalink__iexact=slug).first() or False
        drug = AwsDynamoDb.drug.objects.filter(permalink__iexact = slug, status__iexact="approved").select_related('author').values('permalink', 'name', 'brand_name', 'generic_name', 'pronunciation', 'class_name',  'dosage_forms', 'availability', 'author__username', 'widgets', 'uses',  'side_effects', 'warnings', 'precautions', 'interactions', 'overdose',  'seo_title', 'seo_description', 'seo_keywords', 'permalink',  'status', 'last_updated', 'author__last_name', 'author__last_name').first() or False
        vitamins_and_supplement = AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink__iexact = slug, status__iexact="approved").values().first() or False
        if page_data:
            metadata = {"og_description": page_data.seo_description,"og_image": "https://rxzee.com/static/RxZee.svg", "og_url": f"https://rxzee.com/{page_data.permalink}"}
            return render(request, "pages.html", {'title': page_data.title, 'page_data': page_data, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': page_data.title, 'link': f"/{page_data.permalink}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
        elif drug:
            AwsDynamoDb.drug_search.objects.filter(permalink__iexact = drug.permalink).update(search_count=F('search_count') + 1)
            from random import randint as random_number
            generic_names = drug.get('generic_name', '').split(",") if drug['generic_name'] else []
            AwsDynamoDb.drug_search.objects.filter(permalink = slug).update(search_count=F('search_count') + 1)
            metadata = {"og_description": drug.seo_description, "og_image": "https://rxzee.com/static/RxZee.svg", "og_url": f"https://rxzee.com/{slug}"}
            return render(request, "drugSpecificPage.html", {"title": drug["name"], "drug": drug, 'generic_names': generic_names, "faqs": list(AwsDynamoDb.drugsFaq.objects.filter(drug=id).values('question', 'answer')), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Drugs', 'link': "/drugs"}, {'name': drug.get('name'), 'link': f"/{drug.get('permalink')}"}], 'id': random_number(1000, 9999), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
        elif vitamins_and_supplement:
            from random import randint as random_number
            AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink=slug).update(search_count=F('search_count') + 1)
            faqs = list(AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(vitaminsAndSupplement = slug).values('question', 'answer'))
            metadata = {
                    "og_description": vitamins_and_supplement.seo_description,
                    "og_image": "https://rxzee.com/static/RxZee.svg",
                    "og_url": f"https://rxzee.com/{slug}"}
            return render(request, "vitaminsAndSupplementsSpecificPage.html", {"title": vitamins_and_supplement["name"], "vitaminsAndSupplement": vitamins_and_supplement, "faqs": faqs, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': vitamins_and_supplement.get('name'), 'link': f"/{vitamins_and_supplement.get('permalink')}"}], 'id': random_number(1000, 9999), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
        else:
            raise Http404('404! NOT FOUND.')
    except:
        raise Http404('404! NOT FOUND.')
##################### Pages Ends Here #######################

##################### Pages Starts Here #####################
def Sitemap(request):
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
    well_being = [ "Aging Well", "Baby", "Birth Control", "Children's Health",  "Diet & Weight Management", "Fitness & Exercise", "Food & Recipes",  "Health & Balance", "Healthy Beauty", "Men's Health",  "Parenting", "Pet Health", "Pregnancy", "Sex & Relationships",  "Teen Health", "Women's Health"]
    # Had to be changed
    drugs =  [{"name": "A/B Otic", "id": "#"}, {"name": "Abacavir", "id": "#"}, {"name": "Abacavir and lamivudine", "id": "#"}, {"name": "Abacavir and Lamivudine Tablets", "id": "#"}, {"name": "Abacavir Oral Solution", "id": "#"}, {"name": "Abacavir Sulfate Tablets", "id": "#"}, {"name": "Abacavir, dolutegravir, and lamivudine", "id": "#"}, {"name": "Abacavir, Lamivudine and Zidovudine Tablets", "id": "#"}, {"name": "Abacavir, lamivudine, and zidovudine", "id": "#"}, {"name": "Abaloparatide", "id": "#"}, {"name": "Abametapir", "id": "#"}, {"name": "Abatacept", "id": "#"}, {"name": "Abatuss DMX", "id": "#"}, {"name": "Abavite", "id": "#"}, {"name": "Abbokinase", "id": "#"}, {"name": "Abciximab", "id": "#"}, {"name": "Abecma", "id": "#"}, {"name": "Abelcet", "id": "#"}, {"name": "Abemaciclib", "id": "#"}, {"name": "Abilify", "id": "#"}, {"name": "Abilify (Aripiprazole Intramuscular)", "id": "#"}, {"name": "Abilify Asimtufii", "id": "#"}, {"name": "Abilify Asimtufii injection", "id": "#"}, {"name": "Abilify Discmelt", "id": "#"}, {"name": "Abilify Maintena", "id": "#"}, {"name": "Abilify Maintena Prefilled Syringe injection", "id": "#"}, {"name": "Abilify Mycite", "id": "#"}, {"name": "Abilify MyCite Maintenance Kit oral with sensor", "id": "#"}, {"name": "Abilify MyCite Starter Kit oral with sensor", "id": "#"}, {"name": "Abiraterone", "id": "#"}, {"name": "Abiraterone Acetate", "id": "#"}, {"name": "Abiraterone and niraparib", "id": "#"}, {"name": "Abiraterone, micronized", "id": "#"}, {"name": "Ablavar", "id": "#"}, {"name": "Ablysinol", "id": "#"}, {"name": "AbobotulinumtoxinA", "id": "#"}, {"name": "Abraxane", "id": "#"}, {"name": "Abreva", "id": "#"}, {"name": "Abrilada", "id": "#"}, {"name": "Abrocitinib", "id": "#"}, {"name": "Abrysvo", "id": "#"}, {"name": "Absorbine Athletes Foot", "id": "#"}, {"name": "Absorbine Jr. Antifungal", "id": "#"}, {"name": "Absorica", "id": "#"}, {"name": "Absorica LD", "id": "#"}, {"name": "Abstral", "id": "#"}, {"name": "Abstral Sublingual Tablet", "id": "#"}, {"name": "Abilify Maintena", "id": "#"}, {"name": "Abilify Maintena Prefilled Syringe injection", "id": "#"}, {"name": "Abilify Mycite", "id": "#"}, {"name": "Abilify MyCite Maintenance Kit oral with sensor", "id": "#"}, {"name": "Abilify MyCite Starter Kit oral with sensor", "id": "#"}, {"name": "Abiraterone", "id": "#"}, {"name": "Abiraterone Acetate", "id": "#"}, {"name": "Abiraterone and niraparib", "id": "#"}, {"name": "Abiraterone, micronized", "id": "#"}, {"name": "Ablavar", "id": "#"}, {"name": "Ablysinol", "id": "#"}, {"name": "AbobotulinumtoxinA", "id": "#"}, {"name": "Abraxane", "id": "#"}, {"name": "Abreva", "id": "#"}, {"name": "Abrilada", "id": "#"}, {"name": "Abrocitinib", "id": "#"}, {"name": "Abrysvo", "id": "#"}, {"name": "Absorbine Athletes Foot", "id": "#"}, {"name": "Absorbine Jr. Antifungal", "id": "#"}, {"name": "Absorica", "id": "#"}, {"name": "Absorica LD", "id": "#"}, {"name": "Abstral", "id": "#"}, {"name": "Abstral Sublingual Tablet", "id": "#"}]
    vitamins = [{"name": "5-htp", "id": "#"}, {"name": "Activated charcoal", "id": "#"}, {"name": "Ashwagandha", "id": "#"}, {"name": "Astaxanthin", "id": "#"}, {"name": "Astragalus", "id": "#"}, {"name": "Berberine", "id": "#"}, {"name": "Biotin", "id": "#"}, {"name": "Bromelain", "id": "#"}, {"name": "Calcium", "id": "#"}, {"name": "Chlorella", "id": "#"}, {"name": "Chlorophyll", "id": "#"}, {"name": "Choline", "id": "#"}, {"name": "Chromium", "id": "#"}, {"name": "Coconut oil", "id": "#"}, {"name": "Cod liver oil", "id": "#"}, {"name": "Colloidal silver", "id": "#"}, {"name": "Conjugated linoleic acid", "id": "#"}, {"name": "Cordyceps", "id": "#"}, {"name": "Creatine", "id": "#"}, {"name": "Damiana", "id": "#"}, {"name": "Echinacea", "id": "#"}, {"name": "Emu oil", "id": "#"}, {"name": "Evening primrose oil", "id": "#"}, {"name": "Fenugreek", "id": "#"}, {"name": "Fish oil", "id": "#"}, {"name": "Folic acid", "id": "#"}, {"name": "Gamma-aminobutyric acid (GABA)", "id": "#"}, {"name": "Garlic", "id": "#"}, {"name": "Ginger", "id": "#"}, {"name": "Ginkgo", "id": "#"}, {"name": "Glucomannan", "id": "#"}, {"name": "Glutathione", "id": "#"}, {"name": "Gotu kola", "id": "#"}, {"name": "Holy basil", "id": "#"}, {"name": "Horny goat weed", "id": "#"}, {"name": "Hyaluronic acid", "id": "#"}, {"name": "Inositol", "id": "#"}, {"name": "Iodine", "id": "#"}, {"name": "Iron", "id": "#"}, {"name": "Krill oil", "id": "#"}, {"name": "L-arginine", "id": "#"}, {"name": "L-carnitine", "id": "#"}, {"name": "Lecithin", "id": "#"}, {"name": "Lemon balm", "id": "#"}, {"name": "Licorice", "id": "#"}, {"name": "Lutein", "id": "#"}, {"name": "Maca", "id": "#"}, {"name": "Magnesium", "id": "#"}, {"name": "Maritime pine", "id": "#"}, {"name": "Melatonin", "id": "#"}, {"name": "Moringa", "id": "#"}, {"name": "Oolong tea", "id": "#"}, {"name": "Phenylalanine", "id": "#"}, {"name": "Phosphatidylserine", "id": "#"}, {"name": "Potassium", "id": "#"}, {"name": "Progesterone", "id": "#"}, {"name": "Propolis", "id": "#"}, {"name": "Pu-erh tea", "id": "#"}, {"name": "Quercetin", "id": "#"}, {"name": "Raspberry ketone", "id": "#"}, {"name": "Rhodiola", "id": "#"}, {"name": "Royal jelly", "id": "#"}, {"name": "Saw palmetto", "id": "#"}, {"name": "Serrapeptase", "id": "#"}, {"name": "Slippery elm", "id": "#"}, {"name": "Taurine", "id": "#"}, {"name": "Tea tree oil", "id": "#"}, {"name": "Tribulus", "id": "#"}, {"name": "Valerian", "id": "#"}, {"name": "Vitamin A", "id": "#"}, {"name": "Vitamin D", "id": "#"}, {"name": "Vitamin E", "id": "#"}, {"name": "Whey protein", "id": "#"}, {"name": "Witch hazel", "id": "#"}, {"name": "Xylitol", "id": "#"}, {"name": "Yohimbe", "id": "#"}, {"name": "Zinc", "id": "#"}]
    # Had to be changed
    return render(request, "sitemap.html", {'title': 'Sitemap', 'well_being': well_being, 'drugs': drugs, 'vitamins': vitamins, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Sitemap', 'link': "/sitemap"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
##################### Pages Ends Here #######################

#################################################################################################################################################################
################################################################### Global Views Ends Here ######################################################################
#################################################################################################################################################################


######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################


#################################################################################################################################################################
################################################################### Admin Views Starts Here #####################################################################
#################################################################################################################################################################
##################### DashBoard #####################
def AdminLogin(request):
    if not request.user.is_superuser:
        error = ""
        if request.method == 'POST':
            user = authenticate(request, username = str(request.POST.get('username')), password = str(request.POST.get('password')))
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect("/"+ADMIN_PATH)
            else:
                error = "Invalid username or password, or you are not an admin."
        return render(request, "admin/login.html", {"error": error})
    else:
        return redirect("/"+ADMIN_PATH)
def DashBoard(request):
    if request.user.is_superuser:
        return render(request, "admin/dashboard.html", {"title": "Dashboard", 'HomePage': AwsDynamoDb.HomePage.objects.first(), "activeNav": "da", 'top_news': AwsDynamoDb.news.objects.order_by('-search_count').first(), 'news': list(AwsDynamoDb.news.objects.order_by('-search_count').values('permalink', 'title', 'featured_image')[1:5]), 'count': {'pills_count': AwsDynamoDb.pill.objects.count(), 'messages_count': AwsDynamoDb.contact.objects.count(), 'drug_count': AwsDynamoDb.drug.objects.count(), 'vitamins_count': AwsDynamoDb.vitaminsAndSupplement.objects.count()}, 'ADMIN_PATH': ADMIN_PATH})
    else:
        return redirect("/"+ADMIN_PATH+'login')
def EditHomePage(request):
    if request.user.is_superuser and request.method == "POST":
        if request.POST.get('type') == 'search_drug_conditions':
            AwsDynamoDb.HomePage.objects.filter(id = '1').update(search_drug_conditions = request.POST.get('value') in ['on', 'true', '1'])
        elif request.POST.get('type') == 'slider':
            AwsDynamoDb.HomePage.objects.filter(id = '1').update(slider = request.POST.get('value') in ['on', 'true', '1'])
        elif request.POST.get('type') == 'healthy_life':
            AwsDynamoDb.HomePage.objects.filter(id = '1').update(healthy_life = request.POST.get('value') in ['on', 'true', '1'])
        elif request.POST.get('type') == 'health_az':
            AwsDynamoDb.HomePage.objects.filter(id = '1').update(health_az = request.POST.get('value') in ['on', 'true', '1'])
        elif request.POST.get('type') == 'top_news':
            AwsDynamoDb.HomePage.objects.filter(id = '1').update(top_news = request.POST.get('value') in ['on', 'true', '1'])
        return redirect("/"+ADMIN_PATH)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Pages Views Starts Here #####################
def Pages(request, category):
    if request.user.is_superuser:
        if category == 'header':
            context = {"title": "Header Pages", "activeNav": "hpa", 'table_name': 'All Header Pages', 'allPages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'seo_description', 'last_updated', 'permalink')), 'ADMIN_PATH': ADMIN_PATH, 'category': category}
        elif category == 'footer':
            context = {"title": "Footer Pages", "activeNav": "fpa", 'table_name': 'All Footer Pages', 'allPages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'seo_description', 'last_updated', 'permalink')), 'ADMIN_PATH': ADMIN_PATH, 'category': category}
        else:
            return redirect('/'+ADMIN_PATH)
        return render(request, "admin/page.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddPages(request, category):
    if request.user.is_superuser:
        if category == 'header':
            context = {"title": "Add Header Pages", "activeNav": "hpa", 'form': AwsDynamoDb.HeaderPageForm(), 'ADMIN_PATH': ADMIN_PATH, 'category': category}
        elif category == 'footer':
            context = {"title": "Add Header Pages", "activeNav": "fpa", 'form': AwsDynamoDb.FooterPageForm(), 'ADMIN_PATH': ADMIN_PATH, 'category': category}
        else:
            return redirect('/'+ADMIN_PATH)
        if request.method == "POST":
            if category == 'header':
                context['form'] = AwsDynamoDb.HeaderPageForm(request.POST, request.FILES)
            elif category == 'footer':
                context['form'] = AwsDynamoDb.FooterPageForm(request.POST, request.FILES)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"pages/"+category)
        return render(request, "admin/addEditPage.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditPages(request, category, permalink):
    try:
        if category == 'header':
            data = get_object_or_404(AwsDynamoDb.header_page, permalink = permalink)
            context = {"title": "Edit Pages", "activeNav": "hpa", 'form': AwsDynamoDb.HeaderPageForm(instance = data), 'ADMIN_PATH': ADMIN_PATH}
        elif category == 'footer':
            data = get_object_or_404(AwsDynamoDb.footer_page, permalink = permalink)
            context = {"title": "Edit Pages", "activeNav": "fpa", 'form': AwsDynamoDb.FooterPageForm(instance = data), 'ADMIN_PATH': ADMIN_PATH}
        else:
            return redirect("/"+ADMIN_PATH)
    except:
        return redirect("/"+ADMIN_PATH)
    if request.user.is_superuser and context['form']:
        if request.method == "POST":
            if category == 'header':
                context['form'] = AwsDynamoDb.HeaderPageForm(request.POST, request.FILES, instance = data)
            elif category == 'footer':
                context['form'] = AwsDynamoDb.FooterPageForm(request.POST, request.FILES, instance = data)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"pages/"+category+"/"+permalink)
        return render(request, "admin/addEditPage.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeletePages(request, category, permalink):
    try:
        if category == 'header':
            AwsDynamoDb.header_page.objects.filter(permalink = permalink).delete()
        elif category == 'footer':
            AwsDynamoDb.footer_page.objects.filter(permalink = permalink).delete()
    except:
        return redirect("/"+ADMIN_PATH)
    return redirect("/"+ADMIN_PATH+"pages/"+category)
##################### Pages Views Ends Here #####################

##################### Drugs Views Starts Here #####################
def AllSearchDrugs(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.drug_search.objects.order_by('name').values('id', 'name', 'condition', 'generic_name', 'drug_class', 'permalink')), 500)
        page = request.GET.get('page')
        try:
            allDrugsData = paginator.page(page)
        except PageNotAnInteger:
            allDrugsData = paginator.page(1)
        except EmptyPage:
            allDrugsData = paginator.page(paginator.num_pages)
        context = {"title": "Drugs and Medication", "activeNav": "drs", "table_name": "All Registered Drugs", "data": allDrugsData.object_list, "page_obj": allDrugsData, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/drug_search/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddDrugsSearch(request):
    if request.user.is_superuser:
        context = { "title": "Add Drugs", "activeNav": "drs", "form": AwsDynamoDb.DrugSearchForm(), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['form']= AwsDynamoDb.DrugSearchForm(request.POST)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"drugs")
        return render(request, "admin/drug_search/addedit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditDrugsSearch(request, id):
    try:
        drug_data = AwsDynamoDb.drug_search.objects.filter(id = id).first()
    except:
        return redirect("/"+ADMIN_PATH+"drugs")
    if request.user.is_superuser:
        context = { "title": "Edit Drugs", "activeNav": "drs", "form": AwsDynamoDb.DrugSearchForm(instance = drug_data), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['form']= AwsDynamoDb.DrugSearchForm(request.POST, instance = drug_data)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"drugs/"+id)
        return render(request, "admin/drug_search/addedit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteDrugsSearch(request, id):
    try:
        AwsDynamoDb.drug_search.objects.filter(id = id).delete()
        return redirect("/"+ADMIN_PATH+"drugs/")
    except:
        return redirect("/"+ADMIN_PATH+"drugs/")
def AllDrugs(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.drug.objects.select_related('author').order_by('name').values('permalink', 'name', 'brand_name', 'generic_name', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allDrugsData = paginator.page(page)
        except PageNotAnInteger:
            allDrugsData = paginator.page(1)
        except EmptyPage:
            allDrugsData = paginator.page(paginator.num_pages)
        context = {"title": "Drugs", "activeNav": "dr", "table_name": "All Registered Drugs Articles", "data": allDrugsData.object_list, "page_obj": allDrugsData, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/drugs/drugsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddDrugs(request):
    if request.user.is_superuser:
        context = { "title": "Add Drugs", "activeNav": "dr", "form": AwsDynamoDb.DrugRichTextForm(), "error": "", 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            widgets = [f"widget{i}" for i in range(1, 4) if request.POST.get(f"widget{i}")]
            updated_data = {"name": request.POST.get("name", ''), "pronunciation": request.POST.get("pronunciation", ''), "generic_name": request.POST.get("generic_name", ''), "brand_name": request.POST.get("brand_name", ''), "class_name": request.POST.get("class_name", ''), "dosage_forms": request.POST.get("dosage_forms", ''), "availability": request.POST.get("availability", ''), "author": request.user, "widgets": ', '.join(widgets), "uses": request.POST.get("uses", ''), "status": request.POST.get("status", ''), "side_effects": request.POST.get("side_effects", ''), "warnings": request.POST.get("warnings", ''), "precautions": request.POST.get("precautions", ''), "interactions": request.POST.get("interactions", ''), "overdose": request.POST.get("overdose", ''), "seo_title": request.POST.get("seo_title", ''), "seo_description": request.POST.get("seo_description", ''), "seo_keywords": request.POST.get("seo_keywords", ''), "permalink": str(request.POST.get("permalink", ''))}
            try:
                AwsDynamoDb.drug.objects.create(**updated_data)
                return redirect("/"+ADMIN_PATH+"drugs")
            except Exception as e:
                context['form'] = AwsDynamoDb.DrugRichTextForm({'uses': updated_data['uses'],'warnings': updated_data['warnings'],'precautions': updated_data['precautions'],'overdose': updated_data['overdose'],'side_effects': updated_data['side_effects'],'interactions': updated_data['interactions']})
                context['widgets'] = widgets
                context['error'] = str(e)
        return render(request, "admin/drugs/addEditDrugs.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditDrugs(request, permalink):
    try:
        drugData = AwsDynamoDb.drug.objects.select_related('author').filter(permalink = permalink).values('permalink', 'name', 'brand_name', 'author__first_name', 'author__last_name', 'author__username', 'generic_name', 'pronunciation', 'class_name', 'dosage_forms', 'availability', 'author_id', 'widgets', 'uses', 'side_effects', 'warnings', 'precautions', 'interactions', 'overdose', 'seo_title', 'seo_description', 'seo_keywords',  'search_count', 'status', 'last_updated').first() or False
    except:
        return redirect("/"+ADMIN_PATH+"drugs")
    if request.user.is_superuser and drugData:
        author = {"name": drugData['author__first_name'] + " " + drugData['author__last_name'], "link": drugData['author__username']}
        normal_details = {"name": drugData.get('name'), "pronunciation": drugData.get('pronunciation'), "status" :drugData.get('status'), "generic_name": drugData.get('generic_name'), "brand_name": drugData.get('brand_name'), "class_name": drugData.get('class_name'), "dosage_forms": drugData.get('dosage_forms'), "author": drugData.get('author'), 'availability': drugData.get('availability')}
        form = AwsDynamoDb.DrugRichTextForm({'uses': drugData.get('uses'), 'side_effects': drugData.get('side_effects'), 'warnings': drugData.get('warnings'), 'precautions': drugData.get('precautions'), 'interactions': drugData.get('interactions'), 'overdose': drugData.get('overdose')})
        seo_context = {"seo_title": drugData.get('seo_title'), "seo_description": drugData.get('seo_description'), "seo_keywords": drugData.get('seo_keywords'), "seo_author": drugData.get('seo_author'), "permalink": drugData.get('permalink')}
        allFaqs = list(AwsDynamoDb.drugsFaq.objects.filter(drug = drugData.get('permalink')).values())
        context = { "title": "Edit Drugs", "activeNav": "dr", "normal_details": normal_details, "form": form, "seo_context": seo_context, "id": drugData.get("id"), "allFaqs": allFaqs, "widgets": str(drugData.get("widgets")).split(", "), "error": "", 'ADMIN_PATH': ADMIN_PATH, "author": author}
        if request.method == "POST":
            widgets = [f"widget{i}" for i in range(1, 4) if request.POST.get(f"widget{i}")]
            updated_data = {"name": request.POST.get("name", ''), "pronunciation": request.POST.get("pronunciation", ''), "generic_name": request.POST.get("generic_name", ''), "brand_name": request.POST.get("brand_name", ''), "class_name": request.POST.get("class_name", ''), "dosage_forms": request.POST.get("dosage_forms", ''), "availability": request.POST.get("availability", ''), "author": drugData.get('author_id'), "widgets": ', '.join(widgets), "uses": request.POST.get("uses", ''), "status": request.POST.get("status", ''), "side_effects": request.POST.get("side_effects", ''), "warnings": request.POST.get("warnings", ''), "precautions": request.POST.get("precautions", ''), "interactions": request.POST.get("interactions", ''), "overdose": request.POST.get("overdose", ''), "seo_title": request.POST.get("seo_title", ''), "seo_description": request.POST.get("seo_description", ''), "seo_keywords": request.POST.get("seo_keywords", ''), "permalink": str(request.POST.get("permalink", ''))}
            try:
                AwsDynamoDb.drug.objects.filter(permalink=permalink).update(**updated_data)
                return redirect("/" + ADMIN_PATH + "drugs/" + updated_data['permalink'])
            except Exception as e:
                context['normal_details'] = {key: updated_data[key] for key in normal_details}
                context['form'] = AwsDynamoDb.DrugRichTextForm({'uses': updated_data['uses'],'warnings': updated_data['warnings'],'precautions': updated_data['precautions'],'overdose': updated_data['overdose'],'side_effects': updated_data['side_effects'],'interactions': updated_data['interactions']})
                context['seo_context'] = {"seo_title": updated_data['seo_title'],"seo_description": updated_data['seo_description'],"seo_keywords": updated_data['seo_keywords'],"permalink": updated_data['permalink']}
                context['widgets'] = updated_data['widgets']
                context['error'] = str(e)
                return render(request, "admin/drugs/addEditDrugs.html", context)
        return render(request, "admin/drugs/addEditDrugs.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteDrugs(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.drug.objects.filter(permalink = permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"drugs")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddDrugFAQ(request):
    if request.user.is_superuser and request.method == "POST":
        try:
            drug = request.POST.get("drug", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            data = AwsDynamoDb.drugsFaq.objects.create(question = question, answer = answer, drug = AwsDynamoDb.drug.objects.get(permalink = drug))
            data.save()
            return redirect("/"+ADMIN_PATH+"drugs/"+drug)
        except:
            return redirect("/"+ADMIN_PATH+"drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditDrugFAQ(request, id):
    if request.user.is_superuser and request.method == "POST":
        try:
            drug = request.POST.get("drug", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            AwsDynamoDb.drugsFaq.objects.filter(id=id).update(question=question, answer=answer)
            return redirect("/"+ADMIN_PATH+"drugs/"+drug)
        except:
            return redirect("/"+ADMIN_PATH+"drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteDrugFAQ(request, id):
    if request.user.is_superuser:
        try:
            data = AwsDynamoDb.drugsFaq.objects.filter(id=id).first()
            drug = str(data.drug.permalink)
            data.delete()
            return redirect("/"+ADMIN_PATH+"drugs/"+drug)
        except:
            return redirect("/"+ADMIN_PATH+"drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Drugs Views Ends Here #####################

##################### Vitamins and Supplements Views Starts Here #####################  
def allVitaminsAndSupplements(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.vitaminsAndSupplement.objects.select_related('author').order_by('name').values('permalink', 'name', 'other_names', 'author__id', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allVitaminsAndSupplementsData = paginator.page(page)
        except PageNotAnInteger:
            allVitaminsAndSupplementsData = paginator.page(1)
        except EmptyPage:
            allVitaminsAndSupplementsData = paginator.page(paginator.num_pages)
        context = {"title": "Vitamins and Supplements", "activeNav": "vi", "table_name": "All Vitamins and Supplements", "data": allVitaminsAndSupplementsData.object_list, "page_obj": allVitaminsAndSupplementsData, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/vitamins/vitaminsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def addVitaminsAndSupplements(request):
    if request.user.is_superuser:
        context = { "title": "Add Vitamins and Supplements", "activeNav": "vi", "form": AwsDynamoDb.VitaminsAndSupplementsRichTextForm(), "error": "", 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            widgets = [f"widget{i}" for i in range(1, 4) if request.POST.get(f"widget{i}")]
            name = request.POST.get("name", '')
            other_names = request.POST.get("other_names", '')
            widgets = ', '.join(widgets)
            author = request.user
            overview = request.POST.get("overview", '')
            uses = request.POST.get("uses", '')
            status = request.POST.get("status", '')
            side_effects = request.POST.get("side_effects", '')
            precautions = request.POST.get("precautions", '')
            interactions = request.POST.get("interactions", '')
            dosing = request.POST.get("dosing", '')
            seo_title = request.POST.get("seo_title", '')
            seo_keywords = request.POST.get("seo_keywords", '')
            seo_description = request.POST.get("seo_description", '')
            permalink = request.POST.get("permalink", '')
            try:
                AwsDynamoDb.vitaminsAndSupplement.objects.create(name=name, other_names=other_names, status=status, author=author, widgets=widgets, overview=overview, uses=uses, dosing=dosing, side_effects=side_effects, interactions=interactions, precautions=precautions, seo_title=seo_title, seo_keywords=seo_keywords, seo_description=seo_description, permalink=permalink)
                return redirect("/"+ADMIN_PATH+"vitamins")
            except Exception as e:
                context['normal_details'] = {"name": name, "other_names": other_names, 'author': author, "status": status}
                context['form'] = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': overview, 'uses': uses, 'side_effects': side_effects, 'precautions': precautions, 'interactions': interactions, 'dosing': dosing})
                context['seo_context'] = {"seo_title": seo_title, "seo_description": seo_description, "seo_keywords": seo_keywords, "permalink": permalink}
                context['widgets'] = widgets
                context['error'] = str(e)
        return render(request, "admin/vitamins/addEditVitamins.html",context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def editVitaminsAndSupplements(request, permalink):
    try:
        vitaminsAndSupplementsData = AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink=permalink).values().first()
        if not vitaminsAndSupplementsData:
            return redirect("/" + ADMIN_PATH + "vitaminsandsupplements")
    except Exception as e:
        return redirect("/" + ADMIN_PATH + "vitaminsandsupplements")
    if request.user.is_superuser:
        author = AwsDynamoDb.User.objects.get(id=vitaminsAndSupplementsData['author_id'])
        author_info = {"name": f"{author.first_name} {author.last_name}", "link": author.username}
        normal_details = {"name": vitaminsAndSupplementsData.get('name'), "other_names": vitaminsAndSupplementsData.get('other_names'), 'status': vitaminsAndSupplementsData.get('status')}
        form = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': vitaminsAndSupplementsData.get('overview'), 'uses': vitaminsAndSupplementsData.get('uses'), 'side_effects': vitaminsAndSupplementsData.get('side_effects'), 'interactions': vitaminsAndSupplementsData.get('interactions'), 'precautions': vitaminsAndSupplementsData.get('precautions'), 'dosing': vitaminsAndSupplementsData.get('dosing')})
        seo_context = {"seo_title": vitaminsAndSupplementsData.get('seo_title'), "seo_description": vitaminsAndSupplementsData.get('seo_description'), "seo_keywords": vitaminsAndSupplementsData.get('seo_keywords'), "permalink": vitaminsAndSupplementsData.get('permalink')}
        allFaqs = list(AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(vitaminsAndSupplement=vitaminsAndSupplementsData.get('permalink')).values())
        context = {"title": "Edit Vitamins and Supplements", "activeNav": "vi", "normal_details": normal_details, "form": form, "seo_context": seo_context, "id": vitaminsAndSupplementsData.get("id"), "allFaqs": allFaqs, "widgets": str(vitaminsAndSupplementsData.get("widgets")).split(", "), "error": "", 'ADMIN_PATH': ADMIN_PATH, "author": author_info}
        if request.method == "POST":
            widgets = [f"widget{i}" for i in range(1, 4) if request.POST.get(f"widget{i}")]
            widgets_str = ', '.join(widgets)
            updated_data = {"name": request.POST.get("name", ''), "other_names": request.POST.get("other_names", ''), "status": request.POST.get("status", ''), "widgets": widgets_str, "overview": request.POST.get("overview", ''), "uses": request.POST.get("uses", ''), "side_effects": request.POST.get("side_effects", ''), "precautions": request.POST.get("precautions", ''), "interactions": request.POST.get("interactions", ''), "dosing": request.POST.get("dosing", ''), "seo_title": request.POST.get("seo_title", ''), "seo_keywords": request.POST.get("seo_keywords", ''), "seo_description": request.POST.get("seo_description", ''), "permalink": permalink}
            try:
                AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink=permalink).update(**updated_data)
                return redirect("/" + ADMIN_PATH + "vitamins/" + permalink)
            except Exception as e:
                context['normal_details'] = {"name": updated_data['name'], "other_names": updated_data['other_names'], "status": updated_data['status']}
                context['form'] = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': updated_data['overview'], 'uses': updated_data['uses'], 'side_effects': updated_data['side_effects'], 'precautions': updated_data['precautions'], 'interactions': updated_data['interactions'], 'dosing': updated_data['dosing']})
                context['seo_context'] = {"seo_title": updated_data['seo_title'], "seo_description": updated_data['seo_description'], "seo_keywords": updated_data['seo_keywords'], "permalink": permalink}
                context['widgets'] = widgets_str
                context['error'] = str(e)
        return render(request, "admin/vitamins/addEditVitamins.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def deleteVitaminsAndSupplements(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink=permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"vitamins")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddVitaminsAndSupplementsFAQ(request):
    if request.user.is_superuser and request.method == "POST":
        try:
            vitaminsAndSupplements = request.POST.get("vitaminsandsupplements", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            data = AwsDynamoDb.vitaminsAndSupplementsFaq.objects.create(question = question, answer = answer, vitaminsAndSupplement = AwsDynamoDb.vitaminsAndSupplement.objects.get(permalink = vitaminsAndSupplements))
            data.save()
            return redirect("/"+ADMIN_PATH+"vitamins/"+vitaminsAndSupplements)
        except:
            return redirect("/"+ADMIN_PATH+"vitamins/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditVitaminsAndSupplementsFAQ(request, id):
    if request.user.is_superuser and request.method == "POST":
        try:
            vitaminsAndSupplements = request.POST.get("vitaminsandsupplements", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(id=id).update(question=question, answer=answer)
            return redirect("/"+ADMIN_PATH+"vitamins/"+vitaminsAndSupplements)
        except:
            return redirect("/"+ADMIN_PATH+"vitamins/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteVitaminsAndSupplementsFAQ(request, id):
    if request.user.is_superuser:
        try:
            data = AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(id = id).first()
            vitaminsAndSupplement = str(data.vitaminsAndSupplement.permalink)
            data.delete()
            return redirect("/"+ADMIN_PATH+"vitamins/"+vitaminsAndSupplement)
        except:
            return redirect("/"+ADMIN_PATH+"vitamins/")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Vitamins and Supplements Views Ends Here #######################

##################### Allergies Views Starts Here #####################
def AllAllergies(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.allergies.objects.select_related('author').order_by('name').values('permalink', 'name', 'status', 'author__first_name', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allergies = paginator.page(page)
        except PageNotAnInteger:
            allergies = paginator.page(1)
        except EmptyPage:
            allergies = paginator.page(paginator.num_pages)
        context = {"title": "All Allergies", "activeNav": "al", 'table_name': 'All Allergies', 'allergies': allergies.object_list, 'page_obj': allergies, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/allergies/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddAllergies(request):
    if request.user.is_superuser:
        context = {"title": "Add Allergies", "activeNav": "al", 'form': AwsDynamoDb.AllergiesForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AllergiesForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"allergies")
        return render(request, "admin/allergies/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditAllergies(request, permalink):
    try:
        pillData = get_object_or_404(AwsDynamoDb.allergies, permalink = permalink)
    except:
        return redirect("/"+ADMIN_PATH+"allergies")
    if request.user.is_superuser and pillData:
        author = AwsDynamoDb.User.objects.get(id = pillData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Allergies", "activeNav": "al", 'form': AwsDynamoDb.AllergiesForm(instance = pillData), "author": pillData.author, 'ADMIN_PATH': ADMIN_PATH, "author": author}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.AllergiesForm(request.POST, request.FILES, instance = pillData)
            if context['form'].is_valid():
                AwsDynamoDb.allergies.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"allergies/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "admin/allergies/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteAllergies(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.allergies.objects.filter(permalink = permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"allergies")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Allergies Views Ends Here #######################

##################### Interaction Checker Views Starts Here #####################
def AllInteractions(request):
    if request.user.is_superuser:
        if 'drug' in request.path:
            columns = ['First Drug', 'Second Drug', 'Interaction Type', 'Author', 'Status', 'Last Updated']
            table_name = 'All Drug Interactions'
            activeNav = 'drin'
            paginator = Paginator(list(AwsDynamoDb.drug_interactions.objects.select_related('author').order_by('-last_updated').values('id', 'first_drug', 'second_drug', 'level', 'status', 'last_updated', 'author__first_name')), 500)
        elif 'food' in request.path:
            columns = ['Formula', 'Header', 'Severity', 'Interaction Level', 'Author', 'Status', 'Last Updated']
            table_name = 'All Food Interactions'
            activeNav = 'fin'
            paginator = Paginator(list(AwsDynamoDb.food_interactions.objects.select_related('author').order_by('-last_updated').values('id', 'formula', 'header', 'severity', 'level', 'author__first_name', 'status', 'last_updated')), 500)
        elif 'disease' in request.path:
            columns = ['Formula', 'Header', 'Severity', 'Interaction Level', 'Author', 'Status', 'Last Updated']
            table_name = 'All Disease Interactions'
            activeNav = 'din'
            paginator = Paginator(list(AwsDynamoDb.disease_interactions.objects.select_related('author').order_by('-last_updated').values('id', 'formula', 'header', 'severity', 'level', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allInteractions = paginator.page(page)
        except PageNotAnInteger:
            allInteractions = paginator.page(1)
        except EmptyPage:
            allInteractions = paginator.page(paginator.num_pages)
        context = {"title": "Interaction Checker", "activeNav": activeNav, "table_name": table_name, "columns": columns, "data": allInteractions.object_list, 'page_obj': allInteractions, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/interaction/interactionsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddInteractions(request):
    if request.user.is_superuser:
        if 'drug' in request.path:
            context = { "title": "Add Drug Interactions", "activeNav": 'drin', "form": AwsDynamoDb.DrugInteractionsForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        elif 'food' in request.path:
            context = { "title": "Add Food Interactions", "activeNav": 'fin', "form": AwsDynamoDb.FoodInteractionsForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        elif 'disease' in request.path:
            context = { "title": "Add Disease Interactions", "activeNav": 'din', "form": AwsDynamoDb.DiseaseInteractionsForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            if 'drug' in request.path:
                context['form'] = AwsDynamoDb.DrugInteractionsForm(request.POST, author=request.user)
            elif 'food' in request.path:
                context['form'] = AwsDynamoDb.FoodInteractionsForm(request.POST, author=request.user)
            elif 'disease' in request.path:
                context['form'] = AwsDynamoDb.DiseaseInteractionsForm(request.POST, author=request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect(request.path[:-4])
        return render(request, "admin/interaction/addEditinteractions.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditInteractions(request, id):
    try:
        if 'drug' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "drin", "form": AwsDynamoDb.DrugInteractionsForm(instance = get_object_or_404(AwsDynamoDb.drug_interactions, id = id)), 'ADMIN_PATH': ADMIN_PATH}
        elif 'food' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "fin", "form": AwsDynamoDb.FoodInteractionsForm(instance = get_object_or_404(AwsDynamoDb.food_interactions, id = id)), 'ADMIN_PATH': ADMIN_PATH}
        elif 'disease' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "din", "form": AwsDynamoDb.DiseaseInteractionsForm(instance = get_object_or_404(AwsDynamoDb.disease_interactions, id = id)), 'ADMIN_PATH': ADMIN_PATH}
    except:
        return redirect(request.path)
    if request.user.is_superuser:
        if request.method == "POST":
            if 'drug' in request.path:
                context['form'] = AwsDynamoDb.DrugInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.drug_interactions, id = id))
            elif 'food' in request.path:
                context['form'] = AwsDynamoDb.FoodInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.food_interactions, id = id))
            elif 'disease' in request.path:
                context['form'] = AwsDynamoDb.DiseaseInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.disease_interactions, id = id))
            if context['form'].is_valid():
                context['form'].save()
                return redirect(request.path)
        return render(request, "admin/interaction/addEditinteractions.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteInteractions(request, id):
    if request.user.is_superuser:
        try:
            if 'drug' in request.path:
                AwsDynamoDb.drug_interactions.objects.filter(id=id).delete()
            elif 'food' in request.path:
                AwsDynamoDb.food_interactions.objects.filter(id=id).delete()
            elif 'disease' in request.path:
                AwsDynamoDb.disease_interactions.objects.filter(id=id).delete()
        except:
            pass
        return redirect('/'.join(request.path.split('/')[:-3]))
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Interaction Checker Views Ends Here #######################

##################### Pill Identification Views Starts Here #####################
def AllPillIdentification(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.pill.objects.select_related('author').order_by('name').values('id', 'name', 'generic_name', 'imprint_side_1', 'imprint_side_2', 'status', 'author__first_name', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allPills = paginator.page(page)
        except PageNotAnInteger:
            allPills = paginator.page(1)
        except EmptyPage:
            allPills = paginator.page(paginator.num_pages)
        context = {"title": "Pill Identification", "activeNav": "pi", 'table_name': 'All Pills Registered', 'allPills': allPills.object_list, 'page_obj': allPills, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/pillIdentification/pillIdentificationTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddPillIdentification(request):
    if request.user.is_superuser:
        context = {"title": "Add Pills for Identification", "activeNav": "pi", 'form': AwsDynamoDb.PillForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.PillForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"pillidentification")
        return render(request, "admin/pillIdentification/addEditpill.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditPillIdentification(request, id):
    try:
        pillData = get_object_or_404(AwsDynamoDb.pill, id = id)
    except:
        return redirect("/"+ADMIN_PATH+"pillidentification")
    if request.user.is_superuser and pillData:
        author = AwsDynamoDb.User.objects.get(id = pillData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Pills for Identification", "activeNav": "pi", 'form': AwsDynamoDb.PillForm(instance = pillData), "author": pillData.author, 'ADMIN_PATH': ADMIN_PATH, "author": author}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.PillForm(request.POST, request.FILES, instance = pillData)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"pillidentification/"+id)
        return render(request, "admin/pillIdentification/addEditpill.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeletePillIdentification(request, id):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.pill.objects.filter(id = id).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"pillidentification")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Pill Identification Views Ends Here #######################

##################### NEWS Views Starts Here #####################
def AllNEWS(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.news.objects.select_related('author').order_by('-last_updated').values('permalink', 'title', 'category', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allNews = paginator.page(page)
        except PageNotAnInteger:
            allNews = paginator.page(1)
        except EmptyPage:
            allNews = paginator.page(paginator.num_pages)
        context = {"title": "NEWS", "activeNav": "ne", 'table_name': 'All NEWS', 'allNews': allNews.object_list, "page_obj": allNews, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/news/newsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddNEWS(request):
    if request.user.is_superuser:
        context = {"title": "Write NEWS", "activeNav": "ne", 'form': AwsDynamoDb.NewsForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.NewsForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"news")
        return render(request, "admin/news/addEditNEWS.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditNEWS(request, permalink):
    try:
        newsData = get_object_or_404(AwsDynamoDb.news, permalink = permalink)
    except:
        return redirect("/"+ADMIN_PATH+"news")
    if request.user.is_superuser and newsData:
        author = AwsDynamoDb.User.objects.get(id = newsData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit NEWS", "activeNav": "ne", 'form': AwsDynamoDb.NewsForm(instance = newsData), "author": author, 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.NewsForm(request.POST, request.FILES, instance = newsData)
            if context['form'].is_valid():
                AwsDynamoDb.news.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"news/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "admin/news/addEditNEWS.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteNEWS(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.news.objects.filter(permalink = permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"news")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### NEWS Views Ends Here #######################

##################### Conditions Views Starts Here #####################
def AllConditions(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.condition.objects.select_related('author').order_by('-last_updated').values('permalink', 'heading', 'category', 'author__first_name', 'status', 'last_updated', 'permalink')), 500)
        page = request.GET.get('page')
        try:
            allConditions = paginator.page(page)
        except PageNotAnInteger:
            allConditions = paginator.page(1)
        except EmptyPage:
            allConditions = paginator.page(paginator.num_pages)
        context = {"title": "Conditions", "activeNav": "con", 'table_name': 'All Conditions', 'allConditions': allConditions.object_list, "page_obj": allConditions, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/conditions/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddConditions(request):
    if request.user.is_superuser:
        context = {"title": "Write Conditions", "activeNav": "con", 'form': AwsDynamoDb.ConditionsForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.ConditionsForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"conditions")
        return render(request, "admin/conditions/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditConditions(request, permalink):
    try:
        conditionData = get_object_or_404(AwsDynamoDb.condition, permalink = permalink)
    except:
        return redirect("/"+ADMIN_PATH+"conditions")
    if request.user.is_superuser and conditionData:
        author = AwsDynamoDb.User.objects.get(id = conditionData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Conditions", "activeNav": "con", 'form': AwsDynamoDb.ConditionsForm(instance = conditionData), 'addconditionform': AwsDynamoDb.ConditionForm, "author": author, 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.ConditionsForm(request.POST, request.FILES, instance = conditionData)
            if context['form'].is_valid():
                context['form'].save()
                AwsDynamoDb.condition.objects.filter(permalink = permalink).delete()
                return redirect("/"+ADMIN_PATH+"conditions/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "admin/conditions/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteConditions(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.condition.objects.filter(permalink = permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"conditions")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Conditions Views Ends Here #######################

##################### Well Being Views Starts Here #####################
def AllWellBeing(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.well_being.objects.select_related('author').order_by('-last_updated').values('permalink', 'title', 'category', 'author__first_name', 'status', 'last_updated', 'permalink')), 500)
        page = request.GET.get('page')
        try:
            allWellBeing = paginator.page(page)
        except PageNotAnInteger:
            allWellBeing = paginator.page(1)
        except EmptyPage:
            allWellBeing = paginator.page(paginator.num_pages)
        context = {"title": "Well Being", "activeNav": "we", 'table_name': 'All WellBeing', 'allWellBeing': allWellBeing.object_list, "page_obj": allWellBeing, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/wellbeing/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddWellBeing(request):
    if request.user.is_superuser:
        context = {"title": "Write Well Being", "activeNav": "we", 'form': AwsDynamoDb.WellBeingForm(author = request.user), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.WellBeingForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"wellbeing")
        return render(request, "admin/wellbeing/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditWellBeing(request, permalink):
    try:
        wellbeingData = get_object_or_404(AwsDynamoDb.well_being, permalink = permalink)
    except:
        return redirect("/"+ADMIN_PATH+"wellbeing")
    if request.user.is_superuser and wellbeingData:
        author = AwsDynamoDb.User.objects.get(id = wellbeingData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Well Being", "activeNav": "we", 'form': AwsDynamoDb.WellBeingForm(instance = wellbeingData), "author": author, 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.WellBeingForm(request.POST, request.FILES, instance = wellbeingData)
            if context['form'].is_valid():
                context['form'].save()
                AwsDynamoDb.well_being.objects.filter(permalink = permalink).delete()
                return redirect("/"+ADMIN_PATH+"wellbeing/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "admin/wellbeing/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteWellBeing(request, permalink):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.well_being.objects.filter(permalink = permalink).delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"wellbeing")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Well Being Views Ends Here #######################


##################### Writers Views Starts Here #####################
def AllWriter(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.User.objects.filter(category = 'author').order_by('-first_name').values()), 500)
        page = request.GET.get('page')
        try:
            allWriters = paginator.page(page)
        except PageNotAnInteger:
            allWriters = paginator.page(1)
        except EmptyPage:
            allWriters = paginator.page(paginator.num_pages)
        context = {"title": "Writer", "activeNav": "wr", 'table_name': 'All Writers', 'allWriters': allWriters.object_list, "page_obj": allWriters, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/writer/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AddWriter(request):
    if request.user.is_superuser:
        context = {"title": "Add Writer", "activeNav": "wr", 'form': AwsDynamoDb.AuthorForm(), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorForm(request.POST, request.FILES)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"writer")
        return render(request, "admin/writer/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def EditWriter(request, id):
    try:
        writerData = get_object_or_404(AwsDynamoDb.User, id = id)
    except:
        return redirect("/"+ADMIN_PATH+"news")
    if request.user.is_superuser:
        context = {"title": "Edit Writer", "activeNav": "wr", 'form': AwsDynamoDb.AuthorForm(instance = writerData), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.AuthorForm(request.POST, request.FILES, instance = writerData)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/"+ADMIN_PATH+"writer/"+id)
        return render(request, "admin/writer/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteWriter(request, id):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.User.objects.filter(id = id, category = "author").delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"writer")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Writers Views Ends Here #######################

##################### Users Views Starts Here #####################
def AllUsers(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.User.objects.filter(category = 'user').order_by('-first_name').values()), 500)
        page = request.GET.get('page')
        try:
            allUsers = paginator.page(page)
        except PageNotAnInteger:
            allUsers = paginator.page(1)
        except EmptyPage:
            allUsers = paginator.page(paginator.num_pages)
        context = {"title": "Users", "activeNav": "us", 'allUsers': allUsers.object_list, "page_obj": allUsers, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/users.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def ViewUser(request, id):
    try:
        user = AwsDynamoDb.User.objects.filter(id = id).first()
    except:
        return redirect("/"+ADMIN_PATH+"users")
    if request.user.is_superuser and user:
        return render(request, "admin/user.html", {"title": "Users", "activeNav": "us", 'user': user, 'ADMIN_PATH': ADMIN_PATH})
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def DeleteUser(request, id):
    if request.user.is_superuser:
        try:
            AwsDynamoDb.User.objects.filter(id = id, category = "user").delete()
        except:
            pass
        return redirect("/"+ADMIN_PATH+"users")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Users Views Ends Here #######################

##################### Contact Us Views Starts Here #####################
def ContactUsMessages(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.contact.objects.all().order_by('-last_updated').values('id', 'subject', 'email', 'fullname', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allMessagesData = paginator.page(page)
        except PageNotAnInteger:
            allMessagesData = paginator.page(1)
        except EmptyPage:
            allMessagesData = paginator.page(paginator.num_pages)
        context = {"title": "Contact Us", "activeNav": "co", "table_name": "All Contact Messages", "data": allMessagesData.object_list, 'page_obj': allMessagesData, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/contactus/index.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def SpecificContactMessage(request, id):
    if request.user.is_superuser:
        try:
            message = AwsDynamoDb.contact.objects.filter(id = id).values().first()
            allFiles = list(AwsDynamoDb.ContactFile.objects.filter(contact = id).values_list('file', flat = True))
        except:
            return redirect("/"+ADMIN_PATH+"contactus")
        context = {"title": "Specific Contact Us", "activeNav": "co", 'message': message, 'allFiles': allFiles, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/contactus/specificDrug.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Contact Us Views Ends Here #######################

##################### Sessions Views Starts Here #####################
def Sessions(request):
    if request.user.is_superuser:
        paginator = Paginator(list(AwsDynamoDb.UserSession.objects.order_by('-is_active').select_related('author').values('user__first_name', 'user__last_name', 'user__username', 'user__category', 'is_active', 'ip_address', 'country', 'region', 'session_key')), 500)
        page = request.GET.get('page')
        try:
            allSessions = paginator.page(page)
        except PageNotAnInteger:
            allSessions = paginator.page(1)
        except EmptyPage:
            allSessions = paginator.page(paginator.num_pages)
        context = {"title": "Sessions", "activeNav": "ses", 'allSessions': allSessions.object_list, "page_obj": allSessions, 'ADMIN_PATH': ADMIN_PATH}
        return render(request, "admin/sessions.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def Session(request, session_key):
    try:
        session = AwsDynamoDb.UserSession.objects.filter(session_key = session_key).select_related('author').values('user__first_name', 'user__last_name', 'user__username', 'user__email', 'user__last_login', 'user__category', 'session_key', 'ip_address', 'country', 'region', 'city', 'zip_code', 'user_agent', 'session_expiration', 'is_active').first()
    except:
        return redirect("/"+ADMIN_PATH+"sessions")
    if request.user.is_superuser and session:
        return render(request, "admin/session.html", {"title": "Session", "activeNav": "ses", "session": session, 'ADMIN_PATH': ADMIN_PATH})
    else:
        return redirect("/"+ADMIN_PATH+"sessions")
##################### Sessions Views Starts Here #####################

##################### Settings Views Starts Here #####################
def AdminSettings(request):
    if request.user.is_superuser:
        context = {"title": "Settings", "activeNav": "se", 'ChangePasswordForm': AwsDynamoDb.ChangePasswordForm, 'ChangeSocialsForm': AwsDynamoDb.ChangeSocialsForm(instance = AwsDynamoDb.HomePage.objects.first()), 'ADMIN_PATH': ADMIN_PATH}
        if request.method == "POST":
            context['ChangePasswordForm'] = AwsDynamoDb.ChangePasswordForm(user=request.user, data=request.POST)
            if context['ChangePasswordForm'].is_valid():
                from django.contrib.auth import update_session_auth_hash
                new_password = context['ChangePasswordForm'].cleaned_data['new_password']
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect("/"+ADMIN_PATH)
        return render(request, "admin/settings.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def ChangeGoogleTagId(request):
    if request.method == 'POST' and request.user.is_superuser:
        form = AwsDynamoDb.ChangeSocialsForm(request.POST, instance = AwsDynamoDb.HomePage.objects.first())
        if form.is_valid():
            form.save()
    return redirect("/"+ADMIN_PATH+"settings")
def force_logout(request, session_key):
    if request.user.is_superuser:
        try:
            user_session = AwsDynamoDb.UserSession.objects.get(session_key = session_key)
            user_session.is_active = False
            user_session.save()
        except AwsDynamoDb.UserSession.DoesNotExist:
            pass
        return redirect("/"+ADMIN_PATH+"sessions")
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
##################### Settings Views Ends Here #######################

#################################################################################################################################################################
################################################################### Admin Views Ends Here #######################################################################
#################################################################################################################################################################


######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################


#################################################################################################################################################################
################################################################### User Views Starts User Profile Here #########################################################
#################################################################################################################################################################
def UserProfiles(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        return render(request, "user/profiles/profiles.html", {"title": "User Profiles", 'all_profiles': list(AwsDynamoDb.UserProfile.objects.filter(user = request.user).order_by('-last_updated').values('id', 'profile_name')), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Profile', 'link': "/user/profiles"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')
def UserProfilesAdd(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        context = {"title": "View User Profiles", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Profile', 'link': "/user/profiles"}, {'name': 'Add Profile', 'link': "/user/profiles/add"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), "error": "", 'metadata': metadata}
        if request.method == "POST":
            UserProfileData = {"profile_name": request.POST.get("profile_name"), "pregnancy_lactation_warnings": request.POST.get("pregnancy_lactation_warnings") == "enabled", "emergency_contact_contact_name": request.POST.get("emergency_contact_contact_name"), "emergency_contact_contact_phone_number": request.POST.get("emergency_contact_contact_phone_number"), "primary_physician_contact_name": request.POST.get("primary_physician_contact_name"), "primary_physician_contact_phone_number": request.POST.get("primary_physician_contact_phone_number"), "other_details": request.POST.get("other_details"), "user": request.user}
            if UserProfileData["profile_name"]:
                try:
                    AwsDynamoDb.UserProfile.objects.create(**UserProfileData)
                    return redirect('/user/profiles/')
                except Exception as e:
                    context["error"] = str(e)
            else:
                context["error"] = "Please provide a name to profile."
        return render(request, "user/profiles/addeditprofile.html", context)
    else:
        return redirect('/signin')
def UserProfilesView(request, id):
    try:
        profile = AwsDynamoDb.UserProfile.objects.filter(id = id, user = request.user).first()
    except:
        return redirect('/user/profiles')
    if request.user.is_authenticated and request.user.category == 'user' and profile:
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        return render(request, "user/profiles/profile.html", {"title": "User Profiles", 'profile': profile, 'count': {'drugs_count': AwsDynamoDb.UserProfileDrugs.objects.filter(user_profile = profile, user = request.user).count(), 'conditions_count': AwsDynamoDb.UserProfileConditions.objects.filter(user_profile = profile, user = request.user).count(), 'allergies_count': AwsDynamoDb.UserProfileAllergies.objects.filter(user_profile = profile, user = request.user).count(), 'reports_count': 2, 'reminder_count': AwsDynamoDb.UserProfileReminder.objects.filter(user_profile = profile, user = request.user).count(), 'notes_count': AwsDynamoDb.UserProfileNotes.objects.filter(user_profile = profile, user = request.user).count()}, 'profile_len': AwsDynamoDb.UserProfile.objects.filter(user = request.user).count(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': profile.profile_name, 'link': f"/user/profiles/{profile.id}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')
def UserProfilesEdit(request, id):
    UserProfileData = AwsDynamoDb.UserProfile.objects.filter(id = id).first() or None
    if request.user.is_authenticated and request.user.category == 'user' and UserProfileData:
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        context = {"title": "View User Profiles", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Profile', 'link': "/user/profiles"}, {'name': 'Edit Profile', 'link': f"/user/profiles/edit/{id}"}], "UserProfileData": UserProfileData, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), "error": "", 'metadata': metadata}
        if request.method == "POST":
            UserProfileData = {"profile_name": request.POST.get("profile_name"), "pregnancy_lactation_warnings": request.POST.get("pregnancy_lactation_warnings") == "enabled", "emergency_contact_contact_name": request.POST.get("emergency_contact_contact_name"), "emergency_contact_contact_phone_number": request.POST.get("emergency_contact_contact_phone_number"), "primary_physician_contact_name": request.POST.get("primary_physician_contact_name"), "primary_physician_contact_phone_number": request.POST.get("primary_physician_contact_phone_number"), "other_details": request.POST.get("other_details"), "user": request.user}
            if UserProfileData["profile_name"]:
                try:
                    AwsDynamoDb.UserProfile.objects.filter(id = id).update(**UserProfileData)
                    return redirect(f'/user/profiles/edit/{id}')
                except Exception as e:
                    context["error"] = str(e)
            else:
                context["error"] = "Please provide a name to profile."
        return render(request, "user/profiles/addeditprofile.html", context)
    else:
        return redirect('/signin')
def UserProfilesDelete(request, id):
    if request.user.is_authenticated and request.user.category == 'user':
        try:
            AwsDynamoDb.UserProfile.objects.filter(id = id).delete()
        except:
            pass
        return redirect('/user/profiles/')
    else:
        return redirect('/signin')
def UserProfilesViewItem(request, id, category):
    get_model_name = {'drugs': AwsDynamoDb.UserProfileDrugs, 'conditions': AwsDynamoDb.UserProfileConditions, 'reports': AwsDynamoDb.UserProfileConditions, 'allergies': AwsDynamoDb.UserProfileAllergies, 'reminder': AwsDynamoDb.UserProfileReminder, 'notes': AwsDynamoDb.UserProfileNotes}
    get_category_heading = {'drugs': 'Add your first drug', 'conditions': 'Conditions', 'reports': 'Interactions Report', 'allergies': 'Allergies', 'reminder': 'Manage your meds', 'notes': 'Notes'}
    get_category_text = {'drugs': 'You can start keeping track of your medications by adding them to your profile. Get to conversations, warnings, and alerts right away.', 'conditions': 'To help build your health record, add symptoms to your background. Find out more about these conditions and the medicines that can help you.', 'reports': 'The medicines in your profile did not mix with each other. This doesn&apos;t always mean that there are no encounters. Always talk to your doctor or nurse.', 'allergies': 'You can see alerts when one of your drugs might cause an allergic reaction after adding them to your profile.', 'reminder': 'Add all of your medicines and be reminded every time to take them.', 'notes': 'You can make a timeline of medical events (appointments, accidents, surgeries, etc.) by adding notes to your profile.'}
    try:
        if category in ['drugs', 'conditions', 'reports', 'allergies', 'reminder', 'notes']:
            profile = AwsDynamoDb.UserProfile.objects.filter(id = id, user = request.user).only('id', 'profile_name').first()
            data = get_model_name[category].objects.filter(user_profile = profile, user = request.user)
            category_heading = get_category_heading[category]
            category_text = get_category_text[category]
            if request.user.is_authenticated and request.user.category == 'user' and profile:
                metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
                return render(request, "user/profiles/profile-item.html", {"title": "User Profiles", 'category': category, 'profile': profile, 'data': data, 'category_heading': category_heading, 'category_text': category_text, 'count': {'drugs_count': AwsDynamoDb.UserProfileDrugs.objects.filter(user_profile = profile, user = request.user).count(), 'conditions_count': AwsDynamoDb.UserProfileConditions.objects.filter(user_profile = profile, user = request.user).count(), 'allergies_count': AwsDynamoDb.UserProfileAllergies.objects.filter(user_profile = profile, user = request.user).count(), 'reports_count': 2, 'reminder_count': AwsDynamoDb.UserProfileReminder.objects.filter(user_profile = profile, user = request.user).count(), 'notes_count': AwsDynamoDb.UserProfileNotes.objects.filter(user_profile = profile, user = request.user).count()}, 'profile_len': AwsDynamoDb.UserProfile.objects.filter(user = request.user).count(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': profile.profile_name+" "+category.capitalize(), 'link': f"/user/profiles/{profile.id}/{category}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
            else:
                return redirect('/signin')
        else:
            raise Http404("404! This data doent exist.")
    except:
        raise Http404("404! This data doent exist.")
def UserProfilesViewItemView(request, id, category, item_id):
    get_model_name = {'drugs': AwsDynamoDb.UserProfileDrugs, 'conditions': AwsDynamoDb.UserProfileConditions, 'reports': AwsDynamoDb.UserProfileConditions, 'allergies': AwsDynamoDb.UserProfileAllergies, 'reminder': AwsDynamoDb.UserProfileReminder, 'notes': AwsDynamoDb.UserProfileNotes}
    get_category_heading = {'drugs': 'Add your first drug', 'conditions': 'Conditions', 'reports': 'Interactions Report', 'allergies': 'Allergies', 'reminder': 'Manage your meds', 'notes': 'Notes'}
    get_category_text = {'drugs': 'You can start keeping track of your medications by adding them to your profile. Get to conversations, warnings, and alerts right away.', 'conditions': 'To help build your health record, add symptoms to your background. Find out more about these conditions and the medicines that can help you.', 'reports': 'The medicines in your profile did not mix with each other. This doesn&apos;t always mean that there are no encounters. Always talk to your doctor or nurse.', 'allergies': 'You can see alerts when one of your drugs might cause an allergic reaction after adding them to your profile.', 'reminder': 'Add all of your medicines and be reminded every time to take them.', 'notes': 'You can make a timeline of medical events (appointments, accidents, surgeries, etc.) by adding notes to your profile.'}
    try:
        if category in ['drugs', 'conditions', 'reports', 'allergies', 'reminder', 'notes']:
            profile = AwsDynamoDb.UserProfile.objects.filter(id = id, user = request.user).only('id', 'profile_name').first()
            data = get_model_name[category].objects.filter(user_profile = profile, user = request.user)
            category_heading = get_category_heading[category]
            category_text = get_category_text[category]
            if request.user.is_authenticated and request.user.category == 'user' and profile:
                metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
            
                return render(request, "user/profiles/profile-item.html", {"title": "User Profiles", 'view_data': get_model_name[category].objects.filter(id = item_id).first(), 'category': category, 'profile': profile, 'data': data, 'category_heading': category_heading, 'category_text': category_text, 'count': {'drugs_count': AwsDynamoDb.UserProfileDrugs.objects.filter(user_profile = profile, user = request.user).count(), 'conditions_count': AwsDynamoDb.UserProfileConditions.objects.filter(user_profile = profile, user = request.user).count(), 'allergies_count': AwsDynamoDb.UserProfileAllergies.objects.filter(user_profile = profile, user = request.user).count(), 'reports_count': 2, 'reminder_count': AwsDynamoDb.UserProfileReminder.objects.filter(user_profile = profile, user = request.user).count(), 'notes_count': AwsDynamoDb.UserProfileNotes.objects.filter(user_profile = profile, user = request.user).count()}, 'profile_len': AwsDynamoDb.UserProfile.objects.filter(user = request.user).count(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': profile.profile_name+" "+category.capitalize(), 'link': f"/user/profiles/{profile.id}/{category}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
            else:
                return redirect('/signin')
        else:
            raise Http404("404! This data doent exist.")
    except:
        raise Http404("404! This data doent exist.")
def UserProfilesViewItemAdd(request, id, category):
    get_model_name = {'drugs': AwsDynamoDb.UserProfileDrugs, 'conditions': AwsDynamoDb.UserProfileConditions, 'allergies': AwsDynamoDb.UserProfileAllergies, 'reminder': AwsDynamoDb.UserProfileReminder, 'notes': AwsDynamoDb.UserProfileNotes}
    get_category_heading = {'drugs': 'Add your first drug', 'conditions': 'Conditions', 'allergies': 'Allergies', 'reminder': 'Manage your meds', 'notes': 'Notes'}
    get_category_text = {'drugs': 'You can start keeping track of your medications by adding them to your profile. Get to conversations, warnings, and alerts right away.', 'conditions': 'To help build your health record, add symptoms to your background. Find out more about these conditions and the medicines that can help you.', 'allergies': 'You can see alerts when one of your drugs might cause an allergic reaction after adding them to your profile.', 'reminder': 'Add all of your medicines and be reminded every time to take them.', 'notes': 'You can make a timeline of medical events (appointments, accidents, surgeries, etc.) by adding notes to your profile.'}
    get_form = {'drugs': AwsDynamoDb.UserProfileDrugsFormInitial, 'conditions': AwsDynamoDb.UserProfileConditionsFormInitial, 'allergies': AwsDynamoDb.UserProfileAllergiesForm, 'reminder': AwsDynamoDb.UserProfileReminderForm, 'notes': AwsDynamoDb.UserProfileNotesForm}
    try:
        if category in ['drugs', 'conditions', 'allergies', 'reminder', 'notes']:
            profile = AwsDynamoDb.UserProfile.objects.filter(id = id, user = request.user).only('id', 'profile_name').first()
            data = get_model_name[category].objects.filter(user_profile = profile, user = request.user)
            category_heading = get_category_heading[category]
            category_text = get_category_text[category]
            if request.user.is_authenticated and request.user.category == 'user' and profile:
                metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
              
                context = {"title": "User Profiles", 'form': get_form[category], 'category': category, 'profile': profile, 'data': data, 'category_heading': category_heading, 'category_text': category_text, 'count': {'drugs_count': AwsDynamoDb.UserProfileDrugs.objects.filter(user_profile = profile, user = request.user).count(), 'conditions_count': AwsDynamoDb.UserProfileConditions.objects.filter(user_profile = profile, user = request.user).count(), 'allergies_count': AwsDynamoDb.UserProfileAllergies.objects.filter(user_profile = profile, user = request.user).count(), 'reports_count': 2, 'reminder_count': AwsDynamoDb.UserProfileReminder.objects.filter(user_profile = profile, user = request.user).count(), 'notes_count': AwsDynamoDb.UserProfileNotes.objects.filter(user_profile = profile, user = request.user).count()}, 'profile_len': AwsDynamoDb.UserProfile.objects.filter(user = request.user).count(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': profile.profile_name+" "+category.capitalize(), 'link': f"/user/profiles/{profile.id}/{category}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
                if request.method == 'POST':
                    context['form'] = get_form[category](request.POST)
                    if context['form'].is_valid():
                        try:
                            user_profile_data = context['form'].save(commit=False)
                            user_profile_data.user = request.user
                            user_profile_data.user_profile = profile
                            user_profile_data.save()
                            return redirect(f'/user/profiles/{profile.id}/{category}')
                        except IntegrityError:
                            context['form'].add_error(None, "This record is already associated with the user profile.")
                return render(request, "user/profiles/add-edit-profile-item.html", context)
            else:
                return redirect('/user/profiles/')
        else:
            raise Http404("404! This page doent exist.")
    except:
        raise Http404("404! Doent exist.")
def UserProfilesViewItemEdit(request, id, category, item_id):
    get_model_name = {'drugs': AwsDynamoDb.UserProfileDrugs, 'conditions': AwsDynamoDb.UserProfileConditions, 'allergies': AwsDynamoDb.UserProfileAllergies, 'reminder': AwsDynamoDb.UserProfileReminder, 'notes': AwsDynamoDb.UserProfileNotes}
    get_category_heading = {'drugs': 'Add your first drug', 'conditions': 'Conditions', 'allergies': 'Allergies', 'reminder': 'Manage your meds', 'notes': 'Notes'}
    get_category_text = {'drugs': 'You can start keeping track of your medications by adding them to your profile. Get to conversations, warnings, and alerts right away.', 'conditions': 'To help build your health record, add symptoms to your background. Find out more about these conditions and the medicines that can help you.', 'allergies': 'You can see alerts when one of your drugs might cause an allergic reaction after adding them to your profile.', 'reminder': 'Add all of your medicines and be reminded every time to take them.', 'notes': 'You can make a timeline of medical events (appointments, accidents, surgeries, etc.) by adding notes to your profile.'}
    get_form = {'drugs': AwsDynamoDb.UserProfileDrugsFormInitial, 'conditions': AwsDynamoDb.UserProfileConditionsFormInitial, 'allergies': AwsDynamoDb.UserProfileAllergiesForm, 'reminder': AwsDynamoDb.UserProfileReminderForm, 'notes': AwsDynamoDb.UserProfileNotesForm}
    try:
        if category in ['drugs', 'conditions', 'allergies', 'reminder', 'notes']:
            profile = AwsDynamoDb.UserProfile.objects.filter(id = id, user = request.user).only('id', 'profile_name').first()
            data = get_model_name[category].objects.filter(user_profile = profile, user = request.user)
            category_heading = get_category_heading[category]
            category_text = get_category_text[category]
            if request.user.is_authenticated and request.user.category == 'user' and profile:
                metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
                
                context = {"title": "User Profiles", 'form': get_form[category](instance = get_object_or_404(get_model_name[category], id=item_id)), 'category': category, 'profile': profile, 'data': data, 'category_heading': category_heading, 'category_text': category_text, 'count': {'drugs_count': AwsDynamoDb.UserProfileDrugs.objects.filter(user_profile = profile, user = request.user).count(), 'conditions_count': AwsDynamoDb.UserProfileConditions.objects.filter(user_profile = profile, user = request.user).count(), 'allergies_count': AwsDynamoDb.UserProfileAllergies.objects.filter(user_profile = profile, user = request.user).count(), 'reports_count': 2, 'reminder_count': AwsDynamoDb.UserProfileReminder.objects.filter(user_profile = profile, user = request.user).count(), 'notes_count': AwsDynamoDb.UserProfileNotes.objects.filter(user_profile = profile, user = request.user).count()}, 'profile_len': AwsDynamoDb.UserProfile.objects.filter(user = request.user).count(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': profile.profile_name+" "+category.capitalize(), 'link': f"/user/profiles/{profile.id}/{category}"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
                if request.method == 'POST':
                    context['form'] = get_form[category](request.POST, instance = get_object_or_404(get_model_name[category], id=item_id))
                    if context['form'].is_valid():
                        try:
                            user_profile_data = context['form'].save(commit=False)
                            user_profile_data.user = request.user
                            user_profile_data.user_profile = profile
                            user_profile_data.save()
                            return redirect(f'/user/profiles/{profile.id}/{category}/edit/{item_id}')
                        except IntegrityError:
                            context['form'].add_error(None, "This record is already associated with the user profile.")
                return render(request, "user/profiles/add-edit-profile-item.html", context)
            else:
                return redirect('/user/profiles/')
        else:
            raise Http404("404! This page doent exist.")
    except:
        raise Http404("404! Doent exist.")
def UserProfilesViewItemDelete(request, id, category, item_id):
    get_model_name = {'drugs': AwsDynamoDb.UserProfileDrugs, 'conditions': AwsDynamoDb.UserProfileConditions, 'allergies': AwsDynamoDb.UserProfileAllergies, 'reminder': AwsDynamoDb.UserProfileReminder, 'notes': AwsDynamoDb.UserProfileNotes}
    if request.user.is_authenticated and request.user.category == 'user':
        try:
            get_model_name[category].objects.filter(user = request.user, user_profile = id, id = item_id).delete()
        except:
            return redirect(f'/user/profiles/{id}/{category}')
        return redirect(f'/user/profiles/{id}/{category}')
    else:
        return redirect('/signin')










##################### QNA Pages Starts Here #######################
def QNA(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        if request.method == "POST":
            email = str(request.POST.get('email'))
            newsletter, created = AwsDynamoDb.newsletter.objects.get_or_create(email = email, defaults = {'monthly_newsletter': str(request.POST.get('monthly_newsletter')) == 'on', 'daily_newsletter': str(request.POST.get('daily_newsletter')) == 'on', 'FDA_safety_alerts': str(request.POST.get('FDA_safety_alerts')) == 'on'})
            if not created:
                newsletter.monthly_newsletter = str(request.POST.get('monthly_newsletter')) == 'on'
                newsletter.daily_newsletter = str(request.POST.get('daily_newsletter')) == 'on'
                newsletter.FDA_safety_alerts = str(request.POST.get('FDA_safety_alerts')) == 'on'
                newsletter.save()
        popular_support_groups = [{"name": "Anxiety", "id": "sasfasfasas"}, {"name": "Pain", "id": "sasfasfasas"}, {"name": "Anxiety and...", "id": "sasfasfasas"}, {"name": "Panic Disorder", "id": "sasfasfasas"}, {"name": "Bipolar...", "id": "sasfasfasas"}, {"name": "Period", "id": "sasfasfasas"}, {"name": "Depression", "id": "sasfasfasas"}, {"name": "Pill", "id": "sasfasfasas"}, {"name": "Doctor", "id": "sasfasfasas"}, {"name": "Pregnancy", "id": "sasfasfasas"}, {"name": "Dosage", "id": "sasfasfasas"}, {"name": "Prescription", "id": "sasfasfasas"}, {"name": "Drug", "id": "sasfasfasas"}, {"name": "Psoriasis", "id": "sasfasfasas"}, {"name": "Gabapentin", "id": "sasfasfasas"}, {"name": "Sex", "id": "sasfasfasas"}, {"name": "Generalized...", "id": "sasfasfasas"}, {"name": "Side Effect", "id": "sasfasfasas"}, {"name": "High Blood...", "id": "sasfasfasas"}, {"name": "Sleep", "id": "sasfasfasas"}, {"name": "Infections", "id": "sasfasfasas"}, {"name": "Sleep Disorders", "id": "sasfasfasas"}, {"name": "Insomnia", "id": "sasfasfasas"}, {"name": "Tramadol", "id": "sasfasfasas"}, {"name": "Lexapro", "id": "sasfasfasas"}, {"name": "Weight", "id": "sasfasfasas"}, {"name": "Major...", "id": "sasfasfasas"}, {"name": "Weight Loss...", "id": "sasfasfasas"}, {"name": "Medication", "id": "sasfasfasas"}, {"name": "Xanax", "id": "sasfasfasas"}, {"name": "Medicine", "id": "sasfasfasas"}, {"name": "Zoloft", "id": "sasfasfasas"}]
        recently_popular_questions = [{"id": "#", "question": "Does metoprolol make you sleepy?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Does metoprolol cause hair loss?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Prozac vs Xanax: How do they compare?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Is it normal to have discharge on Depo shot?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Which drugs should I avoid with diverticulitis?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Can pharmacists prescribe Paxlovid?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Penicillin allergies: What do I need to know?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Does Tylenol cause autism, what do the studies say?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Who is eligible for the Biktarvy Copay Card?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "What other Biktarvy Patient Assistance programs are there?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "How long can Emgality be out of the fridge?", "category": "FAQ", "answered_by": "RxZee.com"}, {"id": "#", "question": "Am I able to store Emgality out of the Fridge?", "category": "FAQ", "answered_by": "RxZee.com"}]
        return render(request, "user/qna/qna.html", {"title": "Rx Zee Answers", "popular_support_groups": popular_support_groups, 'recently_popular_questions': recently_popular_questions, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Q & A', 'link': "/user/qna"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')

def Questions(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        return render(request, "user/qna/questions.html", {"title": "Rx Zee Questions", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Q & A', 'link': "/user/qna"}, {'name': 'Questions', 'link': "/user/qna/questions"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')
def AskAQuestion(request):
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}

    context = {"title": "Ask a Question", "form": AwsDynamoDb.QuestionsForm(), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Q & A', 'link': "/user/qna"}, {'name': 'Questions', 'link': "/user/qna/questions"}, {'name': 'Ask', 'link': "/user/qna/questions/ask"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
    if request.user.is_authenticated and request.user.category == 'user':
        if request.method == "POST":
            form = AwsDynamoDb.QuestionsForm(request.POST)
            if form.is_valid():
                question_instance = form.save(commit = False)
                question_instance.user = request.user
                question_instance.save()
                return redirect("/user/qna/questions")
            else:
                context["form"] = form
        return render(request, "user/qna/ask_question.html", context)
    else:
        return redirect('/signin')
##################### QNA Pages Ends Here #########################


##################### Support Groups Starts Here #######################
def support_groups(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        if request.method == "POST":
            email = str(request.POST.get('email'))
            newsletter, created = AwsDynamoDb.newsletter.objects.get_or_create(email = email, defaults = {'monthly_newsletter': str(request.POST.get('monthly_newsletter')) == 'on', 'daily_newsletter': str(request.POST.get('daily_newsletter')) == 'on', 'FDA_safety_alerts': str(request.POST.get('FDA_safety_alerts')) == 'on'})
            if not created:
                newsletter.monthly_newsletter = str(request.POST.get('monthly_newsletter')) == 'on'
                newsletter.daily_newsletter = str(request.POST.get('daily_newsletter')) == 'on'
                newsletter.FDA_safety_alerts = str(request.POST.get('FDA_safety_alerts')) == 'on'
                newsletter.save()
        top_medications_support_groups = ["Adderall", "Clonazepam", "Cymbalta", "Effexor", "Gabapentin", "Ibuprofen", "Klonopin", "Lexapro", "Lisinopril", "Oxycodone", "Plan B One-Step", "Prednisone", "Prozac", "Sertraline", "Suboxone", "Tramadol", "Trazodone", "Wellbutrin", "Xanax", "Zol"]
        top_conditions_support_groups = ["Anxiety", "Anxiety and Stress", "Attention-Deficit Hyperactivity Disorder (ADHD)", "Back Pain", "Bipolar Disorder", "Birth Control", "Blood Disorders", "Chronic Pain", "Contraception", "Depression", "Diabetes, Type 2", "Emergency Contraception", "Fibromyalgia", "GERD", "Generalized Anxiety Disorder", "Headache", "High Blood Pressure", "Infections", "Insomnia", "Major Depressive Disorder", "Migraine", "Nausea / Vomiting", "Obsessive Compulsive Disorder", "Pain", "Panic Disorder", "Psoriasis", "Rheumatoid Arthritis", "Sleep Disorders", "Weight Loss (Obesity / Overweight)"]
        return render(request, "user/support_groups.html", {"title": "Support Groups", 'top_conditions_support_groups': top_conditions_support_groups, 'top_medications_support_groups': top_medications_support_groups, 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Support Groups', 'link': "/user/support-groups"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')
##################### Support Groups Ends Here #########################

















def SettingsAccountOverview(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        return render(request, "user/account/overview.html", {"title": "Account Overview", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Account', 'link': "/signin"}, {'name': 'Overview', 'link': "/account/overview"} ], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata})
    else:
        return redirect('/signin')
def SettingsAccountDetails(request):
    if request.user.is_authenticated and request.user.category == 'user':
        metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}
       
        context = {"title": "Account Details", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Account', 'link': "/signin"}, {'name': 'Details', 'link': "/account/details"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
        if request.method == 'POST':
            print(request.POST)
        return render(request, "user/account/details.html", context)
    else:
        return redirect('/signin')
def SettingsAccountDetailsCloseAccount(request):
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}

    if request.user.is_authenticated and request.user.category == 'user':
        context = {"title": "Close Account", 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Account', 'link': "/signin"}, {'name': 'Details', 'link': "/account/details"}, {'name': 'Close Account', 'link': "/account/details/closeaccount"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), "error": "", 'metadata': metadata}
        if request.method == "POST":
            if request.user.check_password(request.POST.get("password")):
                AwsDynamoDb.UserDeleteAccount.objects.create(user_username = request.user.username, user_full_name = (request.user.first_name+request.user.last_name), closure_reason = request.POST.get("closure_reason"))
                return redirect('/')
            else:
                context["error"] = "Invalid Password! Please check and try again."
        return render(request, "user/account/details/closeaccount.html", context)
    else:
        return redirect('/signin')
def SettingsAccountSubscription(request):
    metadata = {
    "og_description": "Your description here.",
    "og_image": "https://rxzee.com/static/RxZee.svg",
    "og_url": "https://rxzee.com/page"}

    if request.user.is_authenticated and request.user.category == 'user':
        context = {"title": "Account Details", "form": AwsDynamoDb.UserSubscriptionForm(user=request.user, instance = request.user), 'breadcrumbs': [{'name': 'Home', 'link': "/"}, {'name': 'Account', 'link': "/account/overview"}, {'name': 'Subscription', 'link': "/account/subscription"}], "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink')), 'metadata': metadata}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.UserSubscriptionForm(request.POST, user=request.user, instance = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/account/subscription")
        return render(request, "user/account/subscription.html", context)
    else:
        return redirect('/signin')
#################################################################################################################################################################
################################################################### User Views Ends Here ########################################################################
#################################################################################################################################################################


######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################


#################################################################################################################################################################
################################################################## Author Views Starts Here #####################################################################
#################################################################################################################################################################
def AuthorDashboard(request):
    if request.user.is_authenticated and request.user.category == 'author':
        return render(request, "author/dashboard.html", {"title": "Dashboard", "activeNav": "da", "top_stats": {"drugs": AwsDynamoDb.drug.objects.filter(author=request.user).count(), "vitamins": AwsDynamoDb.vitaminsAndSupplement.objects.filter(author = request.user).count(), "interactions": AwsDynamoDb.drug_interactions.objects.filter(author = request.user).count(), "pills": AwsDynamoDb.pill.objects.filter(author = request.user).count()}, "news": list(AwsDynamoDb.news.objects.filter(author = request.user).values('permalink', 'title', 'search_count')[:10]), "condition": list(AwsDynamoDb.condition.objects.filter(author = request.user).values('permalink', 'heading', 'search_count')[:10]), "well_being": list(AwsDynamoDb.well_being.objects.filter(author = request.user).values('permalink', 'title', 'search_count')[:10]), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()})
    else:
        return redirect('/signin')
def AuthorDrugs(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.drug.objects.filter(author = request.user).select_related('author').order_by('name').values('permalink', 'name', 'generic_name', 'dosage_forms', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allDrugsData = paginator.page(page)
        except PageNotAnInteger:
            allDrugsData = paginator.page(1)
        except EmptyPage:
            allDrugsData = paginator.page(paginator.num_pages)
        context = {"title": "Drugs", "activeNav": "dr", "table_name": "All Registered Drugs", "data": allDrugsData.object_list, "page_obj": allDrugsData, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/drugs/drugsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorDrugsAdd(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = { "title": "Add Drugs", "activeNav": "dr", "form": AwsDynamoDb.DrugRichTextForm(), "error": "", "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            widgets = []
            if request.POST.get("widget1"):
                widgets.append("widget1")
            if request.POST.get("widget2"):
                widgets.append("widget2")
            if request.POST.get("widget3"):
                widgets.append("widget3")
            name = request.POST.get("name", '')
            pronunciation = request.POST.get("pronunciation", '')
            generic_name = request.POST.get("generic_name", '')
            brand_name = request.POST.get("brand_name", '')
            class_name = request.POST.get("class_name", '')
            dosage_forms = request.POST.get("dosage_forms", '')
            availability = request.POST.get("availability", '')
            widgets = ', '.join(widgets)
            uses = request.POST.get("uses", '')
            side_effects = request.POST.get("side_effects", '')
            warnings = request.POST.get("warnings", '')
            precautions = request.POST.get("precautions", '')
            interactions = request.POST.get("interactions", '')
            overdose = request.POST.get("overdose", '')
            seo_title = request.POST.get("seo_title", '')
            seo_keywords = request.POST.get("seo_keywords", '')
            seo_description = request.POST.get("seo_description", '')
            permalink = request.POST.get("permalink", '')
            try:
                AwsDynamoDb.drug.objects.create(permalink=permalink, name=name, availability=availability, pronunciation=pronunciation, generic_name=generic_name, brand_name=brand_name, class_name=class_name, dosage_forms=dosage_forms, author=request.user, widgets=widgets, uses=uses, warnings=warnings, overdose=overdose, side_effects=side_effects, interactions=interactions, precautions=precautions, seo_title=seo_title, seo_keywords=seo_keywords, seo_description=seo_description)
                return redirect(f"/author/drugs/{permalink}")
            except Exception as e:
                context['normal_details'] = {"name": name, "availability": availability, "pronunciation": pronunciation, "generic_name": generic_name, "brand_name": brand_name, "class_name": class_name, "dosage_forms": dosage_forms, "author": request.user}
                context['form'] = AwsDynamoDb.DrugRichTextForm({'uses': uses, 'warnings': warnings, 'precautions': precautions, 'overdose': overdose, 'side_effects': side_effects, 'interactions': interactions})
                context['seo_context'] = {"seo_title": seo_title, "seo_description": seo_description, "seo_keywords": seo_keywords, "permalink": permalink}
                context['widgets'] = widgets
                context['error'] = str(e)
        return render(request, "author/drugs/addEditDrugs.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorDrugsEdit(request, permalink):
    if request.user.is_authenticated and request.user.category == 'author':
        try:
            drugData = AwsDynamoDb.drug.objects.filter(author = request.user, permalink = permalink).select_related('author').values('permalink', 'name', 'brand_name', 'generic_name', 'pronunciation', 'class_name', 'dosage_forms', 'availability', 'author_id', 'author__first_name', 'widgets', 'uses', 'side_effects', 'warnings', 'precautions', 'interactions', 'overdose', 'seo_title', 'seo_description', 'seo_keywords',  'search_count', 'status', 'last_updated').first() or False
        except:
            return redirect("/author/drugs")
        if drugData:
            print(drugData['permalink'])
            normal_details = {"name": drugData.get('name'), "status": drugData.get('status'), "pronunciation": drugData.get('pronunciation'), "generic_name": drugData.get('generic_name'), "brand_name": drugData.get('brand_name'), "class_name": drugData.get('class_name'), "dosage_forms": drugData.get('dosage_forms'), 'availability': drugData.get('availability')}
            form = AwsDynamoDb.DrugRichTextForm({'uses': drugData.get('uses'), 'side_effects': drugData.get('side_effects'), 'warnings': drugData.get('warnings'), 'precautions': drugData.get('precautions'), 'interactions': drugData.get('interactions'), 'overdose': drugData.get('overdose'), 'pills': drugData.get('pills')})
            seo_context = {"seo_title": drugData.get('seo_title'), "seo_description": drugData.get('seo_description'), "seo_keywords": drugData.get('seo_keywords'), "permalink": drugData.get('permalink')}
            allFaqs = list(AwsDynamoDb.drugsFaq.objects.filter(drug = drugData.get('permalink')).values())
            context = { "title": "Edit Drugs", "activeNav": "dr", "normal_details": normal_details, "form": form, "seo_context": seo_context, "id": drugData.get("id"), "allFaqs": allFaqs, "widgets": str(drugData.get("widgets")).split(", "), "error": "", "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
            if request.method == "POST":
                widgets = []
                if request.POST.get("widget1"):
                    widgets.append("widget1")
                if request.POST.get("widget2"):
                    widgets.append("widget2")
                if request.POST.get("widget3"):
                    widgets.append("widget3")
                name = request.POST.get("name", '')
                pronunciation = request.POST.get("pronunciation", '')
                generic_name = request.POST.get("generic_name", '')
                brand_name = request.POST.get("brand_name", '')
                class_name = request.POST.get("class_name", '')
                dosage_forms = request.POST.get("dosage_forms", '')
                availability = request.POST.get("availability", '')
                widgets = ', '.join(widgets)
                uses = request.POST.get("uses", '')
                side_effects = request.POST.get("side_effects", '')
                warnings = request.POST.get("warnings", '')
                precautions = request.POST.get("precautions", '')
                interactions = request.POST.get("interactions", '')
                overdose = request.POST.get("overdose", '')
                seo_title = request.POST.get("seo_title", '')
                seo_description = request.POST.get("seo_description", '')
                seo_keywords = request.POST.get("seo_keywords", '')
                permalinks = request.POST.get("permalink", '')
                try:
                    AwsDynamoDb.drug.objects.filter(permalink = permalink).update(name=name, availability=availability, pronunciation=pronunciation, generic_name=generic_name, brand_name=brand_name, class_name=class_name, dosage_forms=dosage_forms, author=request.user, widgets=widgets, uses=uses, warnings=warnings, overdose=overdose, side_effects=side_effects, interactions=interactions, precautions=precautions, seo_title=seo_title, seo_keywords=seo_keywords, seo_description=seo_description, permalink = permalinks)
                    return redirect(f"/author/drugs/{permalinks}")
                except Exception as e:
                    context['normal_details'] = {"name": name, "availability": availability, "pronunciation": pronunciation, "generic_name": generic_name, "brand_name": brand_name, "class_name": class_name, "dosage_forms": dosage_forms}
                    context['form'] = AwsDynamoDb.DrugRichTextForm({'uses': uses, 'warnings': warnings, 'precautions': precautions, 'overdose': overdose, 'side_effects': side_effects, 'interactions': interactions})
                    context['seo_context'] = {"seo_title": seo_title, "seo_description": seo_description, "seo_keywords": seo_keywords, "permalink": permalinks}
                    context['widgets'] = widgets
                    context['error'] = str(e)
            return render(request, "author/drugs/addEditDrugs.html", context)
        else:
            return redirect("/author/drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddDrugFAQ(request):
    if request.user.is_authenticated and request.user.category == 'author' and request.method == "POST":
        try:
            drug = request.POST.get("drug", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            data = AwsDynamoDb.drugsFaq.objects.create(question = question, answer = answer, drug = AwsDynamoDb.drug.objects.get(permalink = drug, author = request.user))
            data.save()
            return redirect("/author/drugs/"+drug)
        except:
            return redirect("/author/drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditDrugFAQ(request, id):
    if request.user.is_authenticated and request.user.category == 'author' and request.method == "POST":
        try:
            drug = request.POST.get("drug", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            AwsDynamoDb.drugsFaq.objects.filter(id=id).update(question=question, answer=answer)
            return redirect("/author/drugs/"+drug)
        except:
            return redirect("/author/drugs/")
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorVitaminsAndSupplements(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.vitaminsAndSupplement.objects.filter(author = request.user).select_related('author').order_by('name').values('permalink', 'name', 'other_names', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allVitaminsAndSupplementsData = paginator.page(page)
        except PageNotAnInteger:
            allVitaminsAndSupplementsData = paginator.page(1)
        except EmptyPage:
            allVitaminsAndSupplementsData = paginator.page(paginator.num_pages)
        context = {"title": "Vitamins and Supplements", "activeNav": "vi", "table_name": "All Vitamins and Supplements", "data": allVitaminsAndSupplementsData.object_list, "page_obj": allVitaminsAndSupplementsData, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/vitamins/vitaminsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorVitaminsAndSupplementsAdd(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = { "title": "Add Vitamins and Supplements", "activeNav": "vi", "form": AwsDynamoDb.VitaminsAndSupplementsRichTextForm(), "error": "", "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            widgets = []
            if request.POST.get("widget1"):
                widgets.append("widget1")
            if request.POST.get("widget2"):
                widgets.append("widget2")
            if request.POST.get("widget3"):
                widgets.append("widget3")
            name = request.POST.get("name", '')
            other_names = request.POST.get("other_names", '')
            widgets = ', '.join(widgets)
            author = request.user
            overview = request.POST.get("overview", '')
            uses = request.POST.get("uses", '')
            side_effects = request.POST.get("side_effects", '')
            precautions = request.POST.get("precautions", '')
            interactions = request.POST.get("interactions", '')
            dosing = request.POST.get("dosing", '')
            seo_title = request.POST.get("seo_title", '')
            seo_keywords = request.POST.get("seo_keywords", '')
            seo_description = request.POST.get("seo_description", '')
            permalink = request.POST.get("permalink", '')
            try:
                AwsDynamoDb.vitaminsAndSupplement.objects.create(name=name, other_names=other_names, author=author, widgets=widgets, overview=overview, uses=uses, dosing=dosing, side_effects=side_effects, interactions=interactions, precautions=precautions, seo_title=seo_title, seo_keywords=seo_keywords, seo_description=seo_description, permalink=permalink)
                return redirect("/author/vitamins")
            except Exception as e:
                context['normal_details'] = {"name": name, "other_names": other_names, 'author': author}
                context['form'] = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': overview, 'uses': uses, 'side_effects': side_effects, 'precautions': precautions, 'interactions': interactions, 'dosing': dosing})
                context['seo_context'] = {"seo_title": seo_title, "seo_description": seo_description, "seo_keywords": seo_keywords, "permalink": permalink}
                context['widgets'] = widgets
                context['error'] = str(e)
        return render(request, "author/vitamins/addEditVitamins.html",context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorVitaminsAndSupplementsEdit(request, permalink):
    if request.user.is_authenticated and request.user.category == 'author':
        try:
            vitaminsAndSupplementsData = AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink = permalink, author = request.user).values().first() or False
        except:
            return redirect("/author/vitamins")
        normal_details = {"name": vitaminsAndSupplementsData.get('name'), "other_names": vitaminsAndSupplementsData.get('other_names'), 'status': vitaminsAndSupplementsData.get('status')}
        form = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': vitaminsAndSupplementsData.get('overview'), 'uses': vitaminsAndSupplementsData.get('uses'), 'side_effects': vitaminsAndSupplementsData.get('side_effects'), 'interactions': vitaminsAndSupplementsData.get('interactions'), 'precautions': vitaminsAndSupplementsData.get('precautions'), 'dosing': vitaminsAndSupplementsData.get('dosing')})
        seo_context = {"seo_title": vitaminsAndSupplementsData.get('seo_title'), "seo_description": vitaminsAndSupplementsData.get('seo_description'), "seo_keywords": vitaminsAndSupplementsData.get('seo_keywords'), "seo_author": vitaminsAndSupplementsData.get('seo_author'), "featured_image": vitaminsAndSupplementsData.get('featured_image'), "permalink": vitaminsAndSupplementsData.get('permalink')}
        allFaqs = list(AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(vitaminsAndSupplement = vitaminsAndSupplementsData.get('permalink')).values())
        context = { "title": "Edit Vitamins and Supplements", "activeNav": "vi", "normal_details": normal_details, "form": form, "seo_context": seo_context, "id": vitaminsAndSupplementsData.get("id"), "allFaqs": allFaqs, "widgets": str(vitaminsAndSupplementsData.get("widgets")).split(", "), "error": "", "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            widgets = []
            if request.POST.get("widget1"):
                widgets.append("widget1")
            if request.POST.get("widget2"):
                widgets.append("widget2")
            if request.POST.get("widget3"):
                widgets.append("widget3")
            name = request.POST.get("name", '')
            other_names = request.POST.get("other_names", '')
            widgets = ', '.join(widgets)
            overview = request.POST.get("overview", '')
            uses = request.POST.get("uses", '')
            side_effects = request.POST.get("side_effects", '')
            precautions = request.POST.get("precautions", '')
            interactions = request.POST.get("interactions", '')
            dosing = request.POST.get("dosing", '')
            seo_title = request.POST.get("seo_title", '')
            seo_keywords = request.POST.get("seo_keywords", '')
            seo_description = request.POST.get("seo_description", '')
            permalinks = request.POST.get("permalink", '')
            try:
                AwsDynamoDb.vitaminsAndSupplement.objects.filter(permalink=permalink).update(name=name, other_names=other_names, widgets=widgets, overview=overview, uses=uses, dosing=dosing, side_effects=side_effects, interactions=interactions, precautions=precautions, seo_title=seo_title, seo_keywords=seo_keywords, seo_description=seo_description, status ="pending", permalink=permalinks)
                return redirect("/author/vitamins/"+permalinks)
            except Exception as e:
                context['normal_details'] = {"name": name, "other_names": other_names}
                context['form'] = AwsDynamoDb.VitaminsAndSupplementsRichTextForm({'overview': overview, 'uses': uses, 'side_effects': side_effects, 'precautions': precautions, 'interactions': interactions, 'dosing': dosing})
                context['seo_context'] = {"seo_title": seo_title, "seo_description": seo_description, "seo_keywords": seo_keywords, "permalink": permalinks}
                context['widgets'] = widgets
                context['error'] = str(e)
        return render(request, "author/vitamins/addEditVitamins.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddVitaminsAndSupplementsFAQ(request):
    if request.user.is_authenticated and request.user.category == 'author' and request.method == "POST":
        try:
            vitaminsAndSupplements = request.POST.get("vitamins", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            data = AwsDynamoDb.vitaminsAndSupplementsFaq.objects.create(question = question, answer = answer, vitaminsAndSupplement = AwsDynamoDb.vitaminsAndSupplement.objects.get(permalink = vitaminsAndSupplements, author = request.user))
            data.save()
            return redirect("/author/vitamins/"+vitaminsAndSupplements)
        except:
            return redirect("/author/vitamins/")
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditVitaminsAndSupplementsFAQ(request, id):
    if request.user.is_authenticated and request.user.category == 'author' and request.method == "POST":
        try:
            vitaminsAndSupplements = request.POST.get("vitamins", False)
            question = request.POST.get("question", False)
            answer = request.POST.get("answer", False)
            AwsDynamoDb.vitaminsAndSupplementsFaq.objects.filter(id = id).update(question=question, answer=answer)
            return redirect("/author/vitamins/"+vitaminsAndSupplements)
        except:
            return redirect("/author/vitamins/")
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAllInteractions(request):
    if request.user.is_authenticated and request.user.category == 'author':
        if 'drug' in request.path:
            columns = ['First Drug', 'Second Drug', 'Interaction Type', 'Author', 'Status', 'Last Updated']
            table_name = 'All Drug Interactions'
            activeNav = 'drin'
            paginator = Paginator(list(AwsDynamoDb.drug_interactions.objects.filter(author = request.user).select_related('author').order_by('-last_updated').values('id', 'first_drug', 'second_drug', 'level', 'status', 'last_updated', 'author__first_name')), 500)
        elif 'food' in request.path:
            columns = ['Formula', 'Header', 'Severity', 'Interaction Level', 'Author', 'Status', 'Last Updated']
            table_name = 'All Food Interactions'
            activeNav = 'fin'
            paginator = Paginator(list(AwsDynamoDb.food_interactions.objects.select_related('author').order_by('-last_updated').values('id', 'formula', 'header', 'severity', 'level', 'author__first_name', 'status', 'last_updated')), 500)
        elif 'disease' in request.path:
            columns = ['Formula', 'Header', 'Severity', 'Interaction Level', 'Author', 'Status', 'Last Updated']
            table_name = 'All Disease Interactions'
            activeNav = 'din'
            paginator = Paginator(list(AwsDynamoDb.disease_interactions.objects.select_related('author').order_by('-last_updated').values('id', 'formula', 'header', 'severity', 'level', 'author__first_name', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allInteractions = paginator.page(page)
        except PageNotAnInteger:
            allInteractions = paginator.page(1)
        except EmptyPage:
            allInteractions = paginator.page(paginator.num_pages)
        context = {"title": "Interaction Checker", "activeNav": activeNav, "table_name": table_name, "columns": columns, "data": allInteractions.object_list, "page_obj": allInteractions}
        return render(request, "author/interaction/interactionsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AuthorAddInteractions(request):
    if request.user.is_authenticated and request.user.category == 'author':
        if 'drug' in request.path:
            context = { "title": "Add Drug Interactions", "activeNav": 'drin', "form": AwsDynamoDb.AuthorDrugInteractionsForm(author = request.user)}
        elif 'food' in request.path:
            context = { "title": "Add Food Interactions", "activeNav": 'fin', "form": AwsDynamoDb.AuthorFoodInteractionsForm(author = request.user)}
        elif 'disease' in request.path:
            context = { "title": "Add Disease Interactions", "activeNav": 'din', "form": AwsDynamoDb.AuthorDiseaseInteractionsForm(author = request.user)}
        if request.method == "POST":
            if 'drug' in request.path:
                context['form'] = AwsDynamoDb.AuthorDrugInteractionsForm(request.POST, author=request.user)
            elif 'food' in request.path:
                context['form'] = AwsDynamoDb.AuthorFoodInteractionsForm(request.POST, author=request.user)
            elif 'disease' in request.path:
                context['form'] = AwsDynamoDb.AuthorDiseaseInteractionsForm(request.POST, author=request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect(request.path[:-4])
        return render(request, "author/interaction/addEditinteractions.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AuthorEditInteractions(request, id):
    try:
        if 'drug' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "drin", "form": AwsDynamoDb.AuthorDrugInteractionsForm(instance = get_object_or_404(AwsDynamoDb.drug_interactions, id = id))}
        elif 'food' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "fin", "form": AwsDynamoDb.AuthorFoodInteractionsForm(instance = get_object_or_404(AwsDynamoDb.food_interactions, id = id))}
        elif 'disease' in request.path:
            context = { "title": "Edit Interactions", "activeNav": "din", "form": AwsDynamoDb.AuthorDiseaseInteractionsForm(instance = get_object_or_404(AwsDynamoDb.disease_interactions, id = id))}
    except:
        return redirect(request.path)
    if request.user.is_authenticated and request.user.category == 'author':
        if request.method == "POST":
            if 'drug' in request.path:
                context['form'] = AwsDynamoDb.AuthorDrugInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.drug_interactions, id = id))
            elif 'food' in request.path:
                context['form'] = AwsDynamoDb.AuthorFoodInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.food_interactions, id = id))
            elif 'disease' in request.path:
                context['form'] = AwsDynamoDb.AuthorDiseaseInteractionsForm(request.POST, instance = get_object_or_404(AwsDynamoDb.disease_interactions, id = id))
            if context['form'].is_valid():
                context['form'].save()
                return redirect(request.path)
        return render(request, "author/interaction/addEditinteractions.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this resource.")
def AuthorAllPillIdentification(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.pill.objects.filter(author = request.user).order_by('name').values('id', 'name', 'generic_name', 'status', 'imprint_side_1', 'imprint_side_2', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allPills = paginator.page(page)
        except PageNotAnInteger:
            allPills = paginator.page(1)
        except EmptyPage:
            allPills = paginator.page(paginator.num_pages)
        context = {"title": "Pill Identification", "activeNav": "pi", 'table_name': 'All Pills Registered', 'allPills': allPills.object_list, 'page_obj': allPills, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/pillIdentification/pillIdentificationTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddPillIdentification(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = {"title": "Add Pills for Identification", "activeNav": "pi", 'form': AwsDynamoDb.AuthorPillForm(author = request.user), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorPillForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/author/pillidentification")
        return render(request, "author/pillIdentification/addEditpill.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditPillIdentification(request, id):
    try:
        pillData = get_object_or_404(AwsDynamoDb.pill, id = id)
    except:
        return redirect("/author/pillidentification")
    if request.user.is_authenticated and request.user.category == 'author' and pillData:
        context = {"title": "Edit Pills for Identification", "activeNav": "pi", 'form': AwsDynamoDb.PillForm(instance = pillData), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.PillForm(request.POST, request.FILES, instance = pillData)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/author/pillidentification/"+id)
        return render(request, "author/pillIdentification/addEditpill.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAllNEWS(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.news.objects.filter(author = request.user).order_by('-last_updated').values('permalink', 'title', 'category', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allNews = paginator.page(page)
        except PageNotAnInteger:
            allNews = paginator.page(1)
        except EmptyPage:
            allNews = paginator.page(paginator.num_pages)
        context = {"title": "NEWS", "activeNav": "ne", 'table_name': 'All NEWS', 'allNews': allNews.object_list, "page_obj": allNews, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/news/newsTable.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddNEWS(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = {"title": "Write NEWS", "activeNav": "ne", 'form': AwsDynamoDb.AuthorNewsForm(author = request.user), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorNewsForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/author/news")
        return render(request, "author/news/addEditNEWS.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditNEWS(request, permalink):
    try:
        newsData = get_object_or_404(AwsDynamoDb.news, permalink = permalink)
    except:
        return redirect("/author/news")
    if request.user.is_authenticated and request.user.category == 'author' and newsData:
        author = AwsDynamoDb.User.objects.get(id = newsData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit NEWS", "activeNav": "ne", 'form': AwsDynamoDb.AuthorNewsForm(instance = newsData), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.AuthorNewsForm(request.POST, request.FILES, instance = newsData)
            if context['form'].is_valid():
                AwsDynamoDb.news.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/author/news/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "author/news/addEditNEWS.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAllConditions(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.condition.objects.filter(author = request.user).order_by('-last_updated').values('permalink', 'heading', 'category', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allConditions = paginator.page(page)
        except PageNotAnInteger:
            allConditions = paginator.page(1)
        except EmptyPage:
            allConditions = paginator.page(paginator.num_pages)
        context = {"title": "Conditions", "activeNav": "con", 'table_name': 'All Conditions', 'allConditions': allConditions.object_list, "page_obj": allConditions, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/conditions/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddConditions(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = {"title": "Write Conditions", "activeNav": "con", 'form': AwsDynamoDb.AuthorConditionsForm(author = request.user), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorConditionsForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect('/author/conditions')
        return render(request, "author/conditions/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditConditions(request, permalink):
    try:
        conditionData = get_object_or_404(AwsDynamoDb.condition, permalink = permalink)
    except:
        return redirect("/author/conditions")
    if request.user.is_authenticated and request.user.category == 'author' and conditionData:
        author = AwsDynamoDb.User.objects.get(id = conditionData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Conditions", "activeNav": "con", 'form': AwsDynamoDb.AuthorConditionsForm(instance = conditionData), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorConditionsForm(request.POST, request.FILES, instance = conditionData)
            if context['form'].is_valid():
                AwsDynamoDb.news.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/author/conditions/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "author/conditions/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAllWellBeing(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.well_being.objects.filter(author = request.user).order_by('-last_updated').values('permalink', 'title', 'category', 'seo_keywords', 'status', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allWellBeing = paginator.page(page)
        except PageNotAnInteger:
            allWellBeing = paginator.page(1)
        except EmptyPage:
            allWellBeing = paginator.page(paginator.num_pages)
        context = {"title": "Well Being", "activeNav": "we", 'table_name': 'All WellBeing', 'allWellBeing': allWellBeing.object_list, "page_obj": allWellBeing, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/wellbeing/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddWellBeing(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = {"title": "Write Well Being", "activeNav": "we", 'form': AwsDynamoDb.AuthorWellBeingForm(author = request.user), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorWellBeingForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/author/wellbeing")
        return render(request, "author/wellbeing/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditWellBeing(request, permalink):
    try:
        wellbeingData = get_object_or_404(AwsDynamoDb.well_being, permalink = permalink, author = request.user)
    except:
        return redirect("/author/wellbeing")
    if request.user.is_authenticated and request.user.category == 'author' and wellbeingData:
        author = AwsDynamoDb.User.objects.get(id = wellbeingData.author_id)
        author = {"name": author.first_name + " " + author.last_name, "link": author.username}
        context = {"title": "Edit Well Being", "activeNav": "we", 'form': AwsDynamoDb.AuthorWellBeingForm(instance = wellbeingData), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.AuthorWellBeingForm(request.POST, request.FILES, instance = wellbeingData)
            if context['form'].is_valid():
                AwsDynamoDb.news.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/author/wellbeing/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "author/wellbeing/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAllAllergies(request):
    if request.user.is_authenticated and request.user.category == 'author':
        paginator = Paginator(list(AwsDynamoDb.allergies.objects.filter(author = request.user).select_related('author').order_by('name').values('permalink', 'name', 'status', 'author__first_name', 'last_updated')), 500)
        page = request.GET.get('page')
        try:
            allergies = paginator.page(page)
        except PageNotAnInteger:
            allergies = paginator.page(1)
        except EmptyPage:
            allergies = paginator.page(paginator.num_pages)
        context = {"title": "Allergies", "activeNav": "al", 'table_name': 'All Allergies', 'allergies': allergies.object_list, 'page_obj': allergies, "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        return render(request, "author/allergies/table.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorAddAllergies(request):
    if request.user.is_authenticated and request.user.category == 'author':
        context = {"title": "Add Allergies", "activeNav": "al", 'form': AwsDynamoDb.AuthorAllergiesForm(author = request.user), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == 'POST':
            context['form'] = AwsDynamoDb.AuthorAllergiesForm(request.POST, request.FILES, author = request.user)
            if context['form'].is_valid():
                context['form'].save()
                return redirect("/author/allergies")
        return render(request, "author/allergies/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
def AuthorEditAllergies(request, permalink):
    try:
        pillData = get_object_or_404(AwsDynamoDb.allergies, permalink = permalink)
    except:
        return redirect("/author/pillidentification")
    if request.user.is_authenticated and request.user.category == 'author' and pillData:
        context = {"title": "Edit Allergies", "activeNav": "al", 'form': AwsDynamoDb.AuthorAllergiesForm(instance = pillData), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first()}
        if request.method == "POST":
            context['form'] = AwsDynamoDb.AuthorAllergiesForm(request.POST, request.FILES, instance = pillData)
            if context['form'].is_valid():
                AwsDynamoDb.allergies.objects.filter(permalink = permalink).delete()
                context['form'].save()
                return redirect("/author/allergies/"+context['form'].cleaned_data.get('permalink'))
        return render(request, "author/allergies/addEdit.html", context)
    else:
        return HttpResponseForbidden("You do not have permission to access this.")
#################################################################################################################################################################
################################################################## Author Views Starts Here #####################################################################
#################################################################################################################################################################

######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################


#################################################################################################################################################################
################################################################### Auth Views Starts Here ######################################################################
#################################################################################################################################################################

# Login Views Starts Here
def LoginUrl(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/"+ADMIN_PATH)
        elif request.user.category == 'author':
            return redirect('/author')
        elif request.user.category == 'user':
            return redirect('/account/overview')
    else:
        context = {
            'title': 'Login',
            'error': False,
            "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(),
            
            "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(),
            'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 
            'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))
        }
        if request.method == 'POST':
            user_data = User.objects.filter(Q(username=request.POST.get('usernameemail')) | Q(email=request.POST.get('usernameemail'))).first()
            if user_data:
                user = authenticate(username = user_data.username, password=request.POST.get('password'))
                if (user is not None) and (not user.is_superuser):
                    login(request, user)
                    if user.category == 'author':
                        return redirect('/author')
                    elif user.category == 'user':
                        return redirect('/account/overview')
                    else:
                        return redirect('/')
                else:
                    context['error'] = 'Invalid username or password.'
            else:
                    context['error'] = 'Invalid username or password.'
        return render(request, "auth/signin.html", context)
# Login Views Ends Here

# Register Views Starts Here
def RegisterUrl(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/"+ADMIN_PATH)
        elif request.user.category == 'author':
            return redirect('/author')
        elif request.user.category == 'user':
            return redirect('/account/overview')
    else:
        context = {'title': 'Register', 'error': False, "form": AwsDynamoDb.UserRegistrationForm(), "GoogleTagId": AwsDynamoDb.HomePage.objects.values_list('GoogleTagId', flat = True).first(), "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))}
        if request.method == "POST":
            context["form"] = AwsDynamoDb.UserRegistrationForm(request.POST)
            if not context["form"].errors:
                context["form"]
                user = AwsDynamoDb.User(username=context["form"].cleaned_data['email'], email=context["form"].cleaned_data['email'], date_of_birth=context["form"].cleaned_data['date_of_birth'])
                user.set_password(context["form"].cleaned_data['password'])
                user.save()
                return redirect("/signin")
        return render(request, "auth/register.html", context)
# Register Views Ends Here

# Logout Views Starts Here
def Logout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('/')
# Logout Views Ends Here

#################################################################################################################################################################
################################################################### Auth Views Ends Here ########################################################################
#################################################################################################################################################################
@require_GET
def search_data_here(request):
    try:
        from urllib.parse import urlparse
        if urlparse(request.META.get('HTTP_REFERER') or request.META.get('HTTP_ORIGIN')).netloc.split(':')[0] in ALLOWED_HOSTS:
            db = request.GET.get('database', '')
            parameter = request.GET.get('parameter', '')

            if db == 'drugs' and len(parameter) > 1:
                drugs = list(AwsDynamoDb.drug_search.objects.filter(name__istartswith=parameter.lower(), off_market_drug=False).order_by('name').distinct('name').values("permalink", "name")) or []
                return JsonResponse(drugs, safe=False, status=200)

            elif db == 'drugsoff' and len(parameter) > 1:
                drugs = list(AwsDynamoDb.drug_search.objects.filter(name__istartswith=parameter.lower(), off_market_drug=True).order_by('name').distinct('name').values("permalink", "name")) or []
                return JsonResponse(drugs, safe=False, status=200)

            elif db == 'drugscondition' and len(parameter) > 1:
                conditions = list(AwsDynamoDb.drug_search.objects.filter(off_market_drug=False).filter(condition__istartswith=parameter.lower(), condition__isnull=False, condition__gt='').values_list('condition', flat=True).distinct())
                return JsonResponse(conditions, safe=False, status=200 if conditions else 204)

            elif db == 'interaction-checker' and len(parameter) > 1:
                data = {'drugs': list({record['name']: record for record in AwsDynamoDb.drug_search.objects.filter(Q(name__istartswith=parameter), Q(off_market_drug=False), Q(generic_name__isnull=False), Q(generic_name__gt=''), Q(name__gt='')).order_by('name').values("generic_name", "name", "id")}.values()), 'generic_names': [name.strip() for name in set(name for names in AwsDynamoDb.drug_search.objects.filter(off_market_drug=False).values_list('generic_name', flat=True) for name in names.split('|')) if name.strip().lower().startswith(parameter.lower())]}
                return JsonResponse(data, safe=False, status=200 if data else 204)

            elif db == 'imprint' and len(parameter) > 1:
                data = list(set(value for tup in AwsDynamoDb.pill.objects.filter(Q(imprint_side_1__istartswith=parameter) | Q(imprint_side_2__istartswith=parameter)).distinct().values_list('imprint_side_1', 'imprint_side_2') for value in tup))
                return JsonResponse(data, safe=False, status=200 if data else 204)

            else:
                return JsonResponse({'You are not allowed': 'Not allowed'}, safe=False, status=200)
        else:
            return JsonResponse({'You are not allowed': 'Not allowed'}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=200)

def error_page_not_found(request, exception=None):
    return render(request, "error.html", {"title": "Not Found", "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))}, status = 404)
def error_page_internal_server_error(request, exception=None):
    return render(request, "error.html", {"title": "Internal Server Error", "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))}, status = 500)
def error_page_forbidden(request, exception=None):
    return render(request, "error.html", {"title": "Forbidden", "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))}, status = 403)
def error_page_bad_request(request, exception=None):
    return render(request, "error.html", {"title": "Bad Request", "SOCIAL_LINK": AwsDynamoDb.HomePage.objects.first(), 'header_pages': list(AwsDynamoDb.header_page.objects.all().values('title', 'category', 'permalink')), 'footer_pages': list(AwsDynamoDb.footer_page.objects.all().values('title', 'category', 'permalink'))}, status = 400)