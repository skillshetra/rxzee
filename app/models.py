from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now

def generate_unique_id():
    from uuid import uuid4
    return str(uuid4()).replace('-', '')[:20]

class HomePage(models.Model):
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 1, primary_key = True, default = '1', editable = False)
    search_drug_conditions = models.BooleanField(default = True)
    slider = models.BooleanField(default = True)
    healthy_life = models.BooleanField(default = True)
    health_az = models.BooleanField(default = True)
    top_news = models.BooleanField(default = True)
    twitter = models.URLField(default = 'https://x.com/rxzee')
    youtube = models.URLField(default = 'https://youtube.com/rxzee')
    facebook = models.URLField(default = 'https://facebook.com/rxzee')
    linkedin = models.URLField(default = 'https://linkedin.com/rxzee')
    instagram = models.URLField(default = 'https://instagram.com/rxzee')
    GoogleTagId = models.CharField(max_length = 50, default = 'GTM-XXXXXX')
    GoogleSearchConsoleId = models.CharField(max_length = 200, default = 'Search Console Id')
    robots = models.TextField(default = "User-agent: *\nDisallow: /")
############## Users Model in Website Starts Here ##############
class User(AbstractUser):
    def __str__(self):
        return self.username
    def clean(self):
        from re import match
        super().clean()
        if self.phone_number:
            if not match(r'^\d{10}$', self.phone_number):
                raise ValidationError({'phone_number': 'Phone number must be exactly 10 digits.'})
        if self.date_of_birth:
            age = (now().date() - self.date_of_birth).days // 365
            if age < 18:
                raise ValidationError({'date_of_birth': 'You must be at least 18 years old.'})
    email = models.EmailField(unique=True)
    category = models.CharField(max_length = 20, choices = [('user', 'User'), ('author', 'Author'), ('admin', 'Admin')], default='user')
    phone_number = models.CharField(max_length = 10)
    address = models.TextField()
    date_of_birth = models.DateField(blank = True)
    link = models.URLField()
    every_day_mednews = models.BooleanField(default = True)
    monthly_newsletter = models.BooleanField(default = True)
    monthly_newsletter_health_care = models.BooleanField(default = True)
    FDA_approvals_for_drugs = models.BooleanField(default = False)
    FDA_safety_alerts = models.BooleanField(default = False)
    supporters = models.BooleanField(default = False)
    notice_of_projects_for_eDetailing = models.BooleanField(default = False)
    notice_of_CME_events = models.BooleanField(default = False)
    groups = models.ManyToManyField('auth.Group', related_name = 'custom_user_set', blank = True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank = True)
############## User Delete Account Model in Website Starts Here ##############

class UserDeleteAccount(AbstractUser):
    def __str__(self):
        return self.user_full_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        User.objects.filter(username = self.user_username).first().delete()
    user_username = models.CharField(max_length = 255)
    user_full_name = models.CharField(max_length = 255)
    closure_reason = models.TextField(max_length = 1000, blank = True, default = "")
    data_of_deletion = models.DateTimeField(auto_now = True)
############## User Delete Account Model in Website Ends Here ##############

############## User Session Account Model in Website Starts Here ##############
class UserSession(models.Model):
    def __str__(self):
        return f"{self.user.username} - {self.session_key}"
    session_key = models.CharField(max_length = 40, primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length = 100, default = '')
    region = models.CharField(max_length = 100, default = '')
    city = models.CharField(max_length = 100, default = '')
    zip_code = models.CharField(max_length = 100, default = '')
    user_agent = models.TextField()
    session_expiration = models.DateTimeField(null = True, blank = True)
    is_active = models.BooleanField(default = True)
    last_activity = models.DateTimeField(auto_now = True)
############## User Session Account Model in Website Ends Here ##############

############## Allergies Model in Website Starts Here ##############
class allergies(models.Model):
    def __str__(self):
        return self.name
    permalink = models.CharField(max_length=200, primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    content = RichTextUploadingField(blank = True, default = "")
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.CharField(max_length = 200)
    search_count = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'AllerigiesAuthor')
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Allergies Model in Website Ends Here ##############

############## Drugs Model in Website Starts Here ##############
class drug_search(models.Model):
    def __str__(self):
        return f'{self.condition} - {self.name}'
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    name = models.CharField(max_length = 150, default = "")
    condition = models.CharField(max_length = 120, default = "")
    generic_name = models.CharField(max_length = 200, default = "")
    drug_class = models.CharField(max_length = 150, default = "")
    type = models.CharField(max_length = 10, default = "")
    permalink = models.CharField(max_length = 150, default = "")
    off_market_drug = models.BooleanField(default = False)
    label = models.CharField(max_length = 10, default = "")
    search_count = models.IntegerField(default = 0)
