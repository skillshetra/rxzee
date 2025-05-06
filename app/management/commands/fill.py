from requests import get as get_data
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from app.models import HomePage, User, footer_page, drug_search, pill as PIll, drug_interactions, disease_interactions, food_interactions, news as NEWS
from gzip import GzipFile as open_data
from json import load as load_data
from io import BytesIO
class Command(BaseCommand):
    help = 'Fill initial data into the database'
    def handle(self, *args, **kwargs):
        try:
            i = 1
            site = Site.objects.first()
            response = get_data('https://rxzee.netlify.app/pages.json.gz', stream=True)
            HomePage.objects.create()
            self.stdout.write(f'\033[93m[{i}]\033[92m Created a default homepage for RxZee.\033[0m')
            i+=1
            if site:
                site.name = "RxZee"
                site.domain = "rxzee.com"
                site.save()
                self.stdout.write(f'\033[93m[{i}]\033[92m Changed Sitemap SEO data for RxZee.\033[0m')
                i+=1
            author = User.objects.create_user(username = 'rxzee', password = 'rxzee@123', first_name = 'RxZee', email = 'rxzee@rxzee.com', category = 'author', phone_number = '1122334455', address = 'Lucknow Uttar Pradesh, India', date_of_birth = '2000-1-1')
            User.objects.create_superuser(username = 'jainya', password = '3c26459566d4be7c5dd10ff9e626a72d', first_name = 'RxZee', last_name = 'Admin', email = 'support@rxzee.com', category = 'admin', phone_number = '1122334455', address = 'Lucknow Uttar Pradesh, India', date_of_birth = '2000-1-1')
            self.stdout.write(f'\033[93m[{i}]\033[92m Created a superuser jainya.\033[0m')
            for news in [{"permalink": "news-example-2024-1", "title": "Innovative Technologies in Home Fitness", "content": "<p>The latest technologies in home fitness equipment are changing how we approach exercise.</p>", "category": "Fitness", "seo_title": "Home Fitness Innovations", "seo_description": "Discover cutting-edge technologies that are transforming home workouts.", "seo_keywords": "home fitness, exercise technology, workout innovations", "featured_image": "https://cdn.sanity.io/images/0vv8moc6/pharmtech/03b5e13f57563d2cceeff5e14f4cc47297f7db7e-1278x723.jpg", "search_count": 20, "status": "approved"}, {"permalink": "news-example-2024-2", "title": "Trends in Organic Food Products", "content": "<p>Organic food products are becoming increasingly popular, reflecting a shift in consumer preferences.</p>", "category": "Food", "seo_title": "Organic Food Trends", "seo_description": "Learn about the latest trends in organic food products and consumer choices.", "seo_keywords": "organic food, consumer trends, health products", "featured_image": "https://images.indianexpress.com/2024/10/FDA-N.jpg?w=414", "search_count": 25, "status": "approved"}, {"permalink": "news-example-2024-3", "title": "The Rise of Mental Health Apps", "content": "<p>Mental health apps are gaining traction as tools for improving emotional well-being.</p>", "category": "Technology", "seo_title": "Mental Health Apps", "seo_description": "Explore the rise of mental health apps and their impact on well-being.", "seo_keywords": "mental health, wellness apps, technology", "featured_image": "https://img.etimg.com/thumb/width-1200,height-1200,imgsize-74528,resizemode-75,msid-101576668/news/international/us/heres-a-long-awaited-new-fda-approved-treatment-for-alzheimers-read-more.jpg", "search_count": 30, "status": "approved"}, {"permalink": "news-example-2024-4", "title": "Sustainable Packaging in Consumer Goods", "content": "<p>More companies are adopting sustainable packaging to meet consumer demands for eco-friendly products.</p>", "category": "Sustainability", "seo_title": "Sustainable Packaging Trends", "seo_description": "Find out how sustainable packaging is shaping the consumer goods industry.", "seo_keywords": "sustainable packaging, eco-friendly, consumer goods", "featured_image": "https://www.fda.gov/files/styles/medium_3/public/prescription-pill-bottles-national-prescription-drug-take-back-day.png?itok=_4wTjSJu", "search_count": 18, "status": "approved"}, {"permalink": "news-example-2024-5", "title": "Advancements in Sleep Technology", "content": "<p>New technologies aimed at improving sleep quality are gaining popularity among consumers.</p>", "category": "Health", "seo_title": "Sleep Technology Innovations", "seo_description": "Discover the latest advancements in sleep technology for better rest.", "seo_keywords": "sleep technology, health products, wellness", "featured_image": "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/8192x5464+0+0/resize/1100/quality/85/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F3d%2F2f%2F314776974d4aa27b99d70243b092%2Fcobenfy-product-image.jpg", "search_count": 12, "status": "approved"}, {"permalink": "news-example-2024-6", "title": "Nutrition Supplements on the Rise", "content": "<p>Nutrition supplements are becoming more mainstream as consumers focus on health and wellness.</p>", "category": "Health", "seo_title": "Nutrition Supplement Trends", "seo_description": "Explore the growing popularity of nutrition supplements and their benefits.", "seo_keywords": "nutrition supplements, health trends, wellness", "featured_image": "https://scx2.b-cdn.net/gfx/news/2024/many-cancer-drugs-stil.jpg", "search_count": 22, "status": "approved"}, {"permalink": "news-example-2024-7", "title": "Smart Wearables for Health Monitoring", "content": "<p>Smart wearables are revolutionizing health monitoring, providing valuable data to users.</p>", "category": "Technology", "seo_title": "Health Monitoring Wearables", "seo_description": "Learn how smart wearables are changing personal health monitoring.", "seo_keywords": "wearable technology, health monitoring, fitness", "featured_image": "https://drugscontrol.org/pdf/US-FDA-FDCA051222081936.jpg", "search_count": 28, "status": "approved"}, {"permalink": "news-example-2024-8", "title": "Holistic Health Approaches", "content": "<p>Consumers are increasingly interested in holistic approaches to health and wellness.</p>", "category": "Wellness", "seo_title": "Holistic Health Trends", "seo_description": "Discover the rise of holistic health approaches among consumers.", "seo_keywords": "holistic health, wellness trends, consumer choices", "featured_image": "", "search_count": 14, "status": "approved"}, {"permalink": "news-example-2024-9", "title": "The Impact of Plant-Based Diets", "content": "<p>Plant-based diets are on the rise, influencing consumer choices in food products.</p>", "category": "Food", "seo_title": "Plant-Based Diet Trends", "seo_description": "Explore the impact of plant-based diets on consumer food choices.", "seo_keywords": "plant-based diet, food trends, health", "featured_image": "https://www.hindustantimes.com/ht-img/img/2024/10/09/550x309/Food-and-Drug-Administration--FDA---Pune-division-_1728501469741.jpg", "search_count": 19, "status": "approved"}, {"permalink": "news-example-2024-10", "title": "Advances in Telehealth Services", "content": "<p>Telehealth services are transforming access to healthcare for consumers worldwide.</p>", "category": "Health", "seo_title": "Telehealth Innovations", "seo_description": "Learn about the latest advancements in telehealth services and their benefits.", "seo_keywords": "telehealth, healthcare access, innovations", "featured_image": "https://bsmedia.business-standard.com/_media/bs/img/article/2024-03/07/full/1709750255-5349.jpg?im=FeatureCrop,size=(826,465)", "search_count": 17, "status": "approved"}]:
                NEWS.objects.create(**news, author = author)
            i+=1
            self.stdout.write(f'\033[93m[{i}]\033[92m Started Pushing data for footer pages RxZee.\033[0m')
            response = get_data('https://rxzee.netlify.app/pages.json.gz', stream=True)
            with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                 page_data = load_data(f)
            for page in page_data:
                self.stdout.write(f'\033[93m[{i}]\033[92m {page['title']} pushed to footer page RxZee.\033[0m')
                footer_page.objects.create(**page)
                i+=1
            del page_data
            response = get_data('https://rxzee.netlify.app/drugs_data.json.gz', stream=True)
            with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                 search_drugs_data = load_data(f)
            self.stdout.write(f'\033[93m[{i}]\033[92m Started pushing all data for drug search RxZee.\033[0m')
            drug_search.objects.bulk_create([drug_search(**drug) for drug in [{key: value for key, value in drug.items() if value not in (None, "", "")} for drug in search_drugs_data]])
            i+=1
            self.stdout.write(f'\033[93m[{i}]\033[92m Pushed all data for drug search RxZee.\033[0m')
            del search_drugs_data
            i+=1
            self.stdout.write(f'\033[93m[{i}]\033[92m Started pushing all data for pill identifier RxZee.\033[0m')
            i+=1
            response = get_data('https://rxzee.netlify.app/pill_identifier.json.gz', stream=True)
            with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                pill_data = load_data(f)
            i+=1
            PIll.objects.bulk_create([PIll(**pill, author = author) for pill in pill_data])
            del pill_data
            self.stdout.write(f'\033[93m[{i}]\033[92m Pushed all data for pill identifier RxZee.\033[0m')
            i+=1
            response = get_data('https://rxzee.netlify.app/disease_interactions_data.json.gz', stream=True)
            with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                disease_interactions_data = load_data(f)
            self.stdout.write(f'\033[93m[{i}]\033[92m Started pushing all data for disease interactions RxZee.\033[0m')
            i+=1
            disease_interactions.objects.bulk_create([disease_interactions(**disease_interaction, author = author) for disease_interaction in disease_interactions_data])
            del disease_interactions_data
            self.stdout.write(f'\033[93m[{i}]\033[92m Pushed all data for disease interactions RxZee.\033[0m')
            i+=1
            response = get_data('https://rxzee.netlify.app/food_interaction.json.gz', stream=True)
            with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                food_interaction_data = load_data(f)
            self.stdout.write(f'\033[93m[{i}]\033[92m Started pushing all data for food interactions RxZee.\033[0m')
            food_interactions.objects.bulk_create([food_interactions(**food_interaction, author = author) for food_interaction in food_interaction_data])
            del food_interaction_data
            i+=1
            self.stdout.write(f'\033[93m[{i}]\033[92m Pushed all data for food interactions RxZee.\033[0m')
            i+=1
            for url in ['https://rxzee.netlify.app/drug_interaction_1.gz', 'https://rxzee.netlify.app/drug_interaction_2.gz', 'https://rxzee.netlify.app/drug_interaction_3.gz', 'https://rxzee.netlify.app/drug_interaction_4.gz', 'https://rxzee.netlify.app/drug_interaction_5.gz']:
                response = get_data(url, stream=True)
                with open_data(fileobj=BytesIO(response.content), mode='rb') as f:
                    drug_interactions_data = load_data(f)
                self.stdout.write(f'\033[93m[{i}]\033[92m Saving data from {url} to the drug interaction.\033[0m')
                drug_interactions.objects.bulk_create([drug_interactions(**drug_interaction, author = author) for drug_interaction in drug_interactions_data])
                i+=1
                del drug_interactions_data
                self.stdout.write(f'\033[93m[{i}]\033[92m Data from {url} saved successfully to the drug interaction.\033[0m')
                i+=1
        except Exception as e:
            self.stdout.write(f'\033[91m{str(e)}\033[0m')