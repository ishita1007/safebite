from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import  recipe,allergenlist,stateNames,UserAllergen
from .forms import RecipeFormUser,RecipeFormGuest
from django.db.models import Count

from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  UserAllergen
from .forms import AllergenForm

@login_required
def select_allergens(request):
    if request.method == 'POST':
        form = AllergenForm(request.POST)
        if form.is_valid():
            # Clear existing selections
            UserAllergen.objects.filter(user=request.user).delete()
            # Save new selections
            for allergen in form.cleaned_data['SelectedAllergen']:
                UserAllergen.objects.create(user=request.user, allergen=allergen)
            #return redirect('select_allergens')
            return render(request,'home.html')
    else:
        user_allergens = UserAllergen.objects.filter(user=request.user).values_list('allergen', flat=True)
        form = AllergenForm(initial={'SelectedAllergen': user_allergens})

    return render(request, 'select_allergens.html', {'form': form})

def hello(request):
     return render(request,'home.html')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def BlogPostLike(request):


    
    post = get_object_or_404(recipe, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    



def formfilter(state,allergen,request):
    
    values=recipe.objects.filter(state=state)
    result=[]
    nono=[]
    for a in allergen:
        print("+++++",a)
        
        allergylist=allergenlist.objects.filter(allergen=a)
        for x in allergylist:
            allerg=x.ingredientList
            allerg=allerg.split(",")
            
        for r in values:
            ingred=r.ingredient
            ingred=ingred.split(",")
            for i in ingred:
                for j in allerg:
                    if i.lower().strip()==j.lower().strip():
                        if r in nono:
                            pass
                        else:
                            liked = 0
                            if r.likes.filter(id=request.user.id).exists():
                                liked = 1
                            nono.append([r,liked])
    for i in values:
        if i not in nono:
            liked = 0
            if i.likes.filter(id=request.user.id).exists():
                 liked = 1
            result.append([i,liked])


            #print('ingredients are',ingred, 'for',r)
    result = sorted(result, key=lambda x: x[0].number_of_likes(), reverse=True)
    nono = sorted(nono, key=lambda x: x[0].number_of_likes(), reverse=True)
    
    #print("*******",result,'this is the final list')
    #print("-----",nono,"nono list")

    output=[result,nono]
    return(output)




def fooddir(request):
    SelectedAllergen = None
    values=None
    print(request.method)
    if request.user.is_authenticated:
        form = RecipeFormUser(request.POST)
    else:
        form = RecipeFormGuest(request.POST)
    
    
    
    if request.method == 'POST':
        if request.user.is_authenticated: 
         if form.is_valid():
       
            SelectedState=form.cleaned_data['SelectedState']
            SelectedAllergen = UserAllergen.objects.filter(user=request.user)
            
            print("---------",SelectedAllergen)
            if SelectedAllergen.exists()==False:
                SelectedAllergen=allergenlist.objects.filter(id="16")
         if SelectedState==None:
            messages.info(request,"please select a state")
        
         else:
            SelectedState = SelectedState.id
            if SelectedAllergen.exists()==False:
                print("!!!!!!!!!",SelectedAllergen)
                SelectedAllergen=allergenlist.objects.filter(id="16")
            
            SelectedAllergen = SelectedAllergen.values_list('allergen_id', flat=True)
            print("SELECTED ALLERGEN",SelectedAllergen)
            
        else:
            if form.is_valid():
                SelectedState=form.cleaned_data['SelectedState']
                SelectedAllergen=form.cleaned_data['SelectedAllergen']
                print(SelectedState)
            if SelectedState==None:
                messages.info(request,"please select a state")
        
            else:
                SelectedState = SelectedState.id
                SelectedAllergen = SelectedAllergen.values_list('id', flat=True)
                print("CMG",SelectedAllergen)
        
                print("!!!!!!!!!",SelectedAllergen)
        SelectedAllergen = ','.join(map(str, SelectedAllergen))
        return redirect(reverse('result') + f'?SelectedState={SelectedState}&SelectedAllergen={SelectedAllergen}')
    
            
    else:
        print("cmg")
        return render(request, 'fooddir.html',{'form':form})
    
def get_context_data(request):
        print("inside get_context_data")
        likes_connected = get_object_or_404(recipe, id=request.POST.get('blogpost_id'))
        liked = False
        if likes_connected.likes.filter(id=request.user.id).exists():
            liked = True
        number_of_likes = likes_connected.number_of_likes()
        post_is_liked = liked
        print("number_of_likes",number_of_likes,"post_is_liked",post_is_liked)
        return number_of_likes,post_is_liked
        



def result(request):
    SelectedAllergenids=request.GET.get("SelectedAllergen")
    SelectedAllergenid=SelectedAllergenids.split(",")
    print("IDDDDD",SelectedAllergenid)
    filters = Q()

    for value in SelectedAllergenid:
        filters |= Q(id=value)
    SelectedStateid=request.GET.get("SelectedState")
    print("SelectedStateid",SelectedStateid)
    SelectedState = stateNames.objects.get(id=SelectedStateid)
    SelectedAllergen = allergenlist.objects.filter(filters)
    #allergen, id, ingredientList, userallergen
    print(SelectedState,SelectedAllergen)
    

    if request.method=="GET":
        
        print("I am inside result", SelectedAllergen,SelectedState)
        values=recipe.objects.filter(state=SelectedState)
        for s in values:
            print(s)
            output=formfilter(SelectedState,SelectedAllergen,request)
            yes,no=output[0],output[1]
            
            
                 
        
            
        return render(request, 'result.html', {'yes':yes,'no':no})
    if request.method == 'POST':

        #if 'blogpost_id2' in request.POST:
                data=get_context_data(request)
                print("%%%%%%%%",data)
                print("HERE")

                BlogPostLike(request)
                
                return redirect(reverse('result') + f'?SelectedState={SelectedStateid}&SelectedAllergen={SelectedAllergenids}')

@login_required
def userprofile(request):

    user = request.user
    liked_recipes = user.blogpost_like.all()
    user_allergens = UserAllergen.objects.filter(user=request.user)
    
    print("****** USERPROFILE",liked_recipes)
    print("*****allergen",user_allergens)
    
    return render(request, 'userprofile.html', {'liked_recipes': liked_recipes,'user_allergens': user_allergens})
    






