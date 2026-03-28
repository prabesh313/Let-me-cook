from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Create your views here.

def landing(request):
    return render(request, 'chef/landing.html')


def index(request):
    return render(request , 'chef/index.html')


def generate_recipe(request):
    if request.method == "POST":
        ingredients = request.POST.get('ingredients', '').strip()
        if not ingredients:
            return render(request, 'chef/index.html', {'error': 'Please enter some ingredients.'})
        
        prompt = f"""You are a creative chef. Given these ingredients: {ingredients}

Generate a complete recipe that uses most of them. Format your response clearly with:
- Recipe name (as a heading)
- Prep time and cook time
- Ingredients list with amounts
- Step-by-step cooking instructions
- One serving suggestion

Note: Do not follow **markdown formatting. Just provide the information in a clear, easy-to-read format.
after each point of recipe leave a line break. Do not use emojis or any special formatting.

Keep it practical, delicious, and easy to follow.


        """
        try:
            response = model.generate_content(prompt)
            recipe = response.text.strip()
        except Exception as e:
            return render(request, 'chef/index.html',
                          {'error': f'Error generating recipe: {str(e)}',
                           'ingredients': ingredients,
                           })

            
        return render(request, 'chef/result.html', {'recipe': recipe , 'ingredients': ingredients})
   
    return render(request, 'chef/index.html')

def nutrition(request):
    recipe = request.GET.get('recipe', '')
    ingredients = request.GET.get('ingredients', '')

    prompt = f"""Given this recipe and ingredients: {recipe}

Provide a detailed nutritional breakdown per serving . Format clearly with:
- Calories
- Protein (g)
- Carbohydrates (g)
- Fats (g)
- Fiber (g)
- Sugar (g)
- Sodium (mg)
- Vitamins and minerals (most significant ones)
- Overall health rating out of 10
- One short health tip about this meal
Note: Do not use **markdown formatting. Just provide the information in a clear, easy-to-read format.
"""

    try:
        response = model.generate_content(prompt)
        nutrition_info = response.text.strip()
    except Exception as e:
        nutrition_info = f"Error: {str(e)}"

    return render(request, 'chef/nutrition.html', {
        'nutrition': nutrition_info,
        'ingredients': ingredients,
    })


def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get('message', '')
        recipe_context = data.get('recipe_context', '')

        prompt = f"""You are a helpful chef assistant. The user is asking about this recipe and its nutrition:

{recipe_context}

User question: {user_message}

Answer helpfully and concisely. Stay on topic about the recipe, ingredients, cooking tips, and nutrition."""

        try:
            response = model.generate_content(prompt)
            reply = response.text.strip()
        except Exception as e:
            reply = f"Sorry, I couldn't process that: {str(e)}"

        return JsonResponse({'reply': reply})

    return render(request, 'chef/chatbot.html')