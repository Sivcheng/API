from django.core.cache import cache
from django.shortcuts import render, redirect
from .models import Student
import requests
from django.http import JsonResponse
import requests
import requests
from django.shortcuts import render

def home_view(request):
    context = {}
    
    # ១. ទាញខេត្ត
    try:
        res = requests.get("https://pumi.onrender.com/pumi/provinces")
        context['provinces'] = res.json() if res.status_code == 200 else []
    except:
        context['provinces'] = []

    # ២. ទាញស្រុក បើមានការជ្រើសរើសខេត្ត
    p_id = request.GET.get('province')
    if p_id:
        context['selected_province'] = p_id
        res_d = requests.get(f"https://pumi.onrender.com/pumi/districts?province_id={p_id}")
        context['districts'] = res_d.json() if res_d.status_code == 200 else []

    # ៣. ទាញឃុំ បើមានការជ្រើសរើសស្រុក
    d_id = request.GET.get('district')
    if d_id:
        context['selected_district'] = d_id
        res_c = requests.get(f"https://pumi.onrender.com/pumi/communes?district_id={d_id}")
        context['communes'] = res_c.json() if res_c.status_code == 200 else []

    return render(request, 'index.html', context)


def get_locations(request):
    loc_type = request.GET.get('type')  # district, commune, village
    parent_id = request.GET.get('id')
    
    # កំណត់ Parameter ឱ្យត្រូវនឹង API របស់ Pumi
    if loc_type == 'district':
        param_key = 'province_id'
    elif loc_type == 'commune':
        param_key = 'district_id'
    elif loc_type == 'village':
        param_key = 'commune_id' # ភូមិត្រូវការ ID របស់ឃុំ
    else:
        param_key = f"{loc_type}_id"
        
    url = f"https://pumi.onrender.com/pumi/{loc_type}s?{param_key}={parent_id}"
    response = requests.get(url)
    
    return JsonResponse(response.json(), safe=False)

def submit_registration(request):
    if request.method == 'POST':
        # ទាញយកទិន្នន័យពី Form
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        dob=request.POST.get("dob")
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        photo = request.FILES.get('photo') if hasattr(request, 'FILES') else None
        # ទីតាំង (ID)
        province = request.POST.get('province')
        district = request.POST.get('district')
        commune = request.POST.get('commune')
        village = request.POST.get('village')
        

        # រក្សាទុកចូលក្នុង Model
        Student.objects.create(
            full_name=full_name,
            gender=gender,
            dob=dob,
            province=province or 0,
            district=district or 0,
            commune=commune or 0,
            village=village or 0,
            father_name=father_name,
            mother_name=mother_name,
            photo=photo,
        )
        
        return redirect('student_list')
    return render(request, 'index.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})
