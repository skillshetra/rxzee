from django.core.management.base import BaseCommand
from app.models import drug_search, drug_interactions, disease_interactions, food_interactions
import re
class Command(BaseCommand):
    help = 'Creating Internal Linking'
    INTERNAL_LINKING_MODELS = [drug_interactions, disease_interactions, food_interactions]
    LINKS = {drug.name.strip(): drug.permalink for drug in drug_search.objects.all()}
    def update_links(self):
        self.LINKS.update({name.strip(): drug.permalink for drug in drug_search.objects.all() for name in drug.generic_name.split('|')})
    def replace_words(self, content):
        for word in re.sub(r'[^\w\s]', '', re.sub(r'<\/?p>', '', content)).split():
            if word in self.LINKS and f'<a href="/{self.LINKS[word]}" class="text-[#0095FD] hover:underline transition duration-300">{word}</a>' not in content:
                content = content.replace(word, f'<a href="/{self.LINKS[word]}" class="text-[#0095FD] hover:underline transition duration-300">{word}</a>', 1)
        return content
    def handle(self, *args, **kwargs):
        try:
            self.update_links()
            self.stdout.write('\033[93m[1]\033[92m Starting to build internal links for RxZee This will take a few minutes.\033[0m')
            i = 2
            for model in self.INTERNAL_LINKING_MODELS:
                for offset in range(0, model.objects.count(), 1000):
                    records = model.objects.all()[offset:offset + 1000]
                    update_drug_records = [record for record in records if isinstance(record, drug_interactions) and (setattr(record, 'consumer', self.replace_words(record.consumer)) or  setattr(record, 'professional', self.replace_words(record.professional)) or True)]
                    update_disease_records = [record for record in records if isinstance(record, disease_interactions) and (setattr(record, 'content', self.replace_words(record.content)) or True)]
                    update_food_records = [record for record in records if isinstance(record, food_interactions) and (setattr(record, 'consumer', self.replace_words(record.consumer)) or setattr(record, 'professional', self.replace_words(record.professional)) or True)]
                    if update_disease_records:
                        disease_interactions.objects.bulk_update(update_disease_records, ['content'])
                    if update_drug_records:
                        drug_interactions.objects.bulk_update(update_drug_records, ['consumer', 'professional'])
                    if update_food_records:
                        food_interactions.objects.bulk_update(update_food_records, ['consumer', 'professional'])
                    self.stdout.write(f'\033[93m[{i}]\033[92m Updated {offset} - {offset+1000} with internal links of {model.__name__.replace('_', ' ').title()} model in RxZee.\033[0m')
                    i += 1
            self.stdout.write(f'\033[93m[{i}]\033[92m Built internal links for RxZee successfully.\033[0m')
        except Exception as e:
            self.stdout.write(f'\033[91m{str(e)}\033[0m')