from django.shortcuts import render, redirect

from . forms import RegisterForm, LoginForm # şu anki klasörümüzün forms.py dosyasından RegisterForm clasını dahil etme

from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout #bu authenticate fonksiyonu aldığı kullanıcı ismi ve paraloya göre bizim db de böyle bir kullanıcı olup olmadığını sorgulayacak.
#logout fonsiyonuna biz request vericez zaten requestin içinde bizim user bilgilerimiz var.

from django.contrib import messages



def register(request):
        if request.method == "POST":
            form = RegisterForm(request.POST)
    
            if form.is_valid(): # clean methodunu çağırıyor.

                username = form.cleaned_data.get("username") # Bunları hangi kee ile dönmüşsek ona göre alıyoruz. 
                password = form.cleaned_data.get("password")

                newUser = User(username = username)
                newUser.set_password(password)
                newUser.save() # Kullanıcı veritabanına kaydediliyor.

                login(request, newUser) #içine bu user ı verirsek kullanıcı aynı zamanda sisteme login olmuş olucak. hem kayıt olmuş oldu hem de bu login sayesinde giriş yapmış oldu.

                messages.success(request,"Başarıyla kayıt oldunuz.")
                return redirect("index")
            
            context = { "form" : form # kullanıcının doldurmuş olduğu formu context ile register.html'e gönderiyoruz.


            }
            
            return render(request,"register.html", context)
        
        else:
            form = RegisterForm()
            context = { "form" : form


            }
            return render(request,"register.html", context)
   

def loginUser(request):

    form = LoginForm(request.POST or None) # ikinci yöntem get request olduğunda form boş olucak ancak post request olduğunda bu formumuz formdan gelen bilgilerle doldurulucak.

    context = {
        "form":form
    }

    if form.is_valid(): #formda herhangi bir sıkıntı çıkıp çıkmadığını kontrol ediyor.True ise (yani herhangi bir sıkıntı yok ise) giriş işlemi gerçekleşir.
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password") # forms.py clean methodu yazmamıza gerek yok registerda olduğu gibi forms.Form clasında nasıl tanımlanmışsa ona göre çalışacak.
        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request, "Kullanıcı Adı veya Parola Hatalı")
            return render (request, "login.html", context)

        messages.success(request,"Başarıyla giriş yaptınız")
        login(request,user)
        return redirect("index")

    return render(request, "login.html", context)
   

def logoutUser(request):

    logout(request)
    messages.success(request, "Başarı ile çıkış yaptınız")


    return redirect("index")


