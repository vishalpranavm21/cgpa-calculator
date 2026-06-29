from rest_framework.decorators import api_view
from rest_framework.response import Response

def calculate_grade(cgpa):
    if cgpa >= 9.0:   return "O"
    elif cgpa >= 8.0: return "A+"
    elif cgpa >= 7.0: return "A"
    elif cgpa >= 6.0: return "B+"
    elif cgpa >= 5.0: return "B"
    else:             return "F"

@api_view(['POST'])
def calculate_cgpa(request):
    semesters = request.data.get('semesters', [])
    if not semesters:
        return Response({'error': 'No semester GPAs provided'}, status=400)
    cgpa = round(sum(semesters) / len(semesters), 2)
    percentage = round(cgpa * 9.5, 2)
    return Response({
        'cgpa': cgpa,
        'percentage': percentage,
        'grade': calculate_grade(cgpa)
    })
