from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from . import forms
from .forms import MemoForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    )

from .models import Memo,Tag

import sys
sys.path.append('../')
from accounts.models import Profile

def index_view(request):
    object_list = Memo.objects.order_by('title') #tagsを設定すると増殖バグが…w
    return render(request, 'memo/index.html', {'object_list' : object_list})

class ListMemoView(ListView):
    template_name = 'memo/memo_list.html'
    model = Memo

class DetailMemoView(DetailView):
    template_name = 'memo/memo_detail.html'
    model = Memo

# class CreateMemoView(CreateView):
    # template_name = 'memo/memo_create.html'
    # model = Memo
    # fields = ('title', 'text')
    # success_url = reverse_lazy('memo-list')
 
    # def form_valid(self, form):
    #     print("print1")

    #     tag_list = self.request.POST["tags"].split('　')
    #     print(tag_list)

    #     # 新しく「＊＊＊＊（メモ）」を作る
    #     # tagは割り当てない
    #     new_memo = Memo.objects.create(title = self.request.POST["title"], text = self.request.POST["text"])
    #     #tagにtagsを割り当てる（for文で回す）
    #     for tag in tag_list:
    #         print(tag)
    #         new_tag = Tag.objects.create(tag_name = tag)
    #         new_memo.tags.add(new_tag)

    #     return super().form_valid(form)

# class CreateMemoView(CreateView): #改造版
    #利用するモデルを指定
    #model = Memo
    #利用するフォームクラス名を指定     
    #form_class = MemoForm
    #登録処理が正常終了した場合の遷移先を指定
    #success_url = reverse_lazy('memo/index.html')
    # template_name = 'memo/memo_create.html'
 
    # def form_valid(self, form):
    #     print("print1")

    #     tag_list = self.request.POST["tags"].split('　')
    #     print(tag_list)

    #     # 新しく
    #     # tagは割り当てない
    #     new_memo = Memo.objects.create(title = self.request.POST["title"], text = self.request.POST["text"])
    #     #tagにtagsを割り当てる（for文で回す）
    #     for tag in tag_list:
    #         print(tag)
    #         new_tag = Tag.objects.create(tag_name = tag)
    #         new_memo.tags.add(new_tag)

    #     return super().form_valid(form)
    
def creatememo_func(request):
    model = Memo
    form_class = forms.MemoForm()
    context = None
    template_name = 'memo/memo_create.html'
    print("print1")

    form = form_class(request.GET or None)
    context = ({'form':form})

    if request.method=='POST':
       form = form_class(request.POST or None)
       
    if form.is_valid():
        form.save(commit=True)
    
    tag_list = request.POST["tags"].split('　')
    print(tag_list)

    # 新しく「＊＊＊＊（メモ）」を作る
    # tagは割り当てない
    #tagにtagsを割り当てる（for文で回す）
    for tag in tag_list:
        print(tag)
        new_tag = Tag.objects.create(tag_name = tag)
        form.tags.add(new_tag)

    return render(request, 'memo/memo-list', context)

class DeleteMemoView(DeleteView):
    template_name = 'memo/memo_delete.html'
    model = Memo
    success_url = reverse_lazy('memo-list')

class UpdateMemoView(UpdateView):
    template_name = 'memo/memo_update.html'
    model = Memo
    fields = (['title', 'text'])
    success_url = reverse_lazy('memo-list')

#並び替え
def memo_orderchange(request, ):
    # ----------↓object_listに全書籍データを代入↓----------
    object_list = Memo.objects.all()
    # ----------↓profile1にログインしているユーザーのプロフィール情報を代入↓----------
    profile1 = Profile.objects.get(pk=request.user.profile.id) # profile1に一人分のプロフィールデータが入る
    # ----------↓profile1の本の並び順を取得する↓----------
    order_list = profile1.save_memo_id
    # object_pk_list = []
    # for obj in object_list:
    #     object_pk_list.append(obj.pk)
    # print(f”全フォルダのid(object_pk_list):{object_pk_list}“)
    # print(f”ユーザーの並び変え順(order_list):{order_list}“)
    # ----------↓設定されている順番に並び替える↓----------
    memos_dict = dict([(memo.id, memo) for memo in object_list]) # [id: そのidのFolderデータ]という形で辞書に収める
    sorted_memos_list = [memos_dict[int(id)] for id in order_list] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_memosに積めていく
    # print(f”idとデータの辞書(memo_dict):{memos_dict}“)
    print(f"並び替えられた書籍データ（sorted_memos_list）:{sorted_memos_list}")
    # ----------↑設定されている順番に並び替える↑----------
    # ----------↓並び替え確定のボタンが押されてリクエストが来た時の分岐↓----------
    if (request.method == 'POST'):
        new_order = request.POST['submit'].split(",") # new_orderに並び替えた後のデータをリスト型で保管する
        print(f"html側から受け取ったもの：{new_order}") # htmlから渡されたものを確認する
        profile1.save_memo_id = new_order # プロフィールのsave_memo_idに上書き
        profile1.save() # 変更を保存
        print(f"並び替え後のlist：{profile1.save_memo_id}") # profileテーブルの内容が上書きされているかを確認する
        return redirect('memo-list')
    # ----------↑並び替え確定のボタンが押されてリクエストが来た時の分岐↑----------
    # ----------↓並び替えするためにリクエストが来た時の分岐↓----------
    else:
        context = {
            # "object_list": object_list, # 全書籍データ
            # # "object_pk_list": object_pk_list, # 全書籍データ（idのみ）
            # "order_list": order_list, # ユーザーの並び替え順（idのみ）
            # "memos_dict": memos_dict, # {id: その書籍データ}と、辞書型で全書籍データがある
            "sorted_memos_list": sorted_memos_list, # 並び替え順で書籍データが詰まっている（リスト型）
        }
        return render(
        request,
        'memo/change.html',
        context)
    # ----------↑並び替えするためにリクエストが来た時の分岐↑----------