from django.shortcuts import render,HttpResponse,redirect, get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required

def index(request):

    context= {"numbers":[1,2,3,4]}

    return render(request,"index.html",context)

def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):#dashboard requesti gelmeden detail e gidemez dolayısıyla id bilgisini burda aldıktan sonra a elementiyle request gitten sonra url ler üzerinden tekrar id bilgisini alarak detail fonksiyonuna id gönderilir. 
    articles = Article.objects.filter(author = request.user)# liste içindeki her bir eleman sözlük olucak şekilde(sözlüklerinde her bir elemanı bir makalenin bir özelliğini temsil eder listenin her bir elemanı ise makale objelerini temsil eder.)
    context = { 
        "articles":articles

    }
    return render(request, "dashboard.html",context)

@login_required(login_url = "user:login")   
def addArticle(request):

    form = ArticleForm(request.POST or None, request.FILES or None) #post request olduğunda kullanıcıdan gelen bilgilerle dolduruluyor get request olduğund form boş gösteriliyor.
    
    if form.is_valid():

        article = form.save(commit=False) #author bilgisini almadan kaydetmesini önlemek için commit:false yaptık yoksa hata veriyor.çünkü biz input girdiğimizde author inputu yok girmiyoruz o nedenle hata veriyor.
        article.author = request.user #request eden user bilgisini yazar bilgisi olarak veriyoruz.yani author bilgisini de biz dolduruyoruz burda komutla.
        article.save()
        messages.success(request, "Makale başarı ile oluşturuldu.")
        return redirect("article:dashboard")

    return render(request, "addArticle.html",{"form":form}) 

def detail(request,id): #Django id yi otomatik olarak gönderiyor.
    # article = Article.objects.filter(id=id).first() # first koymazsan bu sorgu liste şeklinde bir yapı geitriyor o da bir obje olmuyor sonrasında hata veriyor biz first koyarak ilk objeyi almış oluyoruz.
    article = get_object_or_404(Article,id=id)#burada olmayan url id girdiğimizde boş sayfa yerine hata fırlatmış oluyoruz.
    comments = article.comments.all()
    return render(request, "detail.html", {"article":article,"comments":comments})

@login_required(login_url = "user:login")
def updateArticle(request,id):

    article = get_object_or_404(Article, id = id)#böyle bir id varsa alıyor yoksa get requeste cevap veriyor.
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)#form oluşturmak ile article objesi oluşturmak farklı şeyler karıştırma form oluşturmadığında objeyi almana rağmen bir şey gözükmüyordu biz burda objedenden gelen bilgilerle formu oluşturucağız.
    #instance parametresi ile biz article bilgilerini formun içine vermiş oluyoruz.
    if form.is_valid():

        article = form.save(commit=False) #author bilgisini almadan kaydetmesini önlemek için commit:false yaptık yoksa hata veriyor.çünkü biz input girdiğimizde author inputu yok girmiyoruz o nedenle hata veriyor.
        article.author = request.user #request eden user bilgisini yazar bilgisi olarak veriyoruz.yani author bilgisini de biz dolduruyoruz burda komutla.instance başlangıç değeri formun tekrar doludurulduğunda post yapıldığında yeni değerlerle doldurulmuş olacak.
        article.save()
        messages.success(request, "Makale başarı ile güncellendi.")
        return redirect("article:dashboard")

    return render(request,"update.html",{"form":form})

@login_required(login_url = "user:login")#ismi login olan url'ye gitmek istiyoruz girş yapmadan bazı fonsiyonlara ulaşmaya çalıştığımızda
def deleteArticle(request,id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Makale başarı ile silindi")

    return redirect("article:dashboard")

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword: # burda da arama yapılmaksızın tüm makaleleri görüntülemek için request olmuş olabilir onun kontrolünü burda yapıyoruz eğer aramaya bişey yazılmışsa True olucak ve if durumu içine girilmiş olucak.
        articles = Article.objects.filter(title__contains = keyword )
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()

    return render(request,"articles.html",{"articles":articles})


def addComment(request,id):  # aslında adres çubuğunda bu url hiç yazmıyor bu url yi biz kullanıcıdan sadece bilgi almak için kullanıyoruz.yada çok hızlı redirect olduğu için göremiyoruz.
    article = get_object_or_404(Article,id=id)   

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author, comment_content=comment_content)

        
        newComment.article = article

        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id})) 