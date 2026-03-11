from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    # Validación adicional a nivel de formulario
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'malas palabras' in title.lower():  # Ejemplo de validación
            raise forms.ValidationError("El título contiene palabras prohibidas.")
        return title