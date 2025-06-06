from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import UserProfile
from .models import Activity, Department
from .forms import ActivityForm
from django.core.paginator import Paginator
from core.models import UserProfile  

def landing(request):
    # Create a context variable for the range of images
    image_range = range(1, 6)  # Numbers 1 to 10
    return render(request, 'landing.html', {'image_range': image_range})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Get or create the user's profile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Debugging: print the role
            print(f"User '{user.username}' role: {user_profile.role}")  # Add this line

            if user_profile.role == 'Ceso_Staff':
                return redirect('cesostaff_dashboard')
            else:
                return redirect('landing')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def guest(request):
    return render(request, 'guest.html')

@login_required
def cesostaff_dashboard(request):
    return render(request, 'cesostaff_dashboard.html')


def manage_research(request):
    return render(request, 'manage_research.html')

def manage_certificates(request):
    return render(request, 'manage_certificates.html')

def view_reports(request):
    return render(request, 'view_reports.html')

@login_required
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)

            # Add custom fields
            activity.faculty_name = request.POST.get('faculty_name')
            activity.faculty_department = request.POST.get('faculty_department')
            activity.student_name = request.POST.get('student_name')
            activity.student_department = request.POST.get('student_department')
            activity.staff_name = request.POST.get('staff_name')
            activity.staff_department = request.POST.get('staff_department')
            # Handle fees and tags
            activity.fees_expenses = request.POST.get('fees_expenses')
            activity.tags = request.POST.get('tags')

            # Save the activity instance to the database
            activity.save()

            # Handle ManyToMany relationships
            faculty_ids = request.POST.getlist('faculty')
            student_ids = request.POST.getlist('students')
            staff_ids = request.POST.getlist('staff')

            # Set ManyToMany relationships
            activity.faculty.set(faculty_ids)
            activity.students.set(student_ids)
            activity.staff.set(staff_ids)

            return redirect('manage_activities')
        else:
            print(form.errors)  # Debugging
    else:
        form = ActivityForm()
    return render(request, 'create_activity.html', {'form': form})


@login_required
def manage_activities(request):
    # Get search query from GET request
    search_query = request.GET.get('search', '')
    activities = Activity.objects.filter(is_archived=False)  # Exclude archived activities

    # Filter activities based on the search query if provided
    if search_query:
        activities = activities.filter(title__icontains=search_query)

    # Set up pagination - show 10 activities per page
    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass context to the template for rendering
    return render(request, 'manage_activities.html', {
        'page_obj': page_obj,          # Activities for the current page
        'search_query': search_query,  # Keep the search query in the form
        'total_activities': activities.count(),  # Total number of activities
        'sort_field': request.GET.get('sort', 'created_at'),  # Sorting field (e.g., created_at)
        'direction': request.GET.get('direction', 'asc'),     # Sorting direction (asc or desc)
    })
    
@login_required
def view_activity(request, pk=None, id=None):
    key = pk or id
    activity = get_object_or_404(Activity, pk=key)

    faculties = activity.faculty.all()
    students = activity.students.all()
    staff = activity.staff.all()

    context = {
        'activity': activity,
        'faculties': faculties,
        'students': students,
        'staff': staff,
    }
    return render(request, 'view_activity.html', context)

@login_required
def update_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if activity.status == 'Completed':
        return HttpResponse("This activity is finalized and cannot be edited.")
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)

            # Add custom fields
            activity.faculty_name = request.POST.get('faculty_name')
            activity.faculty_department = request.POST.get('faculty_department')
            activity.student_name = request.POST.get('student_name')
            activity.student_department = request.POST.get('student_department')
            activity.staff_name = request.POST.get('staff_name')
            activity.staff_department = request.POST.get('staff_department')
            # Handle fees and tags
            activity.fees_expenses = request.POST.get('fees_expenses')
            activity.tags = request.POST.get('tags')

            # Save the activity instance to the database
            activity.save()

            # Update ManyToMany relationships
            faculty_ids = request.POST.getlist('faculty')
            student_ids = request.POST.getlist('students')
            staff_ids = request.POST.getlist('staff')

            activity.faculty.set(faculty_ids)
            activity.students.set(student_ids)
            activity.staff.set(staff_ids)

            return redirect('manage_activities')
        else:
            print(form.errors)  # Debugging
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'update_activity.html', {'form': form, 'activity': activity})


def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('manage_activities')  # Redirect to the activities list after saving
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})

@login_required
def archive_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.is_archived = True
    activity.save()
    messages.success(request, f"Activity '{activity.title}' has been archived.")
    return redirect('manage_activities')

@login_required
def archived_activities(request):
    activities = Activity.objects.filter(is_archived=True)  # Only archived activities
    paginator = Paginator(activities, 10)  # Pagination
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'archived_activities.html', {
        'page_obj': page_obj,
    })

def restore_activity(request, pk):
    # Fetch the activity by primary key
    activity = get_object_or_404(Activity, pk=pk)

    # Update the is_archived field
    if activity.is_archived:
        activity.is_archived = False
        activity.save()

    # Redirect back to the archived activities page
    return redirect('archived_activities')  # Adjust this if needed