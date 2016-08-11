from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import ErrorLog


class GetAllErrors(View):
    template_name = 'errorlog/all_errors.html'

    def get(self, request):
        page = request.GET.get('page', 1)

        errors = ErrorLog.objects.all().order_by('-created_on')
        paginator = Paginator(errors, 10)

        try:
            errors = paginator.page(page)
        except EmptyPage:
            errors = paginator.page(paginator.num_pages)

        context = {'errors': errors}
        return render(request, self.template_name, context)


def delete_all_errors(request):
    ErrorLog.objects.all().delete()
    return HttpResponseRedirect(reverse('errorlog:all_errors'))
