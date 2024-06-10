from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai

# Create your views here.
# add here to your generated API key
genai.configure(api_key="AIzaSyBmtMFKlvUpUYtW2FLX-_qLvev71yxEMJk")

@login_required
def ask_question(request):
    if request.method == "POST":
        text = request.POST.get("text")
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        response = chat.send_message(text)
        user = request.user
        ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
        # Extract necessary data from response
        response_data = {
            "text": response.text,  # Assuming response.text contains the relevant response data
            # Add other relevant data from response if needed
        }
        # return JsonResponse({"data": response_data})
        return HttpResponseRedirect(reverse("chat") + f"?text={response_data['text']}")
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )  # Redirect to chat page for GET requests


# from django.http import HttpResponseBadRequest
# @login_required
# def ask_question(request):
#     if request.method == "POST":
#         text = request.POST.get("text")
#         if text.strip():  # Check if the text is not empty or contains only whitespace
#             model = genai.GenerativeModel("gemini-pro")
#             chat = model.start_chat()
#             response = chat.send_message(text)
#             user = request.user
#             ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
#             # Redirect to the chat page with the response data
#             return HttpResponseRedirect(reverse("chat") + f"?text={response.text}")
#         else:
#             return HttpResponseBadRequest("Text cannot be empty")  # Return error response for empty text
#     else:
#         return HttpResponseRedirect(reverse("chat"))  # Redirect to chat page for GET requests

# @login_required
# def chat(request):
#     user = request.user
#     chats = ChatBot.objects.filter(user=user)
#     return render(request, "chat_bot.html", {"chats": chats})

# @login_required
# def chat(request):
#     user = request.user
#     chats = ChatBot.objects.filter(user=user)
#     for chat in chats:
#         chat.sentences = chat.gemini_output.split('\n')  # Split gemini_output into sentences
#     return render(request, "chat_bot.html", {"chats": chats})

@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    for chat in chats:
        chat.sentences = [sentence.replace('*', '') for sentence in chat.gemini_output.split('\n') if sentence.strip()]  # Remove asterisks and empty sentences
    return render(request, "chat_bot.html", {"chats": chats})