from django.shortcuts import render, redirect

from .models import ImageHolder
from .forms import ImageForm

from .utils import black_white_diff, get_client_ip, get_pixel_amount_by_hex
from .log import log_upload_image, log_count_hex


def main_view(request):
    image_url = request.session.get('last_saved_image', '/static/your_photo_here.png')
    form = ImageForm()

    white_count, black_count = black_white_diff(image_url)
    context = {'image_url': image_url, 'form': form,
               'pixel_color': {white_count: 'Белых', black_count: 'Черных'}[max(white_count, black_count)],
               'black_while_diff': max(white_count, black_count) - min(white_count, black_count)}

    if request.session.get('hex_color_requested', False):
        context['hex_color_requested'] = True
        context['hex_color'] = request.session['hex_color']
        context['hex_color_count'] = request.session['hex_color_count']

        del request.session['hex_color_requested']
        del request.session['hex_color']
        del request.session['hex_color_count']

    return render(request, 'base.html', context=context)


def file_upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():

            user_ip = get_client_ip(request)

            if form.cleaned_data['document']:
                saved_image = ImageHolder.objects.create(image=form.cleaned_data['document'],
                                                         user_ip=user_ip)

                request.session['last_saved_image'] = f'/media/{saved_image.image}'

                log_upload_image(user_ip, saved_image)

            if form.cleaned_data['hex_color']:
                hex_color = form.cleaned_data['hex_color']

                image_path = request.session.get('last_saved_image',
                                                 '/static/your_photo_here.png')
                hex_color_count = get_pixel_amount_by_hex(hex_color, image_path)

                request.session['hex_color_requested'] = True
                request.session['hex_color'] = hex_color
                request.session['hex_color_count'] = hex_color_count

                log_count_hex(user_ip, hex_color, image_path)

    return redirect('/image_analyzer/main/')
