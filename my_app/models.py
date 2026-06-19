from django.db import models
import requests

class Student(models.Model):
    # ព័ត៌មានផ្ទាល់ខ្លួន
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    
    # ទីតាំង (បន្ថែម default=0 ដើម្បីកុំឱ្យ Error ពេល Migrate)
    province = models.IntegerField(default=0)
    district = models.IntegerField(default=0)
    commune = models.IntegerField(default=0)
    village = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

    def _get_name_from_api(self, endpoint, id_val):
        # ការពារមិនឱ្យហៅ API បើ ID ជា 0
        if not id_val or id_val == 0:
            return "មិនបានជ្រើសរើស"
        try:
            url = f"https://pumi.onrender.com/pumi/{endpoint}?id={id_val}"
            response = requests.get(url, timeout=5)
            data = response.json()
            return data[0]['name_km'] if isinstance(data, list) and data else "មិនស្គាល់"
        except:
            return "កំហុស API"

    @property
    def province_name(self):
        return self._get_name_from_api("provinces", self.province)

    @property
    def district_name(self):
        return self._get_name_from_api("districts", self.district)

    @property
    def commune_name(self):
        return self._get_name_from_api("communes", self.commune)

    @property
    def village_name(self):
        return self._get_name_from_api("villages", self.village)