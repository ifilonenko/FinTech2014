# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Class'
        db.create_table(u'classes_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('private', self.gf('django.db.models.fields.BooleanField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'classes', ['Class'])

        # Adding model 'BasketClassMembership'
        db.create_table(u'classes_basketclassmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('basket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Basket'])),
            ('tclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.Class'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('open_for_voting', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'classes', ['BasketClassMembership'])

        # Adding unique constraint on 'BasketClassMembership', fields ['basket', 'tclass']
        db.create_unique(u'classes_basketclassmembership', ['basket_id', 'tclass_id'])

        # Adding model 'ClassEnrollment'
        db.create_table(u'classes_classenrollment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.Class'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'classes', ['ClassEnrollment'])

        # Adding unique constraint on 'ClassEnrollment', fields ['student', 'tclass']
        db.create_unique(u'classes_classenrollment', ['student_id', 'tclass_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ClassEnrollment', fields ['student', 'tclass']
        db.delete_unique(u'classes_classenrollment', ['student_id', 'tclass_id'])

        # Removing unique constraint on 'BasketClassMembership', fields ['basket', 'tclass']
        db.delete_unique(u'classes_basketclassmembership', ['basket_id', 'tclass_id'])

        # Deleting model 'Class'
        db.delete_table(u'classes_class')

        # Deleting model 'BasketClassMembership'
        db.delete_table(u'classes_basketclassmembership')

        # Deleting model 'ClassEnrollment'
        db.delete_table(u'classes_classenrollment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': u"orm['relationships.Relationship']", 'to': u"orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'classes.basketclassmembership': {
            'Meta': {'unique_together': "(('basket', 'tclass'),)", 'object_name': 'BasketClassMembership'},
            'basket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Basket']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_for_voting': ('django.db.models.fields.BooleanField', [], {}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tclass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['classes.Class']"})
        },
        u'classes.class': {
            'Meta': {'object_name': 'Class'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'baskets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'baskets'", 'symmetrical': 'False', 'through': u"orm['classes.BasketClassMembership']", 'to': u"orm['polls.Basket']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enrollment': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enrollment'", 'symmetrical': 'False', 'through': u"orm['classes.ClassEnrollment']", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'private': ('django.db.models.fields.BooleanField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'classes.classenrollment': {
            'Meta': {'unique_together': "(('student', 'tclass'),)", 'object_name': 'ClassEnrollment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'tclass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['classes.Class']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'polls.basket': {
            'Meta': {'unique_together': "(('owner', 'name'),)", 'object_name': 'Basket'},
            'corks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'corks'", 'symmetrical': 'False', 'through': u"orm['polls.CorkBasketMembership']", 'to': u"orm['polls.Cork']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'polls.cork': {
            'Meta': {'object_name': 'Cork'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'site_images/default_cork.png'", 'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polls.Reference']", 'symmetrical': 'False'})
        },
        u'polls.corkbasketmembership': {
            'Meta': {'unique_together': "(('cork', 'basket'),)", 'object_name': 'CorkBasketMembership'},
            'basket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Basket']"}),
            'cork': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Cork']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'polls.reference': {
            'Meta': {'object_name': 'Reference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'relationships.relationship': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('from_user', 'to_user', 'status', 'site'),)", 'object_name': 'Relationship'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_users'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'relationships'", 'to': u"orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['relationships.RelationshipStatus']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_users'", 'to': u"orm['auth.User']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'})
        },
        u'relationships.relationshipstatus': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RelationshipStatus'},
            'from_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'symmetrical_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['classes']