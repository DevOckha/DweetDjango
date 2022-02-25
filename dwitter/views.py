from django.shortcuts import render, redirect
from .models import Profile, Dweet
from .forms import DweetForm, CustomUserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def dashboard(request):
    if request.user.is_anonymous:
        return redirect('dwitter:login')

    form = DweetForm(request.POST or None)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect('dwitter:dashboard')

    followed_dweets = Dweet.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-created_at')
    
    page = request.GET.get('page')
    
    paginator = Paginator(followed_dweets, 5)
    
    try:
        followed_dweets = paginator.page(page)
    except PageNotAnInteger:
        followed_dweets = paginator.page(1)
    except EmptyPage:
        followed_dweets = paginator.page(paginator.num_pages)

    return render(request, 'dwitter/dashboard.html', {'form':form, 'dweets':followed_dweets},)





def profile_list(request):
    if request.user.is_anonymous:
        return redirect('dwitter:login')
    profiles = Profile.objects.exclude(user=request.user)

    page = request.GET.get('page')
    paginator = Paginator(profiles, 5)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    context = {'profiles':profiles}
    return render(request, 'dwitter/profile_list.html', context)




def profile(request, pk):
    if request.user.is_anonymous:
        return redirect('dwitter:login')
        
    profile = Profile.objects.get(id=pk)

    context = {'profile':profile}

    if request.method == 'POST':
        
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')

        if action == 'follow':
            current_user_profile.follows.add(profile)

        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, 'dwitter/profile.html', context)



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dwitter:dashboard')
        
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Account successfuly created!")

            user = authenticate(request, username= user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
            
            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'dwitter:dashboard'
            return redirect(next_url)
    
        else:
            messages.error(request, "An error has occured with registration")
    
    context = {'form':form}
    return render(request, 'dwitter/register.html', context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dwitter:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, "User with this Username does not exists")
            return redirect('dwitter:login')
        if user is not None:
            login(request, user)
            return redirect('dwitter:dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')
    
    context = {}
    return render(request, 'dwitter/login.html',context)



def logoutUser(request):
	logout(request)
	return redirect('dwitter:login')