class drug(models.Model):
    def __str__(self):
        return self.name
    permalink = models.CharField(max_length = 200, primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    generic_name = models.CharField(max_length = 250, blank = True, default = "")
    brand_name = models.CharField(max_length = 250, blank = True, default = "")
    pronunciation = models.CharField(max_length = 250, blank = True, default = "")
    class_name = models.CharField(max_length = 250, blank = True, default = "")
    dosage_forms = models.CharField(max_length = 250, blank = True, default = "")
    availability = models.CharField(max_length = 250, blank = True, default = "")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'DrugAuthor')
    widgets = models.CharField(max_length = 250, default="a, b, c")
    uses = RichTextUploadingField(blank = True, default = "")
    side_effects = RichTextUploadingField(blank = True, default = "")
    warnings = RichTextUploadingField(blank = True, default = "")
    precautions = RichTextUploadingField(blank = True, default = "")
    interactions = RichTextUploadingField(blank = True, default = "")
    overdose = RichTextUploadingField(blank = True, default = "")
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.CharField(max_length = 200)
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
class drugsFaq(models.Model):
    def __str__(self):
        return f"Drugs FAQ {self.id}"
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    drug = models.ForeignKey(drug, on_delete = models.CASCADE, related_name = 'drug')
    question = models.CharField(max_length = 200, help_text = "question")
    answer = models.TextField(help_text = "answer")
############## Drugs Model in Website Ends Here ##############

############## Pills Model in Website Starts Here ##############
class pill(models.Model):
    def __str__(self):
        return self.name
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    redirect_url_name = models.CharField(max_length = 150, default = "")
    redirect_url_imprint = models.CharField(max_length = 100, default = "")
    name = models.CharField(max_length = 150, default = "")
    generic_name = models.CharField(max_length = 100, default = "")
    strength = models.CharField(max_length = 50, default = "")
    imprint_side_1 = models.CharField(max_length = 50, default = "")
    imprint_side_2 = models.CharField(max_length = 50, default = "")
    color = models.CharField(max_length = 50, default = "")
    shape = models.CharField(max_length = 50, choices = [('Round', 'Round'), ('Oblong', 'Oblong'), ('Oval', 'Oval'), ('Five-Sided', 'Five-Sided'), ('Rectangular', 'Rectangular'), ('Trapezoidal', 'Trapezoidal'), ('Diamond', 'Diamond'), ('Elliptical', 'Elliptical'), ('Square', 'Square'), ('Triangular', 'Triangular'), ('Pentagon', 'Pentagon'), ('Almond', 'Almond'), ('Hexagonal', 'Hexagonal'), ('Cylindrical', 'Cylindrical'), ('Teardrop', 'Teardrop'), ('Shield', 'Shield'), ('Bullet', 'Bullet'), ('Square (Rounded Corners)', 'Square (Rounded Corners)'), ('Rectangular (Rounded End)', 'Rectangular (Rounded End)'), ('Other', 'Other')], default = 'Other')
    image = models.ImageField(upload_to = 'pills/identifier/', blank = True, null = True, max_length = 150)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'PillAuthor')
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Pills Model in Website Ends Here ################

############## Vitamins and Supplements Model in Website Starts Here ##############
class vitaminsAndSupplement(models.Model):
    def __str__(self):
        return self.name
    permalink = models.CharField(max_length = 200, primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    other_names = models.CharField(max_length = 250, blank = True, default = "")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'VitaminsAuthor')
    widgets = models.CharField(max_length = 250, default="a, b, c")
    overview = RichTextUploadingField(blank = True, default = "")
    uses = RichTextUploadingField(blank = True, default = "")
    side_effects = RichTextUploadingField(blank = True, default = "")
    precautions = RichTextUploadingField(blank = True, default = "")
    interactions = RichTextUploadingField(blank = True, default = "")
    dosing = RichTextUploadingField(blank = True, default = "")
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.CharField(max_length = 200)
    search_count = models.IntegerField(default = 0)
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
class vitaminsAndSupplementsFaq(models.Model):
    def __str__(self):
        return f"Vitamins and Supplements FAQ {self.id}"
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    vitaminsAndSupplement = models.ForeignKey(vitaminsAndSupplement, on_delete = models.CASCADE, related_name = 'vitaminsAndSupplement')
    question = models.CharField(max_length = 200, help_text="question")
    answer = models.TextField(help_text = "answer")
############## Vitamins and Supplements Model in Website Ends Here ##############

