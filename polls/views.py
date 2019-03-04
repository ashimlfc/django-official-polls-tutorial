from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from django.template import loader

from .models import Question, Choice

# Create your views here.

def index(request):
	latest_question = Question.objects.order_by("-pub_date")[:5]
	context = {'latest_question': latest_question}

	return render(request, 'polls/index.html', context)

def detail(request, question_id):
		question = get_object_or_404(Question, pk = question_id)
		return render(request,'polls/detail.html', {'question' : question})

def results(request, question_id):
	return HttpResponse("These are the results of the question: %s" % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):

		#Redisplaying the voting form
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice."})

	else:
		selected_choice.votes += 1
		selected_choice.save()

		#returning an HttpResponse Redirect after succesfully dealig with POST data
		#prevents data from being posted twice if a user hits the back button

	return HttpResponseRedirect(reverse('polls:results', args = (question_id,)))
 