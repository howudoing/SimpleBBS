from django.forms import ModelForm
from bbs import models


class ArticleModelForm(ModelForm):
    class Meta:
        model = models.Articles
        exclude = ('author','priority','pub_date')

    def __init__(self, *args, **kwargs):
        super(ArticleModelForm, self).__init__(*args, **kwargs)
        # self.fields['qq'].widget.attrs["class"] = "form-control"
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})