############## Interactions Model in Website Starts Here ##############
class drug_interactions(models.Model):
    def __str__(self):
        return f"Drug Interactions {self.id}"
    def clean(self):
        from django.db.models import Q
        first_drug = self.first_drug.strip().lower()
        second_drug = self.second_drug.strip().lower()
        if first_drug == second_drug:
            raise ValidationError("The same drug cannot interact with itself.")
        if drug_interactions.objects.filter((Q(first_drug=first_drug) & Q(second_drug=second_drug)) | (Q(first_drug=second_drug) & Q(second_drug=first_drug))).exists():
            raise ValidationError("This interaction between the two drugs already exists.")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    first_drug = models.CharField(max_length = 100)
    second_drug = models.CharField(max_length = 100)
    level = models.CharField(max_length = 10, choices = [('Low', 'Low'), ('Moderate', 'Moderate'), ('Major', 'Major')], default = 'Low')
    consumer = RichTextUploadingField()
    professional = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'DrugInteractionAuthor')
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
class food_interactions(models.Model):
    def __str__(self):
        return f"Food Interactions {self.id}"
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    formula = models.CharField(max_length = 50)
    header = models.CharField(max_length = 100)
    severity = models.CharField(max_length = 50)
    other_details = models.TextField(max_length = 60)
    level = models.CharField(max_length = 10, choices = [('Low', 'Low'), ('Moderate', 'Moderate'), ('Major', 'Major')], default = 'Low')
    consumer = RichTextUploadingField()
    professional = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'FoodInteractionAuthor')
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
class disease_interactions(models.Model):
    def __str__(self):
        return f"Disease Interactions {self.id}"
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    formula = models.CharField(max_length = 50)
    header = models.CharField(max_length = 100)
    severity = models.CharField(max_length = 500)
    level = models.CharField(max_length = 10, choices = [('Low', 'Low'), ('Moderate', 'Moderate'), ('Major', 'Major')], default = 'Low')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'DiseaseInteractionAuthor')
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Interactions Model in Website Ends Here ################

############## NEWS Model in Website Starts Here ##############
class news(models.Model):
    def __str__(self):
        return f"NEWS {self.permalink}"
    permalink = models.CharField(max_length = 200, primary_key = True)
    title = models.CharField(max_length = 200)
    content = RichTextUploadingField()
    category = models.CharField(max_length = 50, choices = [('Consumer', 'Consumer'), ('Drugs', 'Drugs'), ('Vitamins', 'Vitamins'), ('Pipeline', 'Pipeline'), ('Clinical Traials', 'Clinical Traials'), ('FDA Alerts', 'FDA Alerts')], default = 'Consumer')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'NewsAuthor')
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.TextField()
    featured_image = models.ImageField(upload_to = 'featured_image/')
    search_count = models.IntegerField(default = 0)
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## NEWS Model in Website Ends Here ################

############## ContactUs Model in Website Starts Here ##############
class contact(models.Model):
    def __str__(self):
        return f"Contact {self.id}"
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    subject = models.CharField(max_length = 50, choices = [('general_inquiry', 'General Inquiry'), ('support', 'Support'), ('feedback', 'Feedback'), ('complaint', 'Complaint'), ('other', 'Other')], default = 'general_inquiry')
    fullname = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    message = models.TextField(max_length = 1000)
    last_updated = models.DateTimeField(auto_now_add = True)
class ContactFile(models.Model):
    contact = models.ForeignKey(contact, related_name = 'files', on_delete=models.CASCADE)
    file = models.FileField(upload_to = 'contactus/')
############## ContactUs Model in Website Ends Here ################

############## Page Model in Website Starts Here ##############
class header_page(models.Model):
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    permalink = models.CharField(max_length = 200, primary_key = True)
    title = models.CharField(max_length = 100)
    content = RichTextUploadingField()
    category = models.CharField(max_length = 50, choices = [('drugs', 'Drugs and Supplements'), ('conditions', 'Conditions'), ('well-being', 'Well Being'), ('more', 'More')], default = 'more')
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.TextField()
    last_updated = models.DateTimeField(auto_now_add = True)
class footer_page(models.Model):
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    permalink = models.CharField(max_length = 200, primary_key = True)
    title = models.CharField(max_length = 100)
    content = RichTextUploadingField()
    category = models.CharField(max_length = 50, choices = [('About Us', 'About Us'), ('Support', 'Support'), ('Terms & Privacy', 'Terms & Privacy')], default = 'aboutus')
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.TextField()
    last_updated = models.DateTimeField(auto_now_add = True)
############## Page Model in Website Ends Here ################

############## Conditions Model in Website Starts Here ##############
class condition(models.Model):
    def __str__(self):
        return self.heading
    permalink = models.CharField(max_length = 200, primary_key = True)
    heading = models.CharField(max_length = 200)
    category = models.CharField(max_length = 200)
    sub_category = models.CharField(max_length = 200)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'ConditionsAuthor')
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.TextField()
    featured_image = models.ImageField(upload_to = 'featured_image/')
    search_count = models.IntegerField(default = 0)
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Conditions Model in Website Ends Here ##############

