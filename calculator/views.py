from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

last_result = {}

def calculate_grade(cgpa):
    if cgpa >= 9.0:   return "O"
    elif cgpa >= 8.0: return "A+"
    elif cgpa >= 7.0: return "A"
    elif cgpa >= 6.0: return "B+"
    elif cgpa >= 5.0: return "B"
    else:             return "F"

def home(request):
    return render(request, 'calculator/index.html')

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'service': 'CGPA Calculator Microservice',
        'version': '1.0.0',
        'author': 'vishalpranavm21'
    })

@api_view(['GET'])
def grade_criteria(request):
    return Response({
        'grade_criteria': [
            {'grade': 'O',  'min_cgpa': 9.0, 'description': 'Outstanding'},
            {'grade': 'A+', 'min_cgpa': 8.0, 'description': 'Excellent'},
            {'grade': 'A',  'min_cgpa': 7.0, 'description': 'Very Good'},
            {'grade': 'B+', 'min_cgpa': 6.0, 'description': 'Good'},
            {'grade': 'B',  'min_cgpa': 5.0, 'description': 'Average'},
            {'grade': 'F',  'min_cgpa': 0.0, 'description': 'Fail'},
        ]
    })

@api_view(['GET', 'POST', 'DELETE'])
def calculate_cgpa(request):
    global last_result

    if request.method == 'GET':
        return Response({
            'message': 'CGPA Calculator API is running!',
            'usage': 'Send POST request with {"semesters": [8.5, 7.9, 8.2, 9.0]}',
            'endpoints': {
                'GET  /api/health/':    'Health check',
                'GET  /api/grades/':    'Grade criteria',
                'GET  /api/calculate/': 'API info',
                'POST /api/calculate/': 'Calculate CGPA',
                'DELETE /api/calculate/': 'Clear last result',
            }
        })

    elif request.method == 'POST':
        semesters = request.data.get('semesters', [])
        if not semesters:
            return Response({'error': 'No semester GPAs provided'}, status=400)
        if not all(0 <= s <= 10 for s in semesters):
            return Response({'error': 'GPA values must be between 0 and 10'}, status=400)
        cgpa = round(sum(semesters) / len(semesters), 2)
        percentage = round(cgpa * 9.5, 2)
        grade = calculate_grade(cgpa)
        last_result = {
            'cgpa': cgpa,
            'percentage': percentage,
            'grade': grade,
            'total_semesters': len(semesters),
            'semesters': semesters
        }
        return Response(last_result)

    elif request.method == 'DELETE':
        last_result = {}
        return Response({'message': 'Last result cleared successfully'}, status=200)
