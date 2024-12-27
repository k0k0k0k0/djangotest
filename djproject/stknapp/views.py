from django.shortcuts import render, redirect
from django.db.models import Sum, Max
from django.utils.timezone import localtime, make_aware, is_naive
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count

from .forms import PathForm
from .models import FileInfo  # модель данных
from . import stakanov # подцепили исходный скрипт, но почему именно такой синтаксис?



def extstats(request, num):
    try:
        num = int(num)  # строку в инт
        # запрашиваем num самых частых расширений
        extensions = (
            FileInfo.objects.values('extension')  # Group by the 'extension' field
            .annotate(count=Count('extension'))  # Count occurrences of each extension
            .order_by('-count')[:num]  # Sort by count in descending order and limit to `num`
        )

        context = {
            "extensions": extensions,
            "num": num,
        }
        return render(request, "extstats.html", context)
    except ValueError:
        return render(request, "extstats.html", {"error": "Invalid number of extensions specified."})

def sizetop(request, num):
    try:   
        num = int(num)  # строку в инт
        # запрашиваем num самых больших файлов
        top_files = FileInfo.objects.order_by('-size')[:num] 

        context = {
            "top_files": top_files,
            "num": num,
        }
        return render(request, "sizetop.html", context)
    except ValueError:
        return render(request, "sizetop.html", {"error": "Invalid number of files specified."})

from django.shortcuts import render
from .models import FileInfo

def imgtop(request, num):
    try:
        num = int(num)  # строку в инт
        # запрашиваем num самых больших картинок по IMG_size
        top_images = FileInfo.objects.filter(IMG_size__isnull=False).order_by('-IMG_size')[:num]

        context = {
            "top_images": top_images,
            "num": num,
        }
        return render(request, "imgtop.html", context)
    except ValueError:
        return render(request, "imgtop.html", {"error": "Invalid number of images specified."})

from django.shortcuts import render
from .models import FileInfo

def pagetop(request, num):
    try:
        num = int(num)  # строку в инт
        # запрашиваем num самых длинных PDF по PDF_num_pages
        top_pdfs = FileInfo.objects.filter(PDF_num_pages__isnull=False).order_by('-PDF_num_pages')[:num]

        context = {
            "top_pdfs": top_pdfs,
            "num": num,
        }
        return render(request, "pagetop.html", context)
    except ValueError:
        return render(request, "pagetop.html", {"error": "Invalid number of PDFs specified."})


def indexview(request):
    if request.method == "POST":
        # Check if "clear_db" button was pressed
        if "clear_db" in request.POST:
            # Clear the database
            FileInfo.objects.all().delete()
            success_message = "Database cleared successfully!"
            
            return render(request, 'index.html', {'success_message': success_message}) # Update the context to include the success message
        
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']

            #print("Data posted! "+ path)
            try:  
                la_pinta = stakanov.ResearchVessel(path)
                #print("Data received!")
                
                for data in la_pinta.fetch_file_objects_django():  # это спец. итератор, обертка fetch_file_objects для джанги
                    #print(data)
                    try:
                        FileInfo.objects.create(**data)  
                    except Exception as e:
                        print(f"Error: {e}")  
                    
                    #print("Data written!")
                
                #print("Data successfully processed and saved!")

                return redirect('sizetop', num=10)  
            except Exception as e:
                messages.error(request, f"Error processing path: {str(e)}")
    else:
        form = PathForm()

    total_size_bytes = FileInfo.objects.aggregate(total_size=Sum('size')).get('total_size', 0) or 0
    total_size_gb = total_size_bytes / (1024 ** 2)  # в GB

    # раз требование задания — использовать только одну таблицу, то самое новое время из таблицы индекса, которое = now 
    # (потому что оно автоматически подставляется now при индексации пустых полей last_modified)
    last_update = FileInfo.objects.aggregate(last_modified=Max('last_modified')).get('last_modified')

    # необходимая магия про часовые пояса
    if last_update and is_naive(last_update):
        from django.utils.timezone import get_current_timezone
        last_update = make_aware(last_update, get_current_timezone())

    context = { # отдали посчитанные переменные и форму в контекст
        "total_size_gb": round(total_size_gb, 2),  
        "last_update": localtime(last_update) if last_update else None,
        'form': form,
    }
    return render(request, "index.html", context)