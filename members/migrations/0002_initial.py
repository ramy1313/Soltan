# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table('members_member', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('job', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('national_number', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('membership_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('personal_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('membership_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deactivated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('members', ['Member'])

        # Adding model 'Receipt'
        db.create_table('members_receipt', (
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('rec_number', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rec_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('current_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('number_of_years', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('last_paid_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('members', ['Receipt'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('members_member')

        # Deleting model 'Receipt'
        db.delete_table('members_receipt')


    models = {
        'members.member': {
            'Meta': {'object_name': 'Member'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactivated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'membership_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'national_number': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'personal_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'members.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'current_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_paid_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'number_of_years': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'rec_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rec_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['members']