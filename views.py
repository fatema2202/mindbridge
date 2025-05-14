from django.shortcuts import render, redirect, get_object_or_404
from .models import Therapist, CommunityForum, ProgressJournal, Testimonial, Appointment, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome, you have successfully logged in!')
                return redirect('home')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
   
    logout(request)
 
    return redirect('login')


def home(request):
    therapists = Therapist.objects.all()
    testimonials = Testimonial.objects.all()
    forum_posts = CommunityForum.objects.all()
    return render(request, 'accounts/home.html', {
        'therapists': therapists,
        'testimonials': testimonials,
        'forum_posts': forum_posts
    })

@login_required
def therapist_directory(request):
    therapists = Therapist.objects.all()
    return render(request, 'accounts/therapist_directory.html', {'therapists': therapists})

@login_required
def progress_journal(request):
    journals = ProgressJournal.objects.filter(user=request.user)
    return render(request, 'accounts/progress_journal.html', {'journals': journals})


@login_required
def testimonial_page(request):
    testimonials = Testimonial.objects.all()  
    return render(request, 'accounts/testimonial_page.html', {'testimonials': testimonials})


import stripe
from django.conf import settings
from .models import Therapist

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def payment_form(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    return render(request, 'accounts/payment_form.html', {'therapist': therapist})

def create_checkout_session(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)

    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'bdt',
                        'product_data': {
                            'name': therapist.name,
                        },
                        'unit_amount': int(therapist.fee * 100),  
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
        )
        return render(request, 'accounts/payment_form.html', {
            'checkout_session_id': checkout_session.id,
            'therapist': therapist,
        })
    except Exception as e:
        return str(e)
    
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'accounts/payment_success.html', {'payment': payment})


def payment_cancel(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'accounts/payment_cancel.html', {'payment': payment})

from .models import ProgressJournal

@login_required
def progress_journal(request):
    
    journals = ProgressJournal.objects.filter(user=request.user)
    return render(request, 'accounts/progress_journal.html', {'journals': journals})

@login_required
def create_journal_entry(request):
    if request.method == 'POST':
        
        mood = request.POST['mood']
        notes = request.POST['notes']
        journal = ProgressJournal(user=request.user, mood=mood, notes=notes)
        journal.save()
        return redirect('progress_journal')  
    return render(request, 'accounts/create_journal_entry.html')

@login_required
def journal_entry_update(request, journal_id):
    journal = get_object_or_404(ProgressJournal, id=journal_id, user=request.user)

    if request.method == 'POST':
        journal.mood = request.POST['mood']
        journal.notes = request.POST['notes']
        journal.save()
        return redirect('progress_journal')
    
    return render(request, 'accounts/journal_entry_update.html', {'journal': journal})

@login_required
def delete_journal_entry(request, journal_id):
    journal = get_object_or_404(ProgressJournal, id=journal_id, user=request.user)
    journal.delete()
    return redirect('progress_journal')

from .forms import TherapistSearchForm

def therapist_search(request):
    form = TherapistSearchForm(request.GET)  
    
    if form.is_valid():
        query = form.cleaned_data['query']
      
        therapists = Therapist.objects.filter(name__icontains=query) | Therapist.objects.filter(specialization__icontains=query)
    else:
        therapists = Therapist.objects.all()  

    return render(request, 'accounts/therapist_search.html', {'form': form, 'therapists': therapists})

def therapist_detail(request, therapist_id):
    
    therapist = get_object_or_404(Therapist, id=therapist_id)
    
  
    return render(request, 'accounts/therapist_detail.html', {'therapist': therapist})


from .forms import TherapistForm


@login_required
def create_therapist(request):
    if request.method == 'POST':
        form = TherapistForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('therapist_list')  
    else:
        form = TherapistForm()
    return render(request, 'accounts/create_therapist.html', {'form': form})


@login_required
def therapist_list(request):
    therapists = Therapist.objects.all() 
    return render(request, 'accounts/therapist_list.html', {'therapists': therapists})



login_required
def update_therapist(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    
    if request.method == 'POST':
        form = TherapistForm(request.POST, instance=therapist)
        if form.is_valid():
            form.save()  
            return redirect('therapist_list')  
    else:
        form = TherapistForm(instance=therapist)  
    
    return render(request, 'accounts/update_therapist.html', {'form': form, 'therapist': therapist})


@login_required
def delete_therapist(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    therapist.delete()  
    return redirect('therapist_list')

from .models import Appointment
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  
            appointment.save()
            return redirect('appointment_list')  
    else:
        form = AppointmentForm()
    return render(request, 'accounts/book_appointment.html', {'form': form})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user) 
    return render(request, 'accounts/appointment_list.html', {'appointments': appointments})


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'accounts/edit_appointment.html', {'form': form, 'appointment': appointment})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.status = 'Cancelled' 
    appointment.save()
    return redirect('appointment_list')




from .models import ForumTopic, Comment
from .forms import ForumTopicForm, CommentForm

def forum_topic_list(request):
    topics = ForumTopic.objects.all()  
    return render(request, 'accounts/forum_topic_list.html', {'topics': topics})


def forum_topic_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    comments = Comment.objects.filter(topic=topic)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.topic = topic
            comment.save()
            return redirect('forum_topic_detail', topic_id=topic.id) 
    else:
        comment_form = CommentForm()

    return render(request, 'accounts/forum_topic_detail.html', {'topic': topic, 'comments': comments, 'comment_form': comment_form})


@login_required
def create_forum_topic(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect('forum_topic_detail', topic_id=topic.id)  
    else:
        form = ForumTopicForm()
    return render(request, 'accounts/create_forum_topic.html', {'form': form})

@login_required
def edit_forum_topic(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id, user=request.user)  
    if request.method == 'POST':
        form = ForumTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('forum_topic_detail', topic_id=topic.id)
    else:
        form = ForumTopicForm(instance=topic)
    return render(request, 'accounts/edit_forum_topic.html', {'form': form, 'topic': topic})


@login_required
def delete_forum_topic(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id, user=request.user)  
    topic.delete()
    return redirect('forum_index')  


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)  
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum_topic_detail', topic_id=comment.topic.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'accounts/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)  
    topic_id = comment.topic.id
    comment.delete()
    return redirect('forum_topic_detail', topic_id=topic_id)  