from django.shortcuts import render, redirect, get_object_or_404
from .models import Practica
from .forms import RegistrationForm, LoginForm


def saludo(request):
    return render(request, "1-plantilla.html")


def vista(request):
    return render(request, "index.html")


def formulario(request, user_id=None):
    instancia = None
    if user_id:
        instancia = get_object_or_404(Practica, id=user_id)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            image_url = form.cleaned_data.get('image_url', '')

            if instancia:
                instancia.username = username
                instancia.password = password
                instancia.image_url = image_url
                instancia.save()
                return redirect('usuarios')

            # crear nuevo usuario
            if Practica.objects.filter(username=username).exists():
                return render(request, 'formulario.html', {'form': form, 'infosms': 'El usuario ya existe'})

            Practica.objects.create(username=username, password=password, image_url=image_url)
            return redirect('login')
    else:
        if instancia:
            form = RegistrationForm(initial={
                'username': instancia.username,
                'password1': instancia.password,
                'password2': instancia.password,
                'image_url': instancia.image_url,
            })
        else:
            form = RegistrationForm()

    return render(request, 'formulario.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Practica.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                return redirect('usuarios')
            except Practica.DoesNotExist:
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def usuarios(request):
    if not request.session.get('user_id'):
        return redirect('login')
    users = Practica.objects.all()
    return render(request, 'usuarios.html', {'users': users})


def eliminar(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    u = get_object_or_404(Practica, id=id)
    u.delete()
    return redirect('usuarios')


def editar(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    return formulario(request, user_id=id)


def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')