from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings 
from .forms import SignupForm, BookForm, UserUpdateForm
from .models import Book
from django.views.generic import ListView

# ✅ ポートフォリオ画面（最初に表示するページ）
class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

# ✅ 新規登録画面
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})  
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)  # 自動ログイン
            return redirect("home")  # ホーム画面へリダイレクト
        return render(request, "signup.html", {"form": form})

# ✅ ログイン画面
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")  

# ✅ ホーム画面（絵本一覧を表示）
class HomeView(ListView):
    model = Book
    template_name = "home.html"
    context_object_name = "books"
    paginate_by = 6

    def get_queryset(self):
        try:
            books = Book.objects.all().order_by('-created_at')
            print(f"📌 デバッグ: HomeView に渡されたデータの数: {books.count()}")  
            return books
        except Exception as e:
            print(f"❌ HomeView のエラー: {e}")
            return Book.objects.none()  # 空のクエリセットを返す

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["MEDIA_URL"] = settings.MEDIA_URL
            return context 
        except Exception as e:
            print(f"❌ HomeView のコンテキストエラー: {e}")
            return {"books": [], "MEDIA_URL": settings.MEDIA_URL}


# ✅ お気に入りページ
def favorite(request):
    return render(request, 'favorite.html')

# ✅ ふりかえりページ
def review(request):
    return render(request, 'review.html')

# ✅ もっとよんでページ
def more_read(request):
    return render(request, 'more_read.html')

# ✅ 設定ページ
def settings_view(request):
    return render(request, 'settings.html')

# ✅ 家族招待ページ
def family_invite(request):
    return render(request, 'family_invite.html')


# ✅ 絵本登録ページ
def add_book(request):
    print("📌 add_book 関数が呼ばれました")  # ✅ デバッグ

    try:
        if request.method == "POST":
            print("📌 POST メソッドが呼ばれました")
            print(f"📌 リクエストデータ: {request.POST}")
            print(f"📌 アップロードされたファイル: {request.FILES}")

            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save()
                print(f"✅ 登録成功: {book.title}, 画像: {book.image}")
                return redirect('home')
            else:
                print("❌ フォームエラー:", form.errors)
                return render(request, "add_book.html", {"form": form, "errors": form.errors})  # エラー情報を渡す
        else:
            form = BookForm()

        return render(request, "add_book.html", {"form": form})

    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return render(request, "add_book.html", {"form": BookForm(), "error_message": "登録中にエラーが発生しました。"})

# ✅ パスワード変更ビュー
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')

password_change_view = login_required(CustomPasswordChangeView.as_view())

# ✅ Django標準の新規登録ビュー
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ 登録後にログイン
            return redirect('home')  # ✅ ホーム画面へリダイレクト
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

# ✅ 絵本詳細ビュー
def book_detail(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        return render(request, "book_detail.html", {"book": book})
    except Exception as e:
        print(f"❌ book_detail のエラー: {e}")
        return render(request, "error.html", {"error_message": "絵本の詳細を取得できませんでした。"})

# ✅ 絵本削除ビュー
def delete_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        if request.method == "POST":
            book.delete()
            return redirect('home')  # ✅ 削除後はホーム画面にリダイレクト
        return render(request, "book_detail.html", {"book": book})
    except Exception as e:
        print(f"❌ delete_book のエラー: {e}")
        return render(request, "error.html", {"error_message": "絵本の削除中にエラーが発生しました。"})
