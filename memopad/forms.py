from .models import Memo
from django import forms

class MemoForm(forms.ModelForm):
    class Meta:
          model = Memo
          fields = ('title', 'text')
          labels = {'title':'タイトル', 'text':'テキスト'}
   

    def test(self):
       print("test_ok")