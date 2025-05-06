from app import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap

handler404 = 'app.views.error_page_not_found'
handler500 = 'app.views.error_page_internal_server_error'
handler403 = 'app.views.error_page_forbidden'
handler400 = 'app.views.error_page_bad_request'

def robots_txt(request):
    from app.models import HomePage
    return HttpResponse(HomePage.objects.first().robots, content_type="text/plain")

urlpatterns = [
    path('robots.txt', robots_txt, name='robots_txt'),
    # path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap, 'drugs': DrugSitemap, 'vitaminsandsupplements': VitaminAndSupplementSitemap, 'news': NewsSitemap, 'careers': CareerSitemap}}, name='sitemap'),
    #######################################################################################################################
    ############################################### Auth Routes Starts Here ###############################################
    #######################################################################################################################
    path('signin/', views.LoginUrl, name='Login Path'),
    path('register/', views.RegisterUrl, name='Register Path'),
    path('logout/', views.Logout, name='logout'),
    #######################################################################################################################
    ############################################# Users Routes Starts Here ################################################
    #######################################################################################################################
    path("user/profiles/", views.UserProfiles, name='User Profile'),
    path("user/profiles/add/", views.UserProfilesAdd, name='Add User Profile'),
    path("user/profiles/<str:id>/", views.UserProfilesView, name='View User Profile'),
    path("user/profiles/edit/<str:id>/", views.UserProfilesEdit, name='Edit User Profile'),
    path("user/profiles/delete/<str:id>/", views.UserProfilesDelete, name='Delete User Profile'),
    path("user/profiles/<str:id>/<str:category>/", views.UserProfilesViewItem, name='User Profile Item'),
    path("user/profiles/<str:id>/<str:category>/add/", views.UserProfilesViewItemAdd, name='Add User Profile Item'),
    path("user/profiles/<str:id>/<str:category>/<str:item_id>/", views.UserProfilesViewItemView, name='View User Profile Item'),
    path("user/profiles/<str:id>/<str:category>/edit/<str:item_id>/", views.UserProfilesViewItemEdit, name='Edit User Profile Item'),
    path("user/profiles/<str:id>/<str:category>/delete/<str:item_id>/", views.UserProfilesViewItemDelete, name='Delete User Profile Item'),
    path("user/qna/", views.QNA, name='Question Answers'),
    path("user/qna/questions/", views.Questions, name='Questions'),
    path("user/qna/questions/ask/", views.AskAQuestion, name='Ask Questions'),
    path("user/support-groups/", views.support_groups, name='Support Groups'),



    path("account/overview/", views.SettingsAccountOverview, name='Settings Account Overview'),
    path("account/details/", views.SettingsAccountDetails, name='Settings Account Details'),
    path("account/details/closeaccount/", views.SettingsAccountDetailsCloseAccount, name='Settings Account Details'),
    path("account/subscription/", views.SettingsAccountSubscription, name='Settings Account Subscription'),



    #######################################################################################################################
    ############################################## Users Routes Ends Here #################################################
    #######################################################################################################################

    #######################################################################################################################
    ############################################# Author Routes Starts Here ###############################################
    #######################################################################################################################
    path("author/", views.AuthorDashboard, name='Author Dashboard'),
    path("author/drugs/", views.AuthorDrugs, name='Author Drugs'),
    path("author/drugs/add/", views.AuthorDrugsAdd, name='Add Author Drugs'),
    path("author/drugs/<str:permalink>/", views.AuthorDrugsEdit, name='Edit Author Drugs'),
    path("author/drugs/faqs/add/", views.AuthorAddDrugFAQ, name='Author Add FAQ to drug Drugs'),
    path("author/drugs/faqs/edit/<str:id>/", views.AuthorEditDrugFAQ, name='Author Edit FAQ to drug Drugs'),
    path("author/vitamins/", views.AuthorVitaminsAndSupplements, name='Author Vitamins'),
    path("author/vitamins/add/", views.AuthorVitaminsAndSupplementsAdd, name='Add Author Vitamins'),
    path("author/vitamins/<str:permalink>/", views.AuthorVitaminsAndSupplementsEdit, name='Edit Author Vitamins'),
    path("author/vitamins/faqs/add/", views.AuthorAddVitaminsAndSupplementsFAQ, name='Author Add FAQ to Vitamins'),
    path("author/vitamins/faqs/edit/<str:id>/", views.AuthorEditVitaminsAndSupplementsFAQ, name='Author Edit FAQ to Vitamins'),
    path("author/drug-interactions/", views.AuthorAllInteractions, name='Author Drug Interactions'),
    path("author/food-interactions/", views.AuthorAllInteractions, name='Author Food Interactions'),
    path("author/disease-interactions/", views.AuthorAllInteractions, name='Author Disease Interactions'),
    path("author/drug-interactions/add/", views.AuthorAddInteractions, name='Author Add Drug Interactions'),
    path("author/food-interactions/add/", views.AuthorAddInteractions, name='Author Add Food Interactions'),
    path("author/disease-interactions/add/", views.AuthorAddInteractions, name='Author Add Disease Interactions'),
    path("author/drug-interactions/<str:id>/", views.AuthorEditInteractions, name='Author Edit Drug Interactions'),
    path("author/food-interactions/<str:id>/", views.AuthorEditInteractions, name='Author Edit Food Interactions'),
    path("author/disease-interactions/<str:id>/", views.AuthorEditInteractions, name='Author Edit Disease Interactions'),
    path("author/pillidentification/", views.AuthorAllPillIdentification, name='Author Pill Identification'),
    path("author/pillidentification/add/", views.AuthorAddPillIdentification, name='Author Add Pill Identification'),
    path("author/pillidentification/<str:id>/", views.AuthorEditPillIdentification, name='Author Edit Pill Identification'),
    path("author/news/", views.AuthorAllNEWS, name='Author NEWS Post'),
    path("author/news/add/", views.AuthorAddNEWS, name='Author Add NEWS Post'),
    path("author/news/<str:permalink>/", views.AuthorEditNEWS, name='Author Edit NEWS Post'),
    path("author/conditions/", views.AuthorAllConditions, name='Author All Conditions'),
    path("author/conditions/add/", views.AuthorAddConditions, name='Author Add Conditions'),
    path("author/conditions/<str:permalink>/", views.AuthorEditConditions, name='Author Edit Conditions'),
    path("author/wellbeing/", views.AuthorAllWellBeing, name='Author All Well Being'),
    path("author/wellbeing/add/", views.AuthorAddWellBeing, name='Author Add Well Being'),
    path("author/wellbeing/<str:permalink>/", views.AuthorEditWellBeing, name='Author Edit Well Being'),
    path("author/allergies/", views.AuthorAllAllergies, name='Author All Allergies'),
    path("author/allergies/add/", views.AuthorAddAllergies, name='Author Add Allergies'),
    path("author/allergies/<str:permalink>/", views.AuthorEditAllergies, name='Author Well Allergies'),
    #######################################################################################################################
    ############################################## Author Routes Ends Here ################################################
    #######################################################################################################################


    #######################################################################################################################
    ############################################## Admin Routes Starts Here ###############################################
    #######################################################################################################################
    path(settings.ADMIN_PATH+"", views.DashBoard, name='Dashboard'),
    path(settings.ADMIN_PATH+"pages/<str:category>/", views.Pages, name='Header Pages'),
    path(settings.ADMIN_PATH+"pages/<str:category>/add/", views.AddPages, name='Add Header Page'),
    path(settings.ADMIN_PATH+"pages/<str:category>/<str:permalink>/", views.EditPages, name='Edit Header Page'),
    path(settings.ADMIN_PATH+"pages/<str:category>/delete/<str:permalink>/", views.DeletePages, name='Delete Header Page'),
    path(settings.ADMIN_PATH+"drugs/", views.AllSearchDrugs, name='All Drugs'),
    path(settings.ADMIN_PATH+"drugs/add/", views.AddDrugsSearch, name='Add Drugs'),
    path(settings.ADMIN_PATH+"drugs/<str:id>/", views.EditDrugsSearch, name='Edit Drugs'),
    path(settings.ADMIN_PATH+"drugs/delete/<str:id>/", views.DeleteDrugsSearch, name='Delete Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/", views.AllDrugs, name='All Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/add/", views.AddDrugs, name='Add Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/<str:permalink>/", views.EditDrugs, name='Edit Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/delete/<str:permalink>/", views.DeleteDrugs, name='Delete Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/faqs/add/", views.AddDrugFAQ, name='Add FAQ to drug Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/faqs/edit/<str:id>/", views.EditDrugFAQ, name='Edit FAQ to drug Articles Drugs'),
    path(settings.ADMIN_PATH+"drug-articles/faqs/delete/<str:id>/", views.DeleteDrugFAQ, name='Delete FAQ to drug Articles Drugs'),
    path(settings.ADMIN_PATH+"vitamins/", views.allVitaminsAndSupplements, name='Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/add/", views.addVitaminsAndSupplements, name='Add Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/<str:permalink>/", views.editVitaminsAndSupplements, name='Edit Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/delete/<str:permalink>/", views.deleteVitaminsAndSupplements, name='Delete Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/faqs/add/", views.AddVitaminsAndSupplementsFAQ, name='Add FAQ Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/faqs/edit/<str:id>/", views.EditVitaminsAndSupplementsFAQ, name='Edit FAQ Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"vitamins/faqs/delete/<str:id>/", views.DeleteVitaminsAndSupplementsFAQ, name='Delete FAQ Vitamins and Supplements'),
    path(settings.ADMIN_PATH+"drug-interactions/", views.AllInteractions, name='Drug Interactions'),
    path(settings.ADMIN_PATH+"food-interactions/", views.AllInteractions, name='Food Interactions'),
    path(settings.ADMIN_PATH+"disease-interactions/", views.AllInteractions, name='Disease Interactions'),
    path(settings.ADMIN_PATH+"drug-interactions/add/", views.AddInteractions, name='Add Drug Interactions'),
    path(settings.ADMIN_PATH+"food-interactions/add/", views.AddInteractions, name='Add Food Interactions'),
    path(settings.ADMIN_PATH+"disease-interactions/add/", views.AddInteractions, name='Add Disease Interactions'),
    path(settings.ADMIN_PATH+"drug-interactions/<str:id>/", views.EditInteractions, name='Edit Drug Interactions'),
    path(settings.ADMIN_PATH+"food-interactions/<str:id>/", views.EditInteractions, name='Edit Food Interactions'),
    path(settings.ADMIN_PATH+"disease-interactions/<str:id>/", views.EditInteractions, name='Edit Disease Interactions'),
    path(settings.ADMIN_PATH+"drug-interactions/delete/<str:id>/", views.DeleteInteractions, name='Delete Drug Interactions'),
    path(settings.ADMIN_PATH+"food-interactions/delete/<str:id>/", views.DeleteInteractions, name='Delete Food Interactions'),
    path(settings.ADMIN_PATH+"disease-interactions/delete/<str:id>/", views.DeleteInteractions, name='Delete Disease Interactions'),
    path(settings.ADMIN_PATH+"pillidentification/", views.AllPillIdentification, name='Pill Identification'),
    path(settings.ADMIN_PATH+"pillidentification/add/", views.AddPillIdentification, name='Add Pill Identification'),
    path(settings.ADMIN_PATH+"pillidentification/<str:id>/", views.EditPillIdentification, name='Edit Pill Identification'),
    path(settings.ADMIN_PATH+"pillidentification/delete/<str:id>/", views.DeletePillIdentification, name='Delete Pill Identification'),
    path(settings.ADMIN_PATH+"allergies/", views.AllAllergies, name='Allergies'),
    path(settings.ADMIN_PATH+"allergies/add/", views.AddAllergies, name='Add Allergies'),
    path(settings.ADMIN_PATH+"allergies/<str:permalink>/", views.EditAllergies, name='Edit Allergies'),
    path(settings.ADMIN_PATH+"allergies/delete/<str:permalink>/", views.DeleteAllergies, name='Delete Allergies'),
    path(settings.ADMIN_PATH+"news/", views.AllNEWS, name='NEWS Post'),
    path(settings.ADMIN_PATH+"news/add/", views.AddNEWS, name='Add NEWS Post'),
    path(settings.ADMIN_PATH+"news/<str:permalink>/", views.EditNEWS, name='Edit NEWS Post'),
    path(settings.ADMIN_PATH+"news/delete/<str:permalink>/", views.DeleteNEWS, name='Delete NEWS Post'),
    path(settings.ADMIN_PATH+"conditions/", views.AllConditions, name='All Conditions'),
    path(settings.ADMIN_PATH+"conditions/add/", views.AddConditions, name='Add Conditions'),
    path(settings.ADMIN_PATH+"conditions/<str:permalink>/", views.EditConditions, name='Edit Conditions'),
    path(settings.ADMIN_PATH+"conditions/delete/<str:permalink>/", views.DeleteConditions, name='Delete Conditions'),
    path(settings.ADMIN_PATH+"wellbeing/", views.AllWellBeing, name='All Well Being'),
    path(settings.ADMIN_PATH+"wellbeing/add/", views.AddWellBeing, name='Add Well Being'),
    path(settings.ADMIN_PATH+"wellbeing/<str:permalink>/", views.EditWellBeing, name='Edit Well Being'),
    path(settings.ADMIN_PATH+"wellbeing/delete/<str:permalink>/", views.DeleteWellBeing, name='Delete Well Being'),
    path(settings.ADMIN_PATH+"users/", views.AllUsers, name='All Users'),
    path(settings.ADMIN_PATH+"users/<str:id>/", views.ViewUser, name='View User'),
    path(settings.ADMIN_PATH+"users/delete/<str:id>/", views.DeleteUser, name='Delete User'),
    path(settings.ADMIN_PATH+"writer/", views.AllWriter, name='All Writers'),
    path(settings.ADMIN_PATH+"writer/add/", views.AddWriter, name='Add Writer'),
    path(settings.ADMIN_PATH+"writer/<str:id>/", views.EditWriter, name='Edit Writer'),
    path(settings.ADMIN_PATH+"writer/delete/<str:id>/", views.DeleteWriter, name='Delete Writer'),
    path(settings.ADMIN_PATH+"contactus/", views.ContactUsMessages, name='Contact Us Messages'),
    path(settings.ADMIN_PATH+"contactus/<str:id>/", views.SpecificContactMessage, name='Specific Contact Us Message'),
    path(settings.ADMIN_PATH+"sessions/", views.Sessions, name='Sessions'),
    path(settings.ADMIN_PATH+"sessions/<str:session_key>", views.Session, name='Specific Session'),
    path(settings.ADMIN_PATH+"settings/", views.AdminSettings, name='Settings'),
    path(settings.ADMIN_PATH+"changehomepage/", views.EditHomePage, name='Edit HomePage'),
    path(settings.ADMIN_PATH+"changegoogletagid/", views.ChangeGoogleTagId, name='Change GoogleTagId'),
    path(settings.ADMIN_PATH+'login/', views.AdminLogin, name = 'AdminLogin'),
    path(settings.ADMIN_PATH+'force_logout/<str:session_key>/', views.force_logout, name = 'Force Logout'),
    #######################################################################################################################
    ############################################### Admin Routes Ends Here ################################################
    #######################################################################################################################
    path('ckeditor/', include("ckeditor_uploader.urls")),


        #######################################################################################################################
    ############################################### Auth Routes Ends Here #################################################
    #######################################################################################################################

    #######################################################################################################################
    ############################################# Global Routes Starts Here ###############################################
    #######################################################################################################################
    path("", views.HomePage, name='HomePage'),
    path('specific_database_search/', views.search_data_here, name='Search Whole Website'),
    path("drugs/", views.drugsPage, name='Drugs Page'),
    path("drugs/off-market/<str:slug>", views.drugsOffMarketPage, name='Off Market Drugs Page'),
    path("drugs/conditions/", views.drugsConditionsPage, name='Conditions Drugs Page'),
    path("drugs/conditions/alpha/<str:slug>", views.drugsConditionsCategoryPage, name='Conditions Category Drugs Page'),
    path("drugs/alpha/<str:slug>/", views.drugsCategoryPage, name='Drug Category Page'),
    path("vitamins/", views.vitaminsAndSupplementsPage, name='Vitamins and Supplements Page'),
    path("vitamins/alpha/<str:slug>/", views.vitaminsAndSupplementsCategoryPage, name='Category Vitamins and Supplements Page'),
    path("pill-identifier/", views.pillIdentifier, name='Pills Identifier Page'),
    path("imprints/<str:permalink>", views.show_pill, name='Pills Imprint Page'),
    path("interaction-checker/", views.interactionChecker, name='Interaction Checker Page'),
    path("interaction-checker/interactions", views.checkerInteractions, name='Check Interactions Page'),
    path("conditions/", views.conditionsPage, name='Conditions Page'),
    path("conditions/<str:category>/", views.conditionsPage, name='Conditions Category Page'),
    path("conditions/<str:category>/<str:slug>", views.conditionsPage, name='Conditions Category and Specific Page'),
    path("well-being/", views.WellBeing, name='Well Being Page'),
    path("well-being/<str:category>/", views.WellBeing, name='WellBeing Category Page'),
    path("well-being/<str:category>/<str:slug>", views.WellBeing, name='WellBeing Category and Specific Page'),
    path("news/", views.news, name='News Page'),
    path("news/<str:permalink>/", views.news, name='Specific News Page'),
    path("contactus/", views.contactUs, name='Contact Us Page'),
    path("sitemap/", views.Sitemap, name='Sitemap'),
    path('<str:slug>/', views.GlobalPages, name='All Pages of Website'),
    #######################################################################################################################
    ############################################## Global Routes Ends Here ################################################
    #######################################################################################################################
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)