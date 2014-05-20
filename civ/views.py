from django.views.generic import FormView

from .forms import RoundForms

class HomePageView(FormView):
    template_name = 'civ/home.html'
    form_class = RoundForms

    def get(self, request, *args, **kwargs):
        self.initial.update(request.session.get('base_initial', {}))
        
        return super(HomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        
        field_list = []
        for field in context['form']:
            field_list.append(field)
        
        context['field_list'] = field_list
        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.request.session['base_initial'] = form.cleaned_data.copy()
        return self.render_to_response(self.get_context_data(form=form, result=form.calculate()))
