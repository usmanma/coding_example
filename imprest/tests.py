from django.test import TestCase
from django.utils import timezone

from .models import Category, Expense, Report

class CategoryModelTest(TestCase):
    def test_can_create_new_category_and_save_to_db(self):
        category = Category()
        
        category.category = "Hospitality"
        category.published = True
        # check we can save it
        category.save()
        # See if we can retrieve it from db
        all_categories_in_db = Category.objects.all()
        self.assertEquals(len(all_categories_in_db), 1)
        # Make sure it was saved
        only_category_in_db = all_categories_in_db[0]
        self.assertEquals(only_category_in_db, category)
        # And make sure it saved both attributes
        self.assertEquals(only_category_in_db.category, "Hospitality")
        self.assertEquals(only_category_in_db.published, True)
        
    def test_can_update_category(self):
        category = Category.objects.all()[0]
        category.category = "Bills"
        category.save()
        
        updated_category = Category.objects.all()[0]
        self.assertEquals(updated_category, category)
        self.assertEquals(updated_category, "Bills")
