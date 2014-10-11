# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'polls_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'polls', ['Author'])

        # Adding model 'Reference'
        db.create_table(u'polls_reference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'polls', ['Reference'])

        # Adding model 'Cork'
        db.create_table(u'polls_cork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Author'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'polls', ['Cork'])

        # Adding M2M table for field references on 'Cork'
        m2m_table_name = db.shorten_name(u'polls_cork_references')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cork', models.ForeignKey(orm[u'polls.cork'], null=False)),
            ('reference', models.ForeignKey(orm[u'polls.reference'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cork_id', 'reference_id'])

        # Adding model 'Basket'
        db.create_table(u'polls_basket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Author'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'polls', ['Basket'])

        # Adding M2M table for field corks on 'Basket'
        m2m_table_name = db.shorten_name(u'polls_basket_corks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('basket', models.ForeignKey(orm[u'polls.basket'], null=False)),
            ('cork', models.ForeignKey(orm[u'polls.cork'], null=False))
        ))
        db.create_unique(m2m_table_name, ['basket_id', 'cork_id'])

        # Adding model 'Choice'
        db.create_table(u'polls_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Cork'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'polls', ['Choice'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'polls_author')

        # Deleting model 'Reference'
        db.delete_table(u'polls_reference')

        # Deleting model 'Cork'
        db.delete_table(u'polls_cork')

        # Removing M2M table for field references on 'Cork'
        db.delete_table(db.shorten_name(u'polls_cork_references'))

        # Deleting model 'Basket'
        db.delete_table(u'polls_basket')

        # Removing M2M table for field corks on 'Basket'
        db.delete_table(db.shorten_name(u'polls_basket_corks'))

        # Deleting model 'Choice'
        db.delete_table(u'polls_choice')


    models = {
        u'polls.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'polls.basket': {
            'Meta': {'object_name': 'Basket'},
            'corks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polls.Cork']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Author']"})
        },
        u'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Cork']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'polls.cork': {
            'Meta': {'object_name': 'Cork'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Author']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['polls.Reference']", 'symmetrical': 'False'})
        },
        u'polls.reference': {
            'Meta': {'object_name': 'Reference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['polls']