############## Well Being Model in Website Starts Here ##############
class well_being(models.Model):
    def __str__(self):
        return self.title
    permalink = models.CharField(max_length = 200, primary_key = True)
    title = models.CharField(max_length = 200, unique = True)
    category = models.CharField(max_length = 50, choices = [("Aging Well", "Aging Well"), ("Baby", "Baby"), ("Birth Control", "Birth Control"), ("Children's Health", "Children's Health"), ("Diet & Weight Management", "Diet & Weight Management"), ("Fitness & Exercise", "Fitness & Exercise"), ("Food & Recipes", "Food & Recipes"), ("Health & Balance", "Health & Balance"), ("Healthy Beauty", "Healthy Beauty"), ("Men's Health", "Men's Health"), ("Parenting", "Parenting"), ("Pet Health", "Pet Health"), ("Pregnancy", "Pregnancy"), ("Sex & Relationships", "Sex & Relationships"), ("Teen Health", "Teen Health"), ("Women's Health", "Women's Health")], default='Aging Well')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'WellBeingAuthor')
    seo_title = models.CharField(max_length = 200)
    seo_description = models.TextField()
    seo_keywords = models.TextField()
    featured_image = models.ImageField(upload_to = 'featured_image/')
    search_count = models.IntegerField(default = 0)
    status = models.CharField(max_length = 20, choices = [('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default = 'pending')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Well Being Model in Website Ends Here ################

############## Profile Model in Website Starts Here ##############
class UserProfile(models.Model):
    from django.core.validators import RegexValidator
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    profile_name = models.CharField(max_length=255)
    pregnancy_lactation_warnings = models.BooleanField(default=False)
    emergency_contact_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_contact_phone_number = models.CharField(max_length = 15, blank = True, null = True, validators = [RegexValidator(regex = r'^\+?1?\d{9,15}$', message = "Phone number must be in the format: '+999999999'. Up to 15 digits allowed.")])
    primary_physician_contact_name = models.CharField(max_length=255, blank=True, null=True)
    primary_physician_contact_phone_number = models.CharField(max_length = 15, blank = True, null = True, validators = [RegexValidator(regex = r'^\+?1?\d{9,15}$', message = "Phone number must be in the format: '+999999999'. Up to 15 digits allowed.")])
    other_details = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ProfileUser')
    last_updated = models.DateTimeField(auto_now_add=True)
############## Profile Model in Website Ends Here ################

############## Profile Items Model in Website Starts Here ##############
class UserProfileDrugs(models.Model):
    class Meta:
        unique_together = ('user_profile', 'drug')
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    drug = models.ForeignKey(drug, on_delete=models.CASCADE, related_name='DrugUserProfile')
    status = models.CharField(max_length = 1, choices = [('C', 'Currently taking'), ('R', 'Researching'), ('P', 'Previously taken')], default='C')
    other_details = models.TextField(blank = True, default = '', max_length = 150)
    condition = models.CharField(max_length = 12)
    dosage = models.CharField(max_length = 50, choices = [('', 'How many'), ('0.25', '¼'), ('0.5', '½'), ('1', '1'), ('1.5', '1 ½'), ('2', '2'), ('2.5', '2 ½'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('7.5', '7 ½'), ('8', '8'), ('9', '9'), ('10', '10'), ('12.5', '12 ½'), ('15', '15'), ('20', '20'), ('other', 'other')], default = '')
    dosage_form = models.CharField(max_length = 50, choices = [('', 'Form'), ('compounding powder', 'compounding powder'), ('oral capsule', 'oral capsule'), ('oral capsule, extended release', 'oral capsule, extended release'), ('oral delayed release capsule', 'oral delayed release capsule'), ('oral delayed release tablet', 'oral delayed release tablet'), ('oral gum', 'oral gum'), ('oral powder for reconstitution', 'oral powder for reconstitution'), ('oral tablet', 'oral tablet'), ('oral tablet, chewable', 'oral tablet, chewable'), ('oral tablet, disintegrating', 'oral tablet, disintegrating'), ('oral tablet, dispersible', 'oral tablet, dispersible'), ('oral tablet, extended release', 'oral tablet, extended release'), ('rectal suppository', 'rectal suppository'), ('other', 'other')], default = '')
    strength_code = models.CharField(max_length = 50, choices = [('', 'Strength'), ('1 g', '1 g'), ('1200 mg', '1200 mg'), ('125 mg', '125 mg'), ('162 mg', '162 mg'), ('162.5 mg', '162.5 mg'), ('227.5 mg', '227.5 mg'), ('300 mg', '300 mg'), ('325 mg', '325 mg'), ('500 mg', '500 mg'), ('60 mg', '60 mg'), ('600 mg', '600 mg'), ('650 mg', '650 mg'), ('800 mg', '800 mg'), ('81 mg', '81 mg'), ('81 mg with phytosterols', '81 mg with phytosterols'), ('975 mg', '975 mg'), ('buffered 325 mg', 'buffered 325 mg'), ('buffered 500 mg', 'buffered 500 mg'), ('buffered 81 mg', 'buffered 81 mg'), ('other', 'other')], default = '')
    schedule_type = models.CharField(max_length = 50, choices = [('', 'Frequency'), ('As needed', 'As needed'), ('Daily', 'Daily'), ('Specific Days of Week', 'Specific Days of Week'), ('Days Interval', 'Days Interval'), ('Birth Control Cycle', 'Birth Control Cycle')], default = '')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='DrugUserProfileItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfileDrugs')
    last_updated = models.DateTimeField(auto_now_add = True)
class UserProfileConditions(models.Model):
    class Meta:
        unique_together = ('user_profile', 'condition')
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    other_details = models.TextField(blank = True, default = '', max_length = 150)
    condition = models.CharField(max_length = 12)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfileConditionsItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfileConditionsUser')
    last_updated = models.DateTimeField(auto_now_add = True)
class UserProfileAllergies(models.Model):
    class Meta:
        unique_together = ('user_profile', 'allergy')
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    allergy = models.ForeignKey(allergies, on_delete=models.CASCADE, related_name='UserProfileAllergies')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfileAllergiesItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfileAllergiesUser')
    last_updated = models.DateTimeField(auto_now_add = True)
class UserProfileReminder(models.Model):
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    date = models.DateField()
    time = models.TimeField()
    drug = models.ForeignKey(drug, on_delete=models.CASCADE, related_name='DrugUserProfileReminder')
    usage = models.TextField(blank = True, default = '', max_length = 50)
    notes = models.TextField(blank = True, default = '', max_length = 100)
    actions = models.CharField(max_length = 50, choices = [('taken', 'Taken'), ('skipped', 'Skipped'), ('', 'None'), ], default = '')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfileReminderItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfileReminder')
    last_updated = models.DateTimeField(auto_now_add = True)
class UserProfileNotes(models.Model):
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    date = models.DateField(default = now)
    time = models.TimeField(default = now)
    title = models.CharField(max_length = 255, default = '')
    more_details = models.TextField(blank = True, default = '')
    tags = models.TextField(blank = True, default = '')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfileNotesItem')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfileNotes')
    last_updated = models.DateTimeField(auto_now_add = True)
############## Profile Items Model in Website Ends Here ################









def validate_unique_permalink(value):
    if (drug.objects.filter(permalink=value).exists() or vitaminsAndSupplement.objects.filter(permalink=value).exists() or header_page.objects.filter(permalink=value).exists() or footer_page.objects.filter(permalink=value).exists()):
        raise ValidationError("This permalink is already taken. Please choose a different one.")






############## Questions Model in Website Starts Here ##############
class Questions(models.Model):
    def __str__(self):
        return self.id
    id = models.CharField(max_length = 20, primary_key = True, default = generate_unique_id, editable = False)
    question = models.CharField(max_length=255)
    details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Question')
    last_updated = models.DateTimeField(auto_now_add=True)
############## Questions Model in Website Ends Here ################


    
class newsletter(models.Model):
    def __str__(self):
        return f"Newsletter {self.email}"
    email = models.CharField(max_length = 100, primary_key = True)
    monthly_newsletter = models.BooleanField(default = True)
    daily_newsletter = models.BooleanField(default = True)
    FDA_safety_alerts = models.BooleanField(default = True)
    date_joined = models.DateTimeField(auto_now_add = True)
############################# Forms Starts Here #############################

class DrugSearchForm(forms.ModelForm):
    class Meta:
        model = drug_search
        fields = ['name', 'condition', 'generic_name', 'drug_class', 'type', 'permalink', 'off_market_drug']
    def __init__(self, *args, **kwargs):
        super(DrugSearchForm, self).__init__(*args, **kwargs)
        for field in ['name', 'condition', 'generic_name', 'drug_class', 'permalink', 'type']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
class DrugRichTextForm(forms.ModelForm):
    class Meta:
        model = drug
        fields = ['uses', 'side_effects', 'warnings', 'precautions', 'interactions', 'overdose']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uses'].widget.attrs.update({'class': 'outline-none'})
        self.fields['side_effects'].widget.attrs.update({'class': 'outline-none'})
        self.fields['warnings'].widget.attrs.update({'class': 'outline-none'})
        self.fields['precautions'].widget.attrs.update({'class': 'outline-none'})
        self.fields['interactions'].widget.attrs.update({'class': 'outline-none'})
        self.fields['overdose'].widget.attrs.update({'class': 'outline-none'})
class VitaminsAndSupplementsRichTextForm(forms.ModelForm):
    class Meta:
        model = vitaminsAndSupplement
        fields = ['overview', 'uses', 'side_effects', 'precautions', 'interactions', 'dosing']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['overview'].widget.attrs.update({'class': 'outline-none'})
        self.fields['uses'].widget.attrs.update({'class': 'outline-none'})
        self.fields['side_effects'].widget.attrs.update({'class': 'outline-none'})
        self.fields['precautions'].widget.attrs.update({'class': 'outline-none'})
        self.fields['interactions'].widget.attrs.update({'class': 'outline-none'})
        self.fields['dosing'].widget.attrs.update({'class': 'outline-none'})
class AllergiesForm(forms.ModelForm):
    class Meta:
        model = allergies
        fields = ['name', 'status', 'seo_title', 'seo_keywords', 'seo_description', 'content', 'permalink', "author"]
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AllergiesForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['name'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['status'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class AuthorAllergiesForm(forms.ModelForm):
    class Meta:
        model = allergies
        fields = ['name', 'status', 'seo_title', 'seo_keywords', 'seo_description', 'content', 'permalink', "author"]
        widgets = {'status': forms.HiddenInput(), 'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorAllergiesForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 'pending'
        if author:
            self.fields['author'].initial = author
        self.fields['name'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['status'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class DrugInteractionsForm(forms.ModelForm):
    class Meta:
        model = drug_interactions
        fields = ['first_drug', 'second_drug', 'level', 'status', 'consumer', 'professional', 'author']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(DrugInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        for field in ['first_drug', 'second_drug', 'level', 'consumer', 'professional', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
class FoodInteractionsForm(forms.ModelForm):
    class Meta:
        model = food_interactions
        fields = ['formula', 'header', 'severity', 'status', 'level', 'other_details', 'consumer', 'professional', 'author']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(FoodInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        for field in ['formula', 'header', 'severity', 'other_details', 'level', 'consumer', 'professional', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded resize-none'})
class DiseaseInteractionsForm(forms.ModelForm):
    class Meta:
        model = disease_interactions
        fields = ['formula', 'header', 'severity', 'level', 'content', 'author', 'status']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(DiseaseInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        for field in ['formula', 'header', 'severity', 'level', 'content', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
class AuthorDrugInteractionsForm(forms.ModelForm):
    class Meta:
        model = drug_interactions
        fields = ['first_drug', 'second_drug', 'level', 'status', 'consumer', 'professional', 'author']
        widgets = {'author': forms.HiddenInput(), 'status': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorDrugInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
           self.fields['status'].initial = 'pending'
        for field in ['first_drug', 'second_drug', 'level', 'consumer', 'professional', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
class AuthorFoodInteractionsForm(forms.ModelForm):
    class Meta:
        model = food_interactions
        fields = ['formula', 'header', 'severity', 'status', 'level', 'other_details', 'consumer', 'professional', 'author']
        widgets = {'author': forms.HiddenInput(), 'status': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorFoodInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
           self.fields['status'].initial = 'pending'
        for field in ['formula', 'header', 'severity', 'other_details', 'level', 'consumer', 'professional', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded resize-none'})
class AuthorDiseaseInteractionsForm(forms.ModelForm):
    class Meta:
        model = disease_interactions
        fields = ['formula', 'header', 'severity', 'level', 'content', 'author', 'status']
        widgets = {'author': forms.HiddenInput(), 'status': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorDiseaseInteractionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
           self.fields['status'].initial = 'pending'
        for field in ['formula', 'header', 'severity', 'level', 'content', 'author', 'status']:
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
class PillForm(forms.ModelForm):
    image_url = forms.CharField(max_length=255, required=False, label='Image URL')
    class Meta:
        model = pill
        fields = ['name', 'generic_name', 'imprint_side_1', 'imprint_side_2', 'strength', 'color', 'shape', 'redirect_url_name', 'redirect_url_imprint', 'image', 'image_url', 'status', 'author']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(PillForm, self).__init__(*args, **kwargs)
        if author:
            self.fields['author'].initial = author
        for field in ['name', 'generic_name', 'strength', 'imprint_side_1', 'imprint_side_2', 'redirect_url_name', 'redirect_url_imprint', 'color', 'shape', 'status', 'image', 'image_url']:
            if field == 'image_url':
                self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'filename.extension'})
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')
        if image and image_url:
            raise ValidationError("Please fill either the image upload or the image URL, not both.")
        if not image and not image_url:
            raise ValidationError("Please provide either an image upload or an image URL.")
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image_url'):
            instance.image = 'pills/identifier/'+self.cleaned_data['image_url']
        else:
            instance.image = self.cleaned_data['image']
        if commit:
            instance.save()
        return instance
class AuthorPillForm(forms.ModelForm):
    image_url = forms.CharField(max_length=255, required=False, label='Image URL')
    class Meta:
        model = pill
        fields = ['name', 'generic_name', 'imprint_side_1', 'imprint_side_2', 'strength', 'color', 'shape', 'redirect_url_name', 'redirect_url_imprint', 'image', 'image_url', 'author', 'status']
        widgets = {'author': forms.HiddenInput(), 'status': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorPillForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 'pending'
        if author:
            self.fields['author'].initial = author
        for field in ['name', 'generic_name', 'strength', 'imprint_side_1', 'imprint_side_2', 'redirect_url_name', 'redirect_url_imprint', 'color', 'shape', 'status', 'image', 'image_url']:
            if field == 'image_url':
                self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'filename.extension'})
            self.fields[field].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')
        if image and image_url:
            raise ValidationError("Please fill either the image upload or the image URL, not both.")
        if not image and not image_url:
            raise ValidationError("Please provide either an image upload or an image URL.")
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image_url'):
            instance.image = 'pills/identifier/'+self.cleaned_data['image_url']
        else:
            instance.image = self.cleaned_data['image']
        if commit:
            instance.save()
        return instance
class ContactUsForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email field cannot be empty.")
        if '@' not in email or '.' not in email:
            raise forms.ValidationError("Enter a valid email address containing '@' and '.'")
        return email
    class Meta:
        model = contact
        fields = ['subject', 'fullname', 'email', 'message']
        widgets = {'subject': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none'}), 'fullname': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 outline-none'}), 'email': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 outline-none'}), 'message': forms.Textarea(attrs={'class': 'h-40 border border-gray-300 p-2 outline-none resize-none'})}
class NewsForm(forms.ModelForm):
    class Meta:
        model = news
        fields = ['title', 'category', 'status', 'seo_title', 'seo_description', 'seo_keywords', 'content', 'featured_image', "author", 'permalink']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(NewsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['status'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'w-full outline-none'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['featured_image'].widget.attrs.update({'class': 'text-sm text-gray-700 file:border file:border-gray-300 file:bg-gray-50 file:py-2 file:px-4 file:rounded-md file:text-sm file:font-medium file:text-gray-700 hover:file:bg-gray-100'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class AuthorNewsForm(forms.ModelForm):
    class Meta:
        model = news
        fields = ['title', 'category', 'seo_title', 'featured_image', 'seo_description', 'seo_keywords', 'content', "author", 'permalink']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorNewsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'w-full outline-none'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['featured_image'].widget.attrs.update({'class': 'text-sm text-gray-700 file:border file:border-gray-300 file:bg-gray-50 file:py-2 file:px-4 file:rounded-md file:text-sm file:font-medium file:text-gray-700 hover:file:bg-gray-100'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class HeaderPageForm(forms.ModelForm):
    class Meta:
        model = header_page
        fields = ['title', 'seo_title', 'permalink', 'category', 'seo_description', 'seo_keywords', 'content']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none', 'placeholder': 'Content'})
        self.fields['permalink'].validators.append(validate_unique_permalink)
class FooterPageForm(forms.ModelForm):
    class Meta:
        model = footer_page
        fields = ['title', 'seo_title', 'permalink', 'category', 'seo_description', 'seo_keywords', 'content']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none', 'placeholder': 'Content'})
        self.fields['permalink'].validators.append(validate_unique_permalink)
class ConditionsForm(forms.ModelForm):
    class Meta:
        model = condition
        fields = ['heading', 'category', 'sub_category', 'status', 'content', 'seo_title', 'seo_description', 'seo_keywords', 'featured_image', "author", 'permalink']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(ConditionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['heading'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['sub_category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['status'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class AuthorConditionsForm(forms.ModelForm):
    class Meta:
        model = condition
        fields = ['heading', 'category', 'sub_category', 'content', 'seo_title', 'seo_description', 'seo_keywords', 'permalink', 'featured_image', "author"]
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorConditionsForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['heading'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['sub_category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none'})
class WellBeingForm(forms.ModelForm):
    class Meta:
        model = well_being
        fields = ['title', 'category', 'status', 'content', 'seo_title', 'seo_description', 'seo_keywords', 'featured_image', 'author', 'permalink']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(WellBeingForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['status'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['featured_image'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class AuthorWellBeingForm(forms.ModelForm):
    class Meta:
        model = well_being
        fields = ['title', 'category', 'content', 'seo_title', 'seo_description', 'seo_keywords', 'permalink', 'featured_image', 'author']
        widgets = {'author': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(AuthorWellBeingForm, self).__init__(*args, **kwargs)
        if author:
           self.fields['author'].initial = author
        self.fields['title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['category'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['content'].widget.attrs.update({'class': 'outline-none'})
        self.fields['permalink'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_title'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_description'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['seo_keywords'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
        self.fields['featured_image'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'})
class ChangeSocialsForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = ['twitter', 'youtube', 'facebook', 'linkedin', 'instagram', 'GoogleTagId', 'GoogleSearchConsoleId', 'robots']
        widgets = {'robots': forms.Textarea(attrs={'class': 'w-full min-h-60 max-h-60 border border-gray-200 focus:border-green-600 outline-none p-2 rounded resize transition duration-300', 'placeholder': 'Robots'}), 'GoogleSearchConsoleId': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'Google Search Console Id'}), 'twitter': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'Twitter URL'}), 'youtube': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'YouTube URL'}), 'facebook': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'Facebook URL'}), 'linkedin': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'LinkedIn URL'}), 'instagram': forms.URLInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'Instagram URL'}), 'GoogleTagId': forms.TextInput(attrs={'class': 'w-full border border-gray-200 focus:border-green-600 outline-none p-2 rounded transition duration-300', 'placeholder': 'Google Tag ID'})}
class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if not self.user.check_password(current_password):
            raise ValidationError('Current password is incorrect.')
        if new_password != confirm_password:
            raise ValidationError('New password and confirm password do not match.')
        if current_password == new_password:
            raise ValidationError('New password must be different from the current password.')
        return cleaned_data
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'placeholder': 'current password', 'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'}), required=True)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'placeholder': 'new password', 'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'}), required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'confirm password', 'class': 'border border-gray-300 p-2 outline-none transtion duration-300 focus:border-gray-700 rounded'}), required=True)
class AuthorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'category', 'password', 'link', 'phone_number', 'address', 'date_of_birth']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['last_name'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['username'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['email'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['password'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['link'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['phone_number'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['address'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'type': 'date'})
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['category'].initial = 'author'
class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required = True, widget = forms.EmailInput(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Email'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Password'}), required = True)
    date_of_birth = forms.CharField(widget = forms.TextInput(attrs = {'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Date of Birth (mm/dd/yyyy)'}), required = True)
    class Meta:
        model = User
        fields = ['email', 'password', 'date_of_birth']
    def clean_date_of_birth(self):
        dob_str = self.cleaned_data.get('date_of_birth')
        if dob_str:
            try:
                from datetime import datetime
                date_of_birth = datetime.strptime(dob_str, '%m/%d/%Y').date()
                age = (now().date() - date_of_birth).days // 365
                if age < 18:
                    raise ValidationError("You must be at least 18 years old.")
                return date_of_birth
            except ValueError:
                raise ValidationError("Date must be in the format mm/dd/yyyy.")
        return None
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    def save(self, commit=True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class UserSubscriptionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['every_day_mednews', 'monthly_newsletter_health_care', 'monthly_newsletter',  'FDA_approvals_for_drugs', 'FDA_safety_alerts', 'supporters',  'notice_of_projects_for_eDetailing', 'notice_of_CME_events']
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
    def clean_user(self):
        if self.user.category != "user":
            raise forms.ValidationError("User category must be 'user'")
        return self.user
class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question', 'details']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'class': 'w-full bg-[#E8F6FB] border border-gray-300 focus:border-gray-900 outline-none p-3 rounded transition duration-300', 'placeholder': 'Enter your question'})
        self.fields['details'].widget.attrs.update({'class': 'w-full bg-[#E8F6FB] border border-gray-300 focus:border-gray-900 outline-none p-3 rounded transition duration-300 resize-none', 'placeholder': 'Enter details here', 'rows': 8})
class UserProfileDrugsFormInitial(forms.ModelForm):
    class Meta:
        model = UserProfileDrugs
        fields = ['drug', 'status', 'other_details']
        widgets = {'other_details': forms.Textarea(attrs={'required': False, 'rows': 10, 'placeholder': 'Additional details...', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded resize-none'}), 'status': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Select status...'}), 'drug': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Select a drug...'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['drug'].queryset = drug.objects.filter(status = 'approved')
        self.fields['other_details'].label = "Other Details (Optional)"
class UserProfileConditionsFormInitial(forms.ModelForm):
    class Meta:
        model = UserProfileConditions
        fields = ['condition', 'other_details']
        widgets = {'other_details': forms.Textarea(attrs={'required': False, 'rows': 10, 'placeholder': 'Additional details (optional)...', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded resize-none'}), 'condition': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_details'].label = "Other Details (Optional)"
class UserProfileAllergiesForm(forms.ModelForm):
    class Meta:
        model = UserProfileAllergies
        fields = ['allergy']
        widgets = {'allergy': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Select an allergy...'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allergy'].label = "Allergy"
class UserProfileReminderForm(forms.ModelForm):
    class Meta:
        model = UserProfileReminder
        fields = ['date', 'time', 'drug', 'usage', 'notes', 'actions']
        widgets = {'date': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'}), 'time': forms.TimeInput(attrs={'type': 'time', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'}), 'drug': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'}), 'usage': forms.Textarea(attrs={'placeholder': 'Usage details...', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'}), 'notes': forms.Textarea(attrs={'placeholder': 'Additional notes...', 'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'}), 'actions': forms.Select(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded'})}
class UserProfileNotesForm(forms.ModelForm):
    class Meta:
        model = UserProfileNotes
        fields = ['date', 'time', 'title', 'more_details', 'tags']
        widgets = {'date': forms.DateInput(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'type': 'date'}), 'time': forms.TimeInput(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'type': 'time'}), 'title': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Enter title...'}), 'more_details': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded resize-none', 'rows': 5, 'placeholder': 'Enter more details...'}), 'tags': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 outline-none transition duration-300 focus:border-gray-700 rounded', 'placeholder': 'Enter tags...'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['more_details'].label = "More Details (Optional)"
        self.fields['tags'].label = "Tags (Optional)"
############################# Forms Ends Here ###############################