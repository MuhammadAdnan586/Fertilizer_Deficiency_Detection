from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
# views.py ke top par isay change karein
from .models import (
    UserHistory, FertilizerRate, FertilizerPrice, 
    FertilizerCalculation, FertilizerInfo
)

# --- 1. USER AUTHENTICATION ---
@api_view(['POST'])
def signup_user(request):
    data = request.data
    try:
        if User.objects.filter(username=data['email']).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('full_name', '')
        )
        return Response({"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- 2. RECOMMENDATION SYSTEM (Multilingual) ---
# --- Updated get_recommendation ---
@api_view(['GET'])
def get_recommendation(request):
    crop = request.GET.get('crop', 'Rice')
    deficiency = request.GET.get('deficiency', 'Nitrogen')

    info_obj = FertilizerInfo.objects.filter(
        crop_name__icontains=crop, 
        deficiency__icontains=deficiency
    ).first()

    # 1. Yahan dono options define karein
    def_map = {
        'Nitrogen': {'opt1': 'Urea', 'opt2': 'Ammonium Nitrate'},
        'Phosphorus': {'opt1': 'DAP', 'opt2': 'SSP (Single Super Phosphate)'},
        'Potassium': {'opt1': 'SOP', 'opt2': 'MOP (Muriate of Potash)'}
    }
    
    # Deficiency ke mutabiq fertilizers nikaalein
    selected_ferts = def_map.get(deficiency, {'opt1': 'Urea', 'opt2': 'Urea'})
    fert1_name = selected_ferts['opt1']
    fert2_name = selected_ferts['opt2']
    
    # Prices database se fetch karein
    price1_obj = FertilizerPrice.objects.filter(name=fert1_name).first()
    price2_obj = FertilizerPrice.objects.filter(name=fert2_name).first()

    if info_obj:
        return Response({
            'status': 'success',
            'deficiency': info_obj.deficiency.upper(),
            'titles': info_obj.titles,
            'symptoms': info_obj.symptoms,
            'fertilizer_1': fert1_name,
            'price1': str(price1_obj.current_price) if price1_obj else "12000", # Fallback price
            'fertilizer_2': fert2_name, # <-- Yeh ab data bhejega
            'price2': str(price2_obj.current_price) if price2_obj else "8500",  # <-- Yeh price bhejega
            'amount': "50kg/acre",
            'category': 'STANDARD',
            'note_key': 'CONSULT_EXPERT' # Note ke liye
        })
    
    return Response({'status': 'error', 'message': 'No data found'}, status=404)
    return Response({'status': 'error', 'message': 'No data found'}, status=404)
# --- 3. SCAN HISTORY MANAGEMENT ---
@api_view(['POST'])
def save_scan(request):
    data = request.data
    try:
        user_email = data.get('uid') 
        if not user_email:
            return Response({"error": "UID (email) is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.get(username=user_email)
        
        UserHistory.objects.create(
            user=user_obj,
            farmer_name=data.get('farmer_name', user_obj.first_name or "Farmer"),
            crop_name=data.get('crop'),
            deficiency_found=data.get('result'),
            suggested_fertilizer=data.get('fertilizers', "Consult local expert")
        )
        return Response({"status": "Success", "message": "Scan saved successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_history(request, email):
    try:
        history = UserHistory.objects.filter(user__username=email).order_by('-scanned_date')
        data = [{
            "scan_id": item.scan_id,
            "crop": item.crop_name,
            "result": item.deficiency_found,
            "recom": item.suggested_fertilizer,
            "date": item.scanned_date.strftime("%Y-%m-%d %H:%M")
        } for item in history]
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- 4. FERTILIZER CALCULATOR ---
@api_view(['GET'])
def get_rates(request):
    crop = request.GET.get('crop')
    area = request.GET.get('area')
    deficiency = request.GET.get('deficiency')
    
    rate = FertilizerRate.objects.filter(
        crop_name=crop, area_type=area, deficiency_type=deficiency
    ).first()

    if rate:
        return JsonResponse({
            'status': 'success',
            'bags_per_acre': rate.bags_per_acre,
            'fertilizer': rate.fertilizer_name
        })
    return JsonResponse({'status': 'error', 'message': 'No data found'}, status=404)

@api_view(['POST'])
def save_calculation(request):
    data = request.data
    try:
        user_email = data.get('uid')
        FertilizerCalculation.objects.create(
            uid=user_email,
            crop=data.get('crop'),
            area=float(data.get('area')),
            area_type=data.get('area_type'),
            result=data.get('result')
        )
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_calculations(request):
    uid = request.GET.get('uid')
    calcs = FertilizerCalculation.objects.filter(uid=uid).order_by('-id')
    data = [{
        "id": c.id, "crop": c.crop, "area": c.area, 
        "result": c.result, "created_at": c.created_at.strftime("%d %b, %Y")
    } for c in calcs]
    return JsonResponse(data, safe=False)

@api_view(['DELETE'])
def delete_calculation(request, pk):
    try:
        item = FertilizerCalculation.objects.get(pk=pk)
        item.delete()
        return Response({"message": "Deleted"}, status=200)
    except FertilizerCalculation.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    
    # model integrate
    
import os
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.core.files.storage import default_storage

# Models Path configuration
RICE_MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'rice_deficiency_model.h5')
MAIZE_MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'maize_deficiency_model.h5')

try:
    # Rice model (MobileNetV2) aur Maize model load ho rahe hain
    rice_model = load_model(RICE_MODEL_PATH, compile=False)
    maize_model = load_model(MAIZE_MODEL_PATH, compile=False)
    print("AI Models for Rice and Maize loaded successfully.")
except Exception as e:
    print(f"Model loading error: {e}")
    rice_model = None
    maize_model = None

def predict_deficiency(img_path):
    if rice_model is None or maize_model is None:
        return "Model Error", 0.0, "None"

    # 1. Image Preprocessing
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0 

    # 2. Labels mapping
    rice_labels = ['Background', 'Healthy', 'Nitrogen(N)', 'Phosphorus(P)', 'Potassium(K)']
    maize_labels = ['Background', 'Healthy', 'Nitrogen', 'Phosphorus', 'Potassium']

    # 3. Get raw predictions
    rice_probs = rice_model.predict(img_array)
    maize_probs = maize_model.predict(img_array)
    
    r_idx = np.argmax(rice_probs)
    m_idx = np.argmax(maize_probs)
    
    r_label, r_conf = rice_labels[r_idx], float(np.max(rice_probs) * 100)
    m_label, m_conf = maize_labels[m_idx], float(np.max(maize_probs) * 100)

    # 4. ADVANCED LOGIC: Background Conflict Resolution
    # Agar dono models keh rahe hain ke ye background hai
    if r_label == 'Background' and m_label == 'Background':
        return "Invalid Image", max(r_conf, m_conf), "None"

    # Case A: Rice model ne leaf detect ki aur Maize background keh raha hai
    if r_label != 'Background' and m_label == 'Background':
        return r_label, round(r_conf, 2), "Rice"

    # Case B: Maize model ne leaf detect ki aur Rice background keh raha hai
    if m_label != 'Background' and r_label == 'Background':
        return m_label, round(m_conf, 2), "Maize"

    # Case C: Agar dono models leaf detect kar rahe hain, to zyada confidence wala jeetay ga
    if r_label != 'Background' and m_label != 'Background':
        if r_conf >= m_conf:
            return r_label, round(r_conf, 2), "Rice"
        else:
            return m_label, round(m_conf, 2), "Maize"

    return "Low Confidence", 0.0, "None"

@csrf_exempt
def predict_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed.'}, status=405)

    img_file = request.FILES.get('image')
    if not img_file:
        return JsonResponse({'status': 'error', 'message': 'No image uploaded.'}, status=400)

    temp_name = f"temp_{np.random.randint(1000)}.jpg"
    file_name = default_storage.save(temp_name, img_file)
    file_path = default_storage.path(file_name)

    try:
        label, confidence, crop_type = predict_deficiency(file_path)

        # Immediate Cleanup for Robustness
        if os.path.exists(file_path):
            os.remove(file_path)

        # Threshold check (Min 70% confidence required for valid detection)
        if label in ["Invalid Image", "Low Confidence", "Model Error"] or confidence < 70:
            return JsonResponse({
                "status": "invalid",
                "message": "Please scan a clear Rice or Maize leaf.",
                "confidence": confidence
            })

        # 5. Database Matching Mapping
        db_mapping = {
            'Healthy': 'Healthy',
            'Nitrogen(N)': 'Nitrogen',
            'Phosphorus(P)': 'Phosphorus',
            'Potassium(K)': 'Potassium',
            'Nitrogen': 'Nitrogen',
            'Phosphorus': 'Phosphorus',
            'Potassium': 'Potassium'
        }
        
        clean_label = db_mapping.get(label, label)

        return JsonResponse({
            'status': 'success',
            'crop_type': crop_type,
            'prediction': clean_label,
            'confidence': confidence,
            'message': f'Healthy {crop_type} leaf!' if clean_label == 'Healthy' else f'{clean_label} deficiency in {crop_type}.'
        })

    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        return JsonResponse({'status': 'error', 'message': f"Internal Error: {str(e)}"}, status=500)
    from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def delete_account(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)
        
    try:
        # Django ke built-in User model mein user ko email se dhundna
        user = User.objects.get(email=email)
        user.delete() 
        return Response({"message": "Account deleted successfully"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found in database"}, status=404)