from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView, View

from .forms import (
    ContactOwnerForm,
    OwnerLoginForm,
    OwnerRegistrationForm,
    PropertyForm,
    PropertySearchForm,
)
from .models import Message, Property, PropertyImage


class PropertyListView(ListView):
    model = Property
    template_name = 'hostel_app/property_list.html'
    context_object_name = 'properties'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.filter(is_available=True)
        form = PropertySearchForm(self.request.GET)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            property_type = form.cleaned_data.get('property_type')

            if location:
                queryset = queryset.filter(location__icontains=location)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if property_type:
                queryset = queryset.filter(property_type=property_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PropertySearchForm(self.request.GET)
        return context


class OwnerRegisterView(FormView):
    template_name = 'hostel_app/register.html'
    form_class = OwnerRegistrationForm
    success_url = reverse_lazy('owner_dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class OwnerLoginView(LoginView):
    template_name = 'hostel_app/login.html'
    form_class = OwnerLoginForm
    success_url = reverse_lazy('owner_dashboard')


class OwnerLogoutView(LogoutView):
    next_page = reverse_lazy('property_list')


class OwnerDashboardView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'hostel_app/dashboard.html'
    context_object_name = 'properties'
    ordering = ['-created_at']

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'hostel_app/property_form.html'
    success_url = reverse_lazy('owner_dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'hostel_app/property_form.html'
    success_url = reverse_lazy('owner_dashboard')

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class PropertyDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
        property_obj.delete()
        return redirect('owner_dashboard')


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'hostel_app/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactOwnerForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ContactOwnerForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.property = self.object
            message.save()
            messages.success(request, 'Your message was sent successfully.')
            return redirect('property_detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)


class SaveFavoriteView(View):
    def get(self, request, property_id):
        favorites = request.session.get('favorites', [])
        if property_id not in favorites:
            favorites.append(property_id)
            request.session['favorites'] = favorites
        return redirect('property_list')


class FavoriteListView(View):
    def get(self, request):
        favorites = request.session.get('favorites', [])
        properties = Property.objects.filter(id__in=favorites)
        return redirect('property_list') if not properties else self.render(request, properties)

    def render(self, request, properties):
        from django.shortcuts import render
        return render(request, 'hostel_app/favorites.html', {'properties': properties})
