# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FoodCategory'
        db.create_table('food_foodcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('food', ['FoodCategory'])

        # Adding model 'Food'
        db.create_table('food_food', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['food.FoodCategory'])),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('cover_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('storage_time', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('storage_method', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('recipe_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('like_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pick_method', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('food_efficacy', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('food', ['Food'])


    def backwards(self, orm):
        # Deleting model 'FoodCategory'
        db.delete_table('food_foodcategory')

        # Deleting model 'Food'
        db.delete_table('food_food')


    models = {
        'food.food': {
            'Meta': {'object_name': 'Food'},
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['food.FoodCategory']"}),
            'cover_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'food_efficacy': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pick_method': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'recipe_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage_method': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'storage_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'food.foodcategory': {
            'Meta': {'object_name': 'FoodCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['food']