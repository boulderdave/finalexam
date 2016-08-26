import datetime as dt
from django.forms import modelformset_factory
from django.views.generic import FormView
from django.http import JsonResponse
from .models import Question
from .forms import QuestionForm


class QuestionView(FormView):
    form_class = modelformset_factory(
        Question,
        form=QuestionForm,
        extra=0)
    template_name = 'question/index.html'

    def set_start_time(self):
        """ Set the timer if it has not been started yet """
        if not self.request.session.get('start_time', None):
            self.request.session['start_time'] = str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def get(self, request, *args, **kwargs):
        """ Upon initially loading the page, set the timer. """
        self.set_start_time()
        return super(QuestionView, self).get(request, *args, **kwargs)

    def get_time_taken(self):
        """ Determine how long it took thus far """
        datetime_obj = dt.datetime.strptime(
            self.request.session.get(
                'start_time',
                str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            "%Y-%m-%d %H:%M:%S")
        return dt.datetime.now() - datetime_obj

    def serialize_data(self, formset):
        """ Serialize form and time data for JSON response. """
        data = {'time_taken': str(self.get_time_taken())}
        if not formset.is_valid():
            data['wrong_answers'] = []
            for form in formset.forms:
                if not form.is_valid():
                    data['wrong_answers'].append(
                        {'id': form.instance.id,
                         'question': form.instance.question}
                    )
        return data

    def get_form_kwargs(self):
        """
        Add the level filter to the formset kwargs
        """
        kwargs = super(QuestionView, self).get_form_kwargs()
        kwargs['queryset'] = Question.objects.filter(level__title=self.kwargs.get('level', 'xx'))
        return kwargs

    def form_invalid(self, form):
        """ Return JSON response. """
        return JsonResponse(self.serialize_data(form))

    def form_valid(self, form):
        """ Return JSON response and reset timer
            as all questions have been successfully answered
        """
        data = self.serialize_data(form)
        self.request.session.pop('start_time', None)
        return JsonResponse(data)
