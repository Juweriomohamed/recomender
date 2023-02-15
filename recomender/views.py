
from django.shortcuts import render


from engine import recommend_restaurants

# Create your views here.

def Recommender(request):
    if (request.method == 'POST'):
        final_model = []
        message = ''
        try:

            restaurant = request.POST['restaurant']

            data = recommend_restaurants(restaurant)

            for index, row in data.iterrows():
                final_model.append({
                    'isError': False,
                    'rest': index,
                    'cost': row['cost'],
                    'cuisines': row['cuisines'],
                    'rating': row['Mean Rating']

                })
        except IndexError:
            message = {
                'isError': True,
                'Message': "Sorry! The restaurant you requested is not in our dataset. Please check the spelling or try with some other restaurants"
            }
    return render(request, 'design/home.html', {'data': final_model, 'error': message})






