from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    # Additional fields with proper attributes for form control
    faculty_name = forms.CharField(required=False, max_length=100, label='Faculty Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    faculty_department = forms.CharField(required=False, max_length=100, label='Faculty Department', widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_name = forms.CharField(required=False, max_length=100, label='Student Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_department = forms.CharField(required=False, max_length=100, label='Student Department', widget=forms.TextInput(attrs={'class': 'form-control'}))
    staff_name = forms.CharField(required=False, max_length=100, label='Staff Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    staff_department = forms.CharField(required=False, max_length=100, label='Staff Department', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Activity
        fields = [
            'title', 'start_date', 'end_date', 'start_time', 'end_time',
            'venue', 'conducted_by', 'description', 'attachment',
            'fees_expenses', 'tags', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'conducted_by': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fees_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        # Ensure any additional field styling remains consistent
        for field_name in ['faculty_name', 'faculty_department', 'student_name', 'student_department', 'staff_name', 'staff_department']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
