# Generated by Django 2.0 on 2017-12-23 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('brief', models.CharField(blank=True, max_length=128, null=True)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField(default=1000, verbose_name='优先级')),
                ('head_img', models.ImageField(upload_to='uploads', verbose_name='文章标题图片')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '已发布'), ('hidden', '隐藏')], default='published', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('brief', models.CharField(blank=True, max_length=128, null=True)),
                ('set_as_top_menu', models.BooleanField(default=False)),
                ('position_index', models.SmallIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_type', models.IntegerField(choices=[(1, '评论'), (2, '点赞')], default=1)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('articles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Articles', verbose_name='所属文章')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_children', to='bbs.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('signature', models.CharField(blank=True, max_length=255, null=True)),
                ('head_img', models.ImageField(blank=True, height_field=150, null=True, upload_to='', width_field=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='category',
            name='admins',
            field=models.ManyToManyField(blank=True, to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Category'),
        ),
    ]